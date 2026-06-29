"""
Recruiter Intelligence Engine
AI-powered candidate ranking system using Claude API
"""

import anthropic
import json
import re
import sys
from pathlib import Path

# Try importing PDF support (optional)
try:
    import pdfplumber
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False


# ─────────────────────────────────────────────
# PDF PARSER
# ─────────────────────────────────────────────

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF resume."""
    if not PDF_SUPPORT:
        raise ImportError("pdfplumber not installed. Run: pip install pdfplumber")
    
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()


# ─────────────────────────────────────────────
# CLAUDE API — SCORE A SINGLE CANDIDATE
# ─────────────────────────────────────────────

def score_candidate(client: anthropic.Anthropic, jd: str, resume: str, candidate_name: str) -> dict:
    """
    Send JD + resume to Claude. Returns structured JSON with scores.
    """
    prompt = f"""
You are an expert technical recruiter. Evaluate the candidate's resume against the job description below.

JOB DESCRIPTION:
{jd}

CANDIDATE RESUME ({candidate_name}):
{resume}

Return ONLY a valid JSON object (no markdown, no explanation) with this exact structure:
{{
  "candidate_name": "{candidate_name}",
  "overall_score": <integer 0-100>,
  "skill_match_score": <integer 0-100>,
  "experience_score": <integer 0-100>,
  "education_score": <integer 0-100>,
  "matched_skills": [<list of skills from JD that candidate has>],
  "missing_skills": [<list of skills from JD that candidate lacks>],
  "strengths": [<2-3 key strengths>],
  "weaknesses": [<2-3 key gaps>],
  "recommendation": "<Strongly Recommend | Recommend | Consider | Reject>",
  "summary": "<2-sentence recruiter summary>"
}}
"""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()

    # Strip markdown fences if present
    raw = re.sub(r"```json|```", "", raw).strip()

    return json.loads(raw)


# ─────────────────────────────────────────────
# RANK ALL CANDIDATES
# ─────────────────────────────────────────────

def rank_candidates(results: list[dict]) -> list[dict]:
    """Sort candidates by overall_score descending."""
    return sorted(results, key=lambda x: x.get("overall_score", 0), reverse=True)


# ─────────────────────────────────────────────
# DISPLAY RESULTS
# ─────────────────────────────────────────────

def display_results(ranked: list[dict]):
    """Print a clean recruiter-friendly report."""
    print("\n" + "=" * 65)
    print("  RECRUITER INTELLIGENCE ENGINE — CANDIDATE RANKING REPORT")
    print("=" * 65)

    for idx, r in enumerate(ranked, 1):
        rec_color = {
            "Strongly Recommend": "✅",
            "Recommend": "🟢",
            "Consider": "🟡",
            "Reject": "🔴"
        }.get(r.get("recommendation", ""), "⚪")

        print(f"\n#{idx}  {r['candidate_name']}")
        print(f"    Overall Score   : {r['overall_score']}/100")
        print(f"    Skill Match     : {r['skill_match_score']}/100")
        print(f"    Experience      : {r['experience_score']}/100")
        print(f"    Education       : {r['education_score']}/100")
        print(f"    Recommendation  : {rec_color} {r['recommendation']}")
        print(f"    Matched Skills  : {', '.join(r['matched_skills']) or 'None'}")
        print(f"    Missing Skills  : {', '.join(r['missing_skills']) or 'None'}")
        print(f"    Strengths       : {' | '.join(r['strengths'])}")
        print(f"    Weaknesses      : {' | '.join(r['weaknesses'])}")
        print(f"    Summary         : {r['summary']}")
        print("    " + "-" * 55)

    print("\n🏆  Top Candidate:", ranked[0]["candidate_name"], f"({ranked[0]['overall_score']}/100)")
    print("=" * 65 + "\n")


# ─────────────────────────────────────────────
# DEMO DATA
# ─────────────────────────────────────────────

SAMPLE_JD = """
Position: Data Analyst (Fresher/Intern)
Company: TechCorp India, Delhi NCR

Requirements:
- Proficiency in Python and SQL
- Experience with data visualization tools (Power BI / Tableau)
- Knowledge of Excel (pivot tables, VLOOKUP, dashboards)
- Understanding of statistics and data cleaning
- Familiarity with pandas, numpy
- Good communication skills
- Bonus: Machine learning basics, Google Analytics
"""

SAMPLE_CANDIDATES = [
    {
        "name": "Priya Sharma",
        "resume": """
        BCA Graduate, 2024 — Delhi University
        Skills: Python, SQL, Power BI, Excel, pandas, numpy, Tableau
        Projects: Sales Dashboard in Power BI, Customer Segmentation using K-Means
        Certifications: Google Data Analytics, NASSCOM AI for All
        Internship: 3-month data analyst intern at StartupXYZ — built automated Excel reports
        Communication: Presented insights to management team of 10+
        """
    },
    {
        "name": "Rahul Verma",
        "resume": """
        B.Tech CSE Graduate, 2023 — Amity University
        Skills: Java, C++, Python (basic), some SQL
        Projects: College management system in Java, Android app
        Certifications: Oracle Java Certified
        No data analytics experience. Interested in switching to data field.
        """
    },
    {
        "name": "Anjali Singh",
        "resume": """
        BCA Graduate, 2024 — IP University
        Skills: Excel (advanced), SQL, Power BI, Google Analytics, Python (pandas, matplotlib)
        Projects: HR Analytics Dashboard, E-commerce Sales Analysis
        Certifications: Microsoft Power BI Desktop, Tutedude Data Analytics
        Forage Simulations: BCG Data Science, JP Morgan Excel Skills
        Strong presentation and communication skills.
        """
    }
]


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    print("\n🚀  Starting Recruiter Intelligence Engine...")
    print("    Connecting to Claude API...\n")

    client = anthropic.Anthropic()  # Reads ANTHROPIC_API_KEY from env

    # ── Load JD ──────────────────────────────
    jd_path = Path("job_description.txt")
    if jd_path.exists():
        jd = jd_path.read_text()
        print(f"📄  Loaded JD from {jd_path}")
    else:
        jd = SAMPLE_JD
        print("📄  Using sample Job Description (create job_description.txt to use your own)")

    # ── Load Candidates ───────────────────────
    resumes_dir = Path("resumes")
    candidates = []

    if resumes_dir.exists() and any(resumes_dir.glob("*.pdf")):
        for pdf_file in sorted(resumes_dir.glob("*.pdf")):
            text = extract_text_from_pdf(str(pdf_file))
            candidates.append({"name": pdf_file.stem.replace("_", " ").title(), "resume": text})
        print(f"📁  Loaded {len(candidates)} PDF resume(s) from /resumes folder\n")
    else:
        candidates = SAMPLE_CANDIDATES
        print("📁  Using 3 sample candidates (add PDFs to /resumes folder to use your own)\n")

    # ── Score Each Candidate ──────────────────
    results = []
    for c in candidates:
        print(f"    Analyzing {c['name']}...", end=" ", flush=True)
        try:
            result = score_candidate(client, jd, c["resume"], c["name"])
            results.append(result)
            print(f"✅  Score: {result['overall_score']}/100")
        except Exception as e:
            print(f"❌  Error: {e}")

    if not results:
        print("\nNo candidates scored successfully. Check your API key and inputs.")
        sys.exit(1)

    # ── Rank & Display ────────────────────────
    ranked = rank_candidates(results)
    display_results(ranked)

    # ── Save JSON Output ──────────────────────
    output_path = Path("results.json")
    with open(output_path, "w") as f:
        json.dump(ranked, f, indent=2)
    print(f"💾  Full results saved to {output_path}\n")


if __name__ == "__main__":
    main()
