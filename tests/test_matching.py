
from app.matching import calculate_match


def test_perfect_skill_and_experience_match():
    candidate = {
        "skills": "python, sql",
        "experience_years": 5,
        "traits": "analytical",
        "availability": "Immediate",
    }

    job = {
        "required_skills": "python, sql",
        "min_experience_years": 3,
        "culture_keywords": "analytical",
    }

    result = calculate_match(candidate, job)

    assert result["score"] == 100
    assert result["matched_skills"] == ["python", "sql"]
    assert result["missing_skills"] == []


def test_missing_skills_reduce_score():
    candidate = {
        "skills": "python",
        "experience_years": 3,
        "traits": "",
        "availability": "Immediate",
    }

    job = {
        "required_skills": "python, sql",
        "min_experience_years": 3,
        "culture_keywords": "",
    }

    result = calculate_match(candidate, job)

    assert result["score"] == 65
    assert result["matched_skills"] == ["python"]
    assert result["missing_skills"] == ["sql"]


def test_experience_score_is_capped_at_100():
    candidate = {
        "skills": "python, sql",
        "experience_years": 10,
        "traits": "",
        "availability": "Immediate",
    }

    job = {
        "required_skills": "python, sql",
        "min_experience_years": 5,
        "culture_keywords": "",
    }

    result = calculate_match(candidate, job)

    assert result["score"] == 100
