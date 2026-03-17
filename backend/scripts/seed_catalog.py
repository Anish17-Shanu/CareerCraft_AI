import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import create_app
from database import db
from models.question import Question, QuestionMeta, QuestionOption
from models.career import Career, CareerTrait, CareerTag, CareerReason, CareerRole
from models.career_roadmap import CareerRoadmap
from services.catalog_service import get_fallback_catalog


def _ensure_question(question_data, difficulty):
    question = Question.query.filter_by(question_text=question_data["text"]).first()
    if not question:
        question = Question(
            question_text=question_data["text"],
            category=question_data.get("category") or question_data.get("id") or "general",
            trait=question_data.get("trait"),
            response_type=question_data.get("type"),
            difficulty=difficulty,
            active=True,
        )
        db.session.add(question)
        db.session.flush()
    else:
        question.category = question_data.get("category") or question_data.get("id") or question.category
        question.trait = question_data.get("trait") or question.trait
        question.response_type = question_data.get("type") or question.response_type
        question.difficulty = difficulty
        question.active = True

    meta = db.session.get(QuestionMeta, question.question_id)
    if not meta:
        meta = QuestionMeta(question_id=question.question_id)
        db.session.add(meta)

    meta.required = bool(question_data.get("required", True))
    meta.why = question_data.get("why")
    meta.min_label = question_data.get("minLabel")
    meta.max_label = question_data.get("maxLabel")
    meta.evidence_high = question_data.get("evidenceHigh")
    meta.evidence_low = question_data.get("evidenceLow")
    meta.placeholder = question_data.get("placeholder")

    QuestionOption.query.filter_by(question_id=question.question_id).delete()
    for option in question_data.get("options") or []:
        db.session.add(
            QuestionOption(
                question_id=question.question_id,
                label=option.get("label"),
                value=option.get("value"),
                detail=option.get("detail"),
                traits=option.get("traits") or {},
            )
        )


def _generate_reasons(career_data):
    reasons = []
    traits = list((career_data.get("traits") or {}).keys())
    if traits:
        reasons.append(f"Strong alignment with {traits[0].replace('_', ' ')}.")
    if len(traits) > 1:
        reasons.append(f"Your signals suggest fit in {traits[1].replace('_', ' ')} work.")
    reasons.append("This path matches your interests and working style preferences.")
    return reasons[:3]


def _weight_for_trait(trait):
    high = {"coding", "data", "systems", "design", "marketing", "business", "communication"}
    if trait in high:
        return 1.3
    return 1.0


def _ensure_career(career_data):
    career = Career.query.filter_by(career_name=career_data["name"]).first()
    if not career:
        career = Career(
            career_name=career_data["name"],
            domain=career_data.get("path"),
            description=career_data.get("summary"),
        )
        db.session.add(career)
        db.session.flush()
    else:
        career.domain = career_data.get("path") or career.domain
        career.description = career_data.get("summary") or career.description

    CareerTrait.query.filter_by(career_id=career.career_id).delete()
    for trait, level in (career_data.get("traits") or {}).items():
        db.session.add(
            CareerTrait(
                career_id=career.career_id,
                trait=trait,
                required_level=level,
                weight=_weight_for_trait(trait),
            )
        )

    CareerTag.query.filter_by(career_id=career.career_id).delete()
    for tag in career_data.get("tags") or []:
        db.session.add(
            CareerTag(
                career_id=career.career_id,
                tag=tag,
            )
        )

    CareerRoadmap.query.filter_by(career_id=career.career_id).delete()
    for index, step in enumerate(career_data.get("roadmap") or [], start=1):
        db.session.add(
            CareerRoadmap(
                career_id=career.career_id,
                step_order=index,
                description=step,
            )
        )

    CareerRole.query.filter_by(career_id=career.career_id).delete()
    for index, role in enumerate(career_data.get("roles") or [], start=1):
        db.session.add(
            CareerRole(
                career_id=career.career_id,
                role_order=index,
                role_title=role,
            )
        )

    CareerReason.query.filter_by(career_id=career.career_id).delete()
    reasons = career_data.get("reasons") or _generate_reasons(career_data)
    for index, reason in enumerate(reasons, start=1):
        db.session.add(
            CareerReason(
                career_id=career.career_id,
                reason_order=index,
                reason_text=reason,
            )
        )


def seed_catalog():
    catalog = get_fallback_catalog()
    for idx, question in enumerate(catalog["questions"], start=1):
        _ensure_question(question, idx)
    for career in catalog["careers"]:
        _ensure_career(career)
    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_catalog()
        print("Catalog seeded successfully.")
