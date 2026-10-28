
# Recruiter Bot

The application ranks candidates against job openings using an explainable matching algorithm.

## Features

- Loads the 15 supplied candidates and six jobs.
- Ranks candidates for a selected job.
- Ranks jobs for a selected candidate.
- Returns scores, matched skills, missing skills, and explanations.
- Uses handwritten SQL through Python's sqlite3 module.
- Includes the SQL Detective Challenge and automated tests.

## Technology Stack

- Python
- Flask
- SQLite
- pytest

## Setup

Python 3.10 or newer is recommended.

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate
python -m pip install -r requirements.txt
python -m scripts.seed
python run.py
```

The server runs at http://127.0.0.1:5000.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /health | Health check |
| GET | /candidates | List candidates |
| GET | /jobs | List jobs |
| GET | /candidates/1/matches | Rank jobs for candidate 1 |
| GET | /jobs/1/matches | Rank candidates for job 1 |

Unknown candidate or job IDs return HTTP 404.

## Matching Algorithm

Skill score is the percentage of required skills possessed by the candidate.

Experience score is the candidate's experience divided by the job's minimum experience, capped at 100. If minimum experience is zero, the experience score is 100.

Final score:

Final Score = 0.70 × Skill Score + 0.30 × Experience Score

The scores are ranking heuristics, not probabilities of hiring success. Results are sorted by score, with candidate name or job title used to break ties.

Availability and culture overlap are included in explanations but do not affect the numerical score.

## Database Design

The database contains candidates and jobs tables. Skills and keywords are stored as comma-separated values to keep the fixed sample dataset simple.

Matches are calculated when requested rather than stored, so scores do not become stale when profile data changes.

## SQL Detective Challenge

The file sql_detective.sql contains queries for all five questions.

Question 3 infers job associations from interview records because the supplied schema does not contain a separate application-to-job table. Email addresses are normalized to handle capitalization differences.

## Tests

Run:

```powershell
python -m pytest -q
```
