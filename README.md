# 🤖 Recruiter Intelligence Engine

> AI-powered candidate ranking system using Python and Claude API to automate resume screening and scoring.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Claude API](https://img.shields.io/badge/Claude-API-orange)](https://anthropic.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📌 What It Does

Paste a **Job Description** + candidate resumes → get an **AI-ranked shortlist** with scores, skill gaps, and recruiter recommendations — in seconds.

No manual screening. No bias. Just data.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🧠 AI Scoring | Claude API scores each candidate on skill match, experience & education |
| 📄 PDF Support | Automatically parses PDF resumes from a `/resumes` folder |
| 📊 Multi-Criteria Ranking | Overall score, skill match %, strengths, weaknesses |
| 🎯 JD Skill Matching | Identifies matched and missing skills vs the Job Description |
| 💡 Recruiter Recommendation | Strongly Recommend / Recommend / Consider / Reject |
| 💾 JSON Export | Full results saved to `results.json` for further analysis |

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/HARSHPANDEY9756/recruiter-intelligence-engine.git
cd recruiter-intelligence-engine
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your Anthropic API key
```bash
# Windows
set ANTHROPIC_API_KEY=your_api_key_here

# Mac/Linux
export ANTHROPIC_API_KEY=your_api_key_here
```

### 4. Run with sample data
```bash
python main.py
```

---

## 📁 Project Structure

```
recruiter-intelligence-engine/
│
├── main.py                  # Core engine — scoring + ranking logic
├── requirements.txt         # Dependencies
├── job_description.txt      # (Optional) Your custom JD
├── resumes/                 # (Optional) Drop PDF resumes here
│   ├── candidate1.pdf
│   └── candidate2.pdf
└── results.json             # Auto-generated ranked output
```

---

## 🔧 Use With Your Own Data

**Custom Job Description:**
Create a `job_description.txt` file in the project root — the engine will auto-detect and use it.

**Real Resumes (PDF):**
Create a `/resumes` folder and drop `.pdf` files in it. The engine parses them automatically.

```bash
mkdir resumes
# copy your PDFs into it
python main.py
```

---

## 📊 Sample Output

```
=================================================================
  RECRUITER INTELLIGENCE ENGINE — CANDIDATE RANKING REPORT
=================================================================

#1  Anjali Singh
    Overall Score   : 91/100
    Skill Match     : 95/100
    Experience      : 85/100
    Education       : 90/100
    Recommendation  : ✅ Strongly Recommend
    Matched Skills  : Python, SQL, Power BI, Excel, Google Analytics
    Missing Skills  : None
    Strengths       : Strong portfolio | Relevant certifications | JD alignment
    Summary         : Anjali demonstrates strong alignment with the role...

#2  Priya Sharma
    Overall Score   : 82/100
    ...

🏆  Top Candidate: Anjali Singh (91/100)
=================================================================
```

---

## 🛠 Tech Stack

- **Python 3.10+**
- **Anthropic Claude API** (`claude-opus-4-6`) — for AI-powered evaluation
- **pdfplumber** — for PDF resume parsing
- **JSON** — for structured output

---

## 💡 How It Works

```
Job Description  ──┐
                   ├──▶  Claude API  ──▶  JSON Score  ──▶  Ranked Output
Resume Text      ──┘
```

1. JD and resume are sent to Claude with a structured prompt
2. Claude returns scores across 4 dimensions
3. All candidates are ranked by overall score
4. Results are displayed and saved to `results.json`

---

## 🔮 Future Scope

- [ ] Web UI with Flask/Streamlit
- [ ] Batch processing from Google Sheets
- [ ] Email shortlist to hiring manager
- [ ] ATS (Applicant Tracking System) integration
- [ ] DOCX resume support

---

## 👤 Author

**Harsh Pandey**
BCA Graduate | Aspiring Data Analyst
📍 New Delhi, India
🔗 [LinkedIn](https://linkedin.com/in/harsh-pandey) | [GitHub](https://github.com/HARSHPANDEY9756)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
