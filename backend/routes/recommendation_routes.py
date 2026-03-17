from flask import Blueprint, jsonify, request
from services.catalog_service import get_catalog
from services.scoring_engine import build_traits_from_answers, compute_fit, build_reasons

recommendation_bp = Blueprint("recommendations", __name__)


@recommendation_bp.route("/recommendations/score", methods=["POST"])
def score_recommendations():
    payload = request.get_json(force=True) or {}
    answers = payload.get("answers") or {}
    limit = int(payload.get("limit", 6))
    offset = int(payload.get("offset", 0))

    catalog = get_catalog()
    questions = catalog.get("questions", [])
    careers = catalog.get("careers", [])

    user_traits, evidence = build_traits_from_answers(questions, answers)

    ranked = []
    for career in careers:
        weights = career.get("weights") or {trait: 1.0 for trait in (career.get("traits") or {}).keys()}
        score = compute_fit(user_traits, career.get("traits") or {}, weights)
        ranked.append(
            {
                **career,
                "fit_score": score,
                "reasons": build_reasons(career, user_traits, evidence),
            }
        )

    ranked.sort(key=lambda item: item["fit_score"], reverse=True)
    paged = ranked[offset : offset + limit]

    return jsonify(
        {
            "results": paged,
            "total": len(ranked),
            "offset": offset,
            "limit": limit,
            "traits": user_traits,
        }
    )


@recommendation_bp.route("/profile/summary", methods=["POST"])
def profile_summary():
    payload = request.get_json(force=True) or {}
    answers = payload.get("answers") or {}
    catalog = get_catalog()
    questions = catalog.get("questions", [])

    traits, evidence = build_traits_from_answers(questions, answers)

    top_traits = [
        {"trait": trait, "score": score}
        for trait, score in sorted(traits.items(), key=lambda item: item[1], reverse=True)
    ][:10]

    return jsonify(
        {
            "traits": top_traits,
            "evidence": evidence,
        }
    )
