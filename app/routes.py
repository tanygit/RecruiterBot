
from flask import Blueprint, jsonify

from .database import get_db
from .matching import calculate_match

api = Blueprint("api", __name__)


def _split_values(value):
    if not value:
        return []

    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]


def _candidate_response(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "skills": _split_values(row["skills"]),
        "experience_years": row["experience_years"],
        "availability": row["availability"],
        "traits": _split_values(row["traits"]),
        "quirk": row["quirk"],
    }


def _job_response(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "required_skills": _split_values(row["required_skills"]),
        "min_experience_years": row["min_experience_years"],
        "culture_keywords": _split_values(row["culture_keywords"]),
        "tagline": row["tagline"],
    }


@api.get("/candidates")
def get_candidates():
    rows = get_db().execute(
        "SELECT * FROM candidates ORDER BY id"
    ).fetchall()

    return jsonify({
        "candidates": [
            _candidate_response(row) for row in rows
        ]
    })


@api.get("/jobs")
def get_jobs():
    rows = get_db().execute(
        "SELECT * FROM jobs ORDER BY id"
    ).fetchall()

    return jsonify({
        "jobs": [_job_response(row) for row in rows]
    })


@api.get("/candidates/<int:candidate_id>")
def get_candidate(candidate_id):
    row = get_db().execute(
        "SELECT * FROM candidates WHERE id = ?",
        (candidate_id,)
    ).fetchone()

    if row is None:
        return jsonify({
            "error": f"Candidate {candidate_id} not found."
        }), 404

    return jsonify(_candidate_response(row))


@api.get("/jobs/<int:job_id>")
def get_job(job_id):
    row = get_db().execute(
        "SELECT * FROM jobs WHERE id = ?",
        (job_id,)
    ).fetchone()

    if row is None:
        return jsonify({
            "error": f"Job {job_id} not found."
        }), 404

    return jsonify(_job_response(row))


@api.get("/jobs/<int:job_id>/matches")
def matches_for_job(job_id):
    db = get_db()

    job_row = db.execute(
        "SELECT * FROM jobs WHERE id = ?",
        (job_id,)
    ).fetchone()

    if job_row is None:
        return jsonify({
            "error": f"Job {job_id} not found."
        }), 404

    job = dict(job_row)
    candidates = db.execute(
        "SELECT * FROM candidates"
    ).fetchall()

    matches = []

    for row in candidates:
        candidate = dict(row)
        result = calculate_match(candidate, job)

        matches.append({
            "candidate_id": candidate["id"],
            "candidate_name": candidate["name"],
            **result,
        })

    matches.sort(
        key=lambda item: (
            -item["score"],
            item["candidate_name"].casefold()
        )
    )

    return jsonify({
        "job_id": job["id"],
        "job_title": job["title"],
        "scoring": {
            "skill_weight": 0.70,
            "experience_weight": 0.30,
            "note": "The score is a ranking heuristic, not a hiring probability."
        },
        "matches": matches,
    })


@api.get("/candidates/<int:candidate_id>/matches")
def matches_for_candidate(candidate_id):
    db = get_db()

    candidate_row = db.execute(
        "SELECT * FROM candidates WHERE id = ?",
        (candidate_id,)
    ).fetchone()

    if candidate_row is None:
        return jsonify({
            "error": f"Candidate {candidate_id} not found."
        }), 404

    candidate = dict(candidate_row)

    jobs = db.execute(
        "SELECT * FROM jobs"
    ).fetchall()

    matches = []

    for row in jobs:
        job = dict(row)
        result = calculate_match(candidate, job)

        matches.append({
            "job_id": job["id"],
            "job_title": job["title"],
            **result,
        })

    matches.sort(
        key=lambda item: (
            -item["score"],
            item["job_title"].casefold()
        )
    )

    return jsonify({
        "candidate_id": candidate["id"],
        "candidate_name": candidate["name"],
        "scoring": {
            "skill_weight": 0.70,
            "experience_weight": 0.30,
            "note": "The score is a ranking heuristic, not a hiring probability."
        },
        "matches": matches,
    })
