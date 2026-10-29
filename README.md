# Recruiter Bot

Recruiter Bot is a Flask backend that ranks candidates against job openings using an explainable matching algorithm. It uses a SQLite database to retrieve candidate and job data.

## Features

- Loads the 15 supplied candidates and six jobs using a seed script.
- Ranks candidates for a selected job.
- Ranks jobs for a selected candidate.
- Returns match scores, matched skills, missing skills, and explanations.
- Uses handwritten SQL through Python's `sqlite3` module, without an ORM or query builder.
- Includes the SQL Detective Challenge and automated tests.

## Technology Stack

- Python
- Flask
- SQLite
- pytest

## Setup and Installation

Open Terminal in the project root and run:

```powershell
git clone https://github.com/tanygit/RecruiterBot.git
cd RecruiterBot

python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m scripts.seed
python run.py
```

The server runs at:

http://127.0.0.1:5000

Keep the terminal running while making API requests.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check API health |
| GET | `/candidates` | List candidates |
| GET | `/jobs` | List job openings |
| GET | `/jobs/1/matches` | Rank candidates for job ID 1 |
| GET | `/candidates/1/matches` | Rank jobs for candidate ID 1 |

The ID `1` in the matching examples is illustrative; other valid IDs can be used.

Unknown candidate or job IDs return HTTP 404.

### Example API Requests

Run these commands in a second PowerShell terminal while the server is running:

```powershell
curl.exe http://127.0.0.1:5000/health
curl.exe http://127.0.0.1:5000/candidates
curl.exe http://127.0.0.1:5000/jobs
curl.exe http://127.0.0.1:5000/jobs/1/matches
curl.exe http://127.0.0.1:5000/candidates/1/matches
```

## Matching Algorithm

The matching algorithm considers skill overlap and experience fit.

**1. Skill score**

The percentage of required job skills possessed by the candidate:

`Skill Score = (Matched Required Skills / Total Required Skills) × 100`

If a job has no required skills, the skill score is 100.

**2. Experience score**

The candidate's experience relative to the job's minimum experience, capped at 100:

`Experience Score = min(100, Candidate Experience / Minimum Experience × 100)`

If the minimum experience is zero, the experience score is 100.

**3. Final score**

`Final Score = (0.70 × Skill Score) + (0.30 × Experience Score)`

Skills receive 70% of the weight, while experience receives 30%. This prioritizes relevant skills while still accounting for experience.

The final score is a ranking heuristic, not a probability of hiring success. Availability and culture overlap are included in explanations but do not affect the numerical score. Results are sorted by score, with candidate name or job title used to break ties.

## Matching Algorithm Example

Consider a job with these requirements:

- **Required skills:** Python, SQL, Flask, Machine Learning
- **Minimum experience:** 3 years

A candidate has the following profile:

- **Skills:** Python, SQL, Machine Learning
- **Experience:** 2 years
- **Traits:** Analytical
- **Availability:** Immediate

### 1. Skill Score

The candidate matches 3 of the 4 required skills. Flask is missing.

`Skill Score = (Matched Skills / Total Required Skills) × 100`

`Skill Score = (3 / 4) × 100 = 75.00`

### 2. Experience Score

The candidate has 2 years of experience, compared with the required 3 years.

`Experience Score = min(100, (Candidate Experience / Minimum Experience) × 100)`

`Experience Score = min(100, (2 / 3) × 100) = 66.67`

### 3. Final Matching Score

Skills contribute 70% of the final score, while experience contributes 30%.

`Final Score = (0.70 × Skill Score) + (0.30 × Experience Score)`

`Final Score = (0.70 × 75.00) + (0.30 × 66.67)`

`Final Score = 52.50 + 20.00 = 72.50`


## Database Design and Trade-offs

The application uses SQLite with separate tables for candidates and jobs. Skills, traits, and keywords are stored as comma-separated values to keep the supplied sample dataset simple.

Database operations use SQL through Python's `sqlite3` module, providing direct control over queries without an ORM or query builder.

Matches are calculated when requested instead of being stored in the database. This avoids retaining stale match scores when candidate or job information changes.

The scoring weights are configurable design choices and could be refined using recruiter feedback or evaluation data. For a larger application, skills and keywords could be normalized into separate relational tables.

## SQL Detective Challenge

The `sql_detective.sql` file contains queries for all five questions in the assignment.

The SQL challenge uses the separate hiring-operations schema supplied in the assignment and is independent of the application's SQLite database.

### Questions Covered

1. **Open Job Postings:** List all currently open job postings along with the names of their recruiters.

2. **Final-Stage Applicants:** Count the distinct applicants who reached the Final interview stage for each job posting.

3. **Applicants Across Multiple Jobs:** Identify people associated with more than one job posting. Email addresses are normalized to handle capitalization differences in duplicate applicant records.

4. **Recruiter Conversion Rate:** Calculate each recruiter's Final-stage conversion rate as passed interviews divided by total Final-stage interviews. Only recruiters with at least three Final-stage interviews are included.

5. **Successful Placements by Department (Bonus):** Use a window function to rank recruiters by successful Final-stage placements within each department and return the top-ranked recruiter or recruiters.


## Tests

Run the automated tests from the project root:

```powershell
python -m pytest -q
```

The tests cover API endpoints and matching-algorithm behavior.