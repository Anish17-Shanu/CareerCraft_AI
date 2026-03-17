import json
from datetime import datetime, timedelta
import urllib.parse
import urllib.request

from database import db
from models.external_cache import ExternalCache

BASE_URL = "http://api.dataatwork.org/v1"


def _fetch(url, timeout=6):
    request = urllib.request.Request(url, headers={"User-Agent": "CareerCraftAI/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def _cache_get(cache_key):
    entry = db.session.get(ExternalCache, cache_key)
    if not entry:
        return None
    if not entry.fetched_at:
        return None
    if entry.fetched_at + timedelta(seconds=entry.ttl_seconds) < datetime.utcnow():
        return None
    return entry.response_json


def _cache_set(cache_key, payload, ttl_seconds=86400):
    entry = db.session.get(ExternalCache, cache_key)
    if not entry:
        entry = ExternalCache(cache_key=cache_key)
        db.session.add(entry)
    entry.response_json = payload
    entry.fetched_at = datetime.utcnow()
    entry.ttl_seconds = ttl_seconds
    db.session.commit()


def _extract_jobs(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("jobs", "job_titles", "results"):
            if isinstance(payload.get(key), list):
                return payload[key]
    return []


def fetch_job_suggestions(query, limit=8):
    if not query:
        return []

    safe_query = urllib.parse.quote(query)
    contains_url = f"{BASE_URL}/jobs/autocomplete?contains={safe_query}"
    begins_url = f"{BASE_URL}/jobs/autocomplete?begins_with={safe_query}"

    cache_key = f"jobs:{query.lower()}:{limit}"
    cached = _cache_get(cache_key)
    if cached is not None:
        data = cached
    else:
        try:
            data = _fetch(contains_url)
        except Exception:
            try:
                data = _fetch(begins_url)
            except Exception:
                return []
        _cache_set(cache_key, data)

    jobs = _extract_jobs(data)
    if not jobs:
        return []

    suggestions = []
    for item in jobs[:limit]:
        suggestion = item.get("suggestion") or item.get("title")
        if suggestion:
            suggestions.append(
                {
                    "title": suggestion,
                    "uuid": item.get("uuid") or item.get("id"),
                    "source": "Open Skills API",
                }
            )

    return suggestions


def fetch_related_skills(job_id, limit=8):
    if not job_id:
        return []
    url = f"{BASE_URL}/jobs/{job_id}/related_skills"
    cache_key = f"skills:{job_id}:{limit}"
    cached = _cache_get(cache_key)
    if cached is not None:
        data = cached
    else:
        try:
            data = _fetch(url)
        except Exception:
            return []
        _cache_set(cache_key, data)

    skills = []
    if isinstance(data, dict):
        skills = data.get("skills") or data.get("results") or []
    elif isinstance(data, list):
        skills = data

    parsed = []
    for item in skills[:limit]:
        name = item.get("skill_name") or item.get("name")
        if name:
            parsed.append(
                {
                    "name": name,
                    "level": item.get("importance") or item.get("level"),
                }
            )
    return parsed


def fetch_related_jobs(job_id, limit=8):
    if not job_id:
        return []
    url = f"{BASE_URL}/jobs/{job_id}/related_jobs"
    cache_key = f"related_jobs:{job_id}:{limit}"
    cached = _cache_get(cache_key)
    if cached is not None:
        data = cached
    else:
        try:
            data = _fetch(url)
        except Exception:
            return []
        _cache_set(cache_key, data)

    jobs = _extract_jobs(data)
    parsed = []
    for item in jobs[:limit]:
        title = item.get("title") or item.get("job_title") or item.get("suggestion")
        if title:
            parsed.append(
                {
                    "title": title,
                    "uuid": item.get("uuid") or item.get("id"),
                }
            )
    return parsed


def fetch_external_bundle(query, limit=8):
    suggestions = fetch_job_suggestions(query, limit=limit)
    primary_id = suggestions[0]["uuid"] if suggestions and suggestions[0].get("uuid") else None
    return {
        "suggestions": suggestions,
        "related_skills": fetch_related_skills(primary_id, limit=limit),
        "related_jobs": fetch_related_jobs(primary_id, limit=limit),
    }
