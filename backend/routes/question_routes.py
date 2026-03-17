from flask import Blueprint, jsonify, request
from services.catalog_service import get_catalog

question_bp = Blueprint("questions", __name__)


@question_bp.route("/questions/next", methods=["POST"])
def next_question():
    payload = request.get_json(force=True) or {}
    answers = payload.get("answers") or {}

    catalog = get_catalog()
    questions = catalog.get("questions", [])

    unanswered = []
    for question in questions:
        qid = question.get("id")
        answer = answers.get(qid)
        if answer is None or answer == "" or answer == []:
            unanswered.append(question)

    if not unanswered:
        return jsonify({"status": "completed"})

    unanswered.sort(key=lambda q: q.get("difficulty") or 0)
    return jsonify(unanswered[0])
