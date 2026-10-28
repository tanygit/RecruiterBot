
from app import create_app
from app.database import get_db, init_db
from app.seed_data import seed_database

app = create_app()

with app.app_context():
    init_db()
    seed_database(get_db())

    db = get_db()

    candidate_count = db.execute(
        "SELECT COUNT(*) FROM candidates"
    ).fetchone()[0]

    job_count = db.execute(
        "SELECT COUNT(*) FROM jobs"
    ).fetchone()[0]

    print(f"Candidates loaded: {candidate_count}")
    print(f"Jobs loaded: {job_count}")
