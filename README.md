# JobMatch AI

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

### AI-powered Resume Screening & ATS Analysis Platform

JobMatch AI is a full-stack web application that evaluates resumes against job descriptions and provides ATS compatibility scores, missing skill analysis, keyword matching, and actionable recommendations to help job seekers optimize their resumes before applying.

---

##  Features

- Upload resumes in PDF format
- Compare resumes against any job description
- Generate ATS compatibility scores
- Identify matching and missing skills
- Detect missing keywords
- Receive actionable resume improvement suggestions
- FastAPI REST API backend
- Modern React + TypeScript frontend

---

## 🛠 Tech Stack

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
- Custom ATS scoring algorithm

---

## 📁 Project Structure

```text
JobMatch-AI/
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
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm

---

### Clone the Repository

```bash
git clone https://github.com/99ms/JobMatch-AI.git
cd JobMatch-AI
```

---

## ⚙ Backend Setup

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

Backend:

```
http://127.0.0.1:8000
```

---

## 💻 Frontend Setup

Open a second terminal.

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```
http://localhost:5173
```

---

## 🔌 API

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/analyze` | Analyze a resume against a job description |

---

## ⚙ How It Works

1. Upload a resume in PDF format.
2. Paste or enter a job description.
3. The backend extracts text from the uploaded PDF.
4. The resume is analyzed against the job description.
5. ATS compatibility, keyword matching, and missing skills are calculated.
6. Results are returned to the React frontend for visualization.

---

## 📷 Screenshots

> Screenshots coming soon.

---

## 🚀 Future Improvements

- AI-generated resume rewriting
- Semantic similarity using sentence embeddings
- DOCX resume support
- Resume history
- User authentication
- Recruiter dashboard
- Cover letter generation
- Saved job descriptions
- Export analysis as PDF

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Arsh Zayd**

GitHub: https://github.com/99ms

---
