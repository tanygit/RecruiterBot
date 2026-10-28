
-- Question 1:
-- List all open job postings and their recruiter names.
SELECT
    jp.id AS job_posting_id,
    jp.title,
    jp.department,
    jp.opened_date,
    r.name AS recruiter_name
FROM job_postings AS jp
JOIN recruiters AS r
    ON jp.recruiter_id = r.id
WHERE jp.status = 'open'
ORDER BY jp.opened_date, jp.id;


-- Question 2:
-- For every job posting, count distinct applicants who reached Final.
SELECT
    jp.id AS job_posting_id,
    jp.title,
    COUNT(DISTINCT i.applicant_id) AS final_stage_applicants
FROM job_postings AS jp
LEFT JOIN interviews AS i
    ON jp.id = i.job_posting_id
   AND i.stage = 'Final'
GROUP BY jp.id, jp.title
ORDER BY jp.id;


-- Question 3:
-- Find people associated with more than one job posting.
-- Normalize email casing and whitespace to identify duplicate applicant records.
-- Interviews are used as evidence of a job-posting association because
-- the supplied schema does not contain a separate applications table.
SELECT
    LOWER(TRIM(a.email)) AS normalized_email,
    MAX(a.full_name) AS person_name,
    COUNT(DISTINCT i.job_posting_id) AS distinct_job_postings
FROM applicants AS a
JOIN interviews AS i
    ON i.applicant_id = a.id
WHERE a.email IS NOT NULL
GROUP BY LOWER(TRIM(a.email))
HAVING COUNT(DISTINCT i.job_posting_id) > 1
ORDER BY normalized_email;


-- Question 4:
-- Final-stage conversion rate by recruiter.
-- Include only recruiters with at least three Final-stage interviews.
SELECT
    r.id AS recruiter_id,
    r.name AS recruiter_name,
    COUNT(*) AS total_final_interviews,
    SUM(
        CASE WHEN i.outcome = 'passed' THEN 1 ELSE 0 END
    ) AS passed_final_interviews,
    ROUND(
        100.0 * SUM(
            CASE WHEN i.outcome = 'passed' THEN 1 ELSE 0 END
        ) / COUNT(*),
        2
    ) AS conversion_rate_percent
FROM recruiters AS r
JOIN job_postings AS jp
    ON jp.recruiter_id = r.id
JOIN interviews AS i
    ON i.job_posting_id = jp.id
WHERE i.stage = 'Final'
GROUP BY r.id, r.name
HAVING COUNT(*) >= 3
ORDER BY conversion_rate_percent DESC, r.name;


-- Question 5 (Bonus):
-- Find the recruiter(s) with the most passed Final interviews
-- in each department using a window function.
WITH recruiter_placements AS (
    SELECT
        jp.department,
        r.id AS recruiter_id,
        r.name AS recruiter_name,
        COUNT(*) AS successful_placements
    FROM job_postings AS jp
    JOIN recruiters AS r
        ON jp.recruiter_id = r.id
    JOIN interviews AS i
        ON i.job_posting_id = jp.id
    WHERE i.stage = 'Final'
      AND i.outcome = 'passed'
    GROUP BY jp.department, r.id, r.name
),
ranked_placements AS (
    SELECT
        department,
        recruiter_id,
        recruiter_name,
        successful_placements,
        RANK() OVER (
            PARTITION BY department
            ORDER BY successful_placements DESC
        ) AS placement_rank
    FROM recruiter_placements
)
SELECT
    department,
    recruiter_id,
    recruiter_name,
    successful_placements
FROM ranked_placements
WHERE placement_rank = 1
ORDER BY department;
