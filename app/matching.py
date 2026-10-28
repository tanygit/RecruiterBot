
def _parse_values(value):
    """Convert comma-separated text into a normalized set."""
    if not value:
        return set()

    return {
        item.strip().casefold()
        for item in value.split(",")
        if item.strip()
    }


def calculate_match(candidate, job):
    candidate_skills = _parse_values(candidate["skills"])
    required_skills = _parse_values(job["required_skills"])

    matched_skills = sorted(candidate_skills & required_skills)
    missing_skills = sorted(required_skills - candidate_skills)

    if required_skills:
        skill_score = (
            len(matched_skills) / len(required_skills)
        ) * 100
    else:
        skill_score = 100.0

    years = int(candidate["experience_years"])
    minimum = int(job["min_experience_years"])

    if minimum <= 0:
        experience_score = 100.0
    else:
        experience_score = min(
            100.0,
            (years / minimum) * 100
        )

    final_score = round(
        0.70 * skill_score + 0.30 * experience_score,
        2
    )

    candidate_traits = _parse_values(candidate["traits"])
    culture_keywords = _parse_values(job["culture_keywords"])

    culture_overlap = sorted(
        candidate_traits & culture_keywords
    )

    reason = (
        f"Matches {len(matched_skills)} of "
        f"{len(required_skills)} required skills; "
        f"has {years} years of experience against "
        f"a minimum of {minimum}."
    )

    if missing_skills:
        reason += (
            " Missing skills: "
            + ", ".join(missing_skills)
            + "."
        )

    if culture_overlap:
        reason += (
            " Culture keyword overlap: "
            + ", ".join(culture_overlap)
            + "."
        )

    if candidate["availability"].casefold() == "not looking":
        reason += " Availability is listed as 'Not looking'."

    return {
        "score": final_score,
        "skill_score": round(skill_score, 2),
        "experience_score": round(experience_score, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "culture_overlap": culture_overlap,
        "reason": reason,
    }
