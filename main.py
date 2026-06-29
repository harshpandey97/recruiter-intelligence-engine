import os
import json
import re
from groq import Groq

# ── Configuration ────────────────────────────────────────────────────────────
API_KEY = os.getenv("GROQ_API_KEY", "YOUR_GROQ_KEY_HERE")
client  = Groq(api_key=API_KEY)
MODEL   = "llama-3.3-70b-versatile"

# ── Job Description ──────────────────────────────────────────────────────────
JD = """
Position: Data Analyst (Fresher/Intern)
Requirements: Python, SQL, Power BI, Excel, pandas, numpy, statistics
Bonus: Machine learning, Google Analytics
"""

# ── Sample Candidates (add more or load from files) ──────────────────────────
CANDIDATES = [
    {
        "name": "Priya Sharma",
        "resume": (
            "BCA Graduate. Skills: Python, SQL, Power BI, Excel, pandas. "
            "Projects: Sales Dashboard, Customer Segmentation. "
            "Certifications: Google Data Analytics, NASSCOM AI. "
            "Internship: 3 months data analyst."
        ),
    },
    {
        "name": "Rahul Verma",
        "resume": (
            "B.Tech CSE. Skills: Java, C++, Python basic. "
            "Projects: Android app. No data analytics experience."
        ),
    },
    {
        "name": "Anjali Singh",
        "resume": (
            "BCA Graduate. Skills: Excel, SQL, Power BI, Google Analytics, Python, pandas. "
            "Projects: HR Analytics Dashboard, E-commerce Analysis. "
            "Certifications: Power BI, Tutedude. Forage: BCG, JP Morgan."
        ),
    },
]

# ── Scoring Engine ────────────────────────────────────────────────────────────
def score_candidate(candidate: dict) -> dict:
    prompt = f"""You are an expert recruiter. Evaluate the candidate against the Job Description.

JD: {JD}
Candidate: {candidate['name']}
Resume: {candidate['resume']}

Return ONLY valid JSON, no markdown, no explanation:
{{"name": "{candidate['name']}", "score": 85, "recommendation": "Recommend", "matched_skills": ["Python", "SQL"], "missing_skills": ["numpy"], "summary": "One sentence summary"}}"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
    )
    raw    = re.sub(r"```json|```", "", response.choices[0].message.content).strip()
    return json.loads(raw)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("\nAnalyzing candidates...\n")
    results = []

    for c in CANDIDATES:
        result = score_candidate(c)
        results.append(result)
        print(f"✅ Scored: {result['name']} — {result['score']}/100")

    results.sort(key=lambda x: x["score"], reverse=True)

    print("\n" + "=" * 55)
    print("   RECRUITER INTELLIGENCE ENGINE — RESULTS")
    print("=" * 55)

    for i, r in enumerate(results, 1):
        print(f"\n#{i} {r['name']}")
        print(f"   Score      : {r['score']}/100")
        print(f"   Decision   : {r['recommendation']}")
        print(f"   Matched    : {', '.join(r['matched_skills'])}")
        print(f"   Missing    : {', '.join(r['missing_skills'])}")
        print(f"   Summary    : {r['summary']}")

    print(f"\n🏆 Top Candidate: {results[0]['name']} ({results[0]['score']}/100)")
    print("=" * 55)

    # Save results
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\n📁 Results saved to results.json")


if __name__ == "__main__":
    main()
