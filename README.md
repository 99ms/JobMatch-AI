# JobMatch AI
![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-009688)
![React](https://img.shields.io/badge/React-61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6)
![License](https://img.shields.io/badge/License-MIT-green)
AI-powered ATS Resume Analyzer

JobMatch AI is a full-stack ATS resume analyzer that evaluates resumes against job descriptions and provides detailed compatibility scores, missing skill analysis, keyword matching, and actionable recommendations to help job seekers improve their resumes.
---

## Features

- Upload resumes in PDF format
- Analyze resumes against custom job descriptions
- Generate an ATS compatibility score
- Identify matching and missing skills
- Highlight keyword gaps
- Provide suggestions to improve resume relevance
- Modern React-based user interface
- RESTful API built with FastAPI

---

## Tech Stack

### Frontend

- React
- TypeScript
- Vite
- CSS

### Backend

- FastAPI
- Python
- Pydantic

### Resume Processing

- PDF text extraction
- Regular expressions
- NLP-inspired keyword matching
- Custom scoring algorithm

---

## Project Structure

```
resume-analyzer/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
└── README.md
```

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/99ms/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

---

## Backend Setup

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

The backend will run on:

```
http://127.0.0.1:8000
```

---

## Frontend Setup

Open a second terminal.

```bash
cd frontend

npm install

npm run dev
```

The frontend will run on:

```
http://localhost:5173
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/analyze` | Analyze a resume against a job description |

---

## How It Works

1. Upload a resume in PDF format.
2. Enter a target job description.
3. The backend extracts text from the uploaded resume.
4. Resume content is compared against the job description.
5. Matching keywords, missing skills, and ATS compatibility are calculated.
6. The frontend presents a structured report with recommendations.

---

## Future Improvements

- AI-generated resume recommendations
- Semantic similarity using sentence embeddings
- Multi-page resume optimization
- Support for DOCX resumes
- Resume history and saved analyses
- User authentication
- Recruiter dashboard

---

## License

This project is licensed under the MIT License.

---

## Author

**Arsh Zayd**

GitHub: https://github.com/99ms
