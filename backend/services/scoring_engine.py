def _normalize_answer(answer, question):
    if question.get("type") == "scale":
        try:
            return float(answer) / 5.0
        except Exception:
            return 0.5
    return answer


def build_traits_from_answers(questions, answers):
    trait_sums = {}
    trait_counts = {}
    evidence = {}

    for question in questions:
        qid = question.get("id")
        answer = answers.get(qid)
        if answer is None or answer == "" or answer == []:
            continue

        if question.get("type") == "single":
            option = next((opt for opt in question.get("options", []) if opt.get("value") == answer), None)
            for trait, value in (option.get("traits") if option else {}).items():
                trait_sums[trait] = trait_sums.get(trait, 0) + value
                trait_counts[trait] = trait_counts.get(trait, 0) + 1

        if question.get("type") == "multi":
            for item in answer:
                option = next((opt for opt in question.get("options", []) if opt.get("value") == item), None)
                for trait, value in (option.get("traits") if option else {}).items():
                    trait_sums[trait] = trait_sums.get(trait, 0) + value
                    trait_counts[trait] = trait_counts.get(trait, 0) + 1

        if question.get("type") == "scale":
            trait = question.get("trait")
            normalized = _normalize_answer(answer, question)
            if trait:
                trait_sums[trait] = trait_sums.get(trait, 0) + normalized
                trait_counts[trait] = trait_counts.get(trait, 0) + 1

                evidence_text = None
                if normalized >= 0.8:
                    evidence_text = question.get("evidenceHigh")
                elif normalized <= 0.4:
                    evidence_text = question.get("evidenceLow")

                if evidence_text:
                    evidence.setdefault(trait, []).append(evidence_text)

    traits = {}
    for trait, total in trait_sums.items():
        traits[trait] = min(1.0, total / trait_counts.get(trait, 1))

    return traits, evidence


def compute_fit(user_traits, career_traits, weights=None):
    if not career_traits:
        return 0.0
    weights = weights or {}
    score = 0.0
    weight_total = 0.0
    for trait, required in career_traits.items():
        user_val = user_traits.get(trait, 0.4)
        weight = weights.get(trait, 1.0)
        score += max(0, 1 - abs(required - user_val)) * weight
        weight_total += weight
    return round(score / max(weight_total, 1), 4)


def build_reasons(career, user_traits, evidence):
    reasons = []
    trait_strengths = sorted(
        career.get("traits", {}).keys(),
        key=lambda t: user_traits.get(t, 0),
        reverse=True,
    )
    for trait in trait_strengths[:3]:
        if trait in evidence and evidence[trait]:
            reasons.append(evidence[trait][0])
        else:
            reasons.append(f"You show strength in {trait.replace('_', ' ')}.")

    stored_reasons = career.get("reasons") or []
    if stored_reasons:
        reasons.extend(stored_reasons[:2])
    return reasons[:4]
