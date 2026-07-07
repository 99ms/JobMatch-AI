import { useState } from "react";
import api from "./services/api";
import "./App.css";

interface AnalysisResult {
  filename: string;
  pages: number;
  analysis: {
    match_score: number;
    matching_keywords: string[];
    missing_keywords: string[];
  };
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!file) {
      alert("Please select a resume.");
      return;
    }

    if (!jobDescription.trim()) {
      alert("Please enter a job description.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_description", jobDescription);

    try {
      setLoading(true);

      const response = await api.post<AnalysisResult>(
        "/resume/process",
        formData
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Analysis failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">

        <h1 className="title">JobMatch AI</h1>
        <p className="subtitle">
          AI Resume & Job Match Analyzer
        </p>

        <div className="section">
          <h3>Upload Resume</h3>

          <input
            type="file"
            accept=".pdf"
            onChange={(e) => {
              if (e.target.files) {
                setFile(e.target.files[0]);
              }
            }}
          />

          {file && (
            <p>
              <strong>Selected:</strong> {file.name}
            </p>
          )}
        </div>

        <div className="section">
          <h3>Job Description</h3>

          <textarea
            value={jobDescription}
            onChange={(e) =>
              setJobDescription(e.target.value)
            }
            placeholder="Paste the job description here..."
          />
        </div>

        <button
          onClick={handleAnalyze}
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Analyze Resume"}
        </button>

        {result && (
          <div className="results">

            <div className="score-card">
              <h2>Match Score</h2>

              <div className="score">
                {result.analysis.match_score}%
              </div>
            </div>

            <div className="keyword-grid">

              <div className="keyword-box">
                <h3>✅ Matching Skills</h3>

                <ul>
                  {result.analysis.matching_keywords.map(
                    (skill) => (
                      <li key={skill}>{skill}</li>
                    )
                  )}
                </ul>
              </div>

              <div className="keyword-box">
                <h3>❌ Missing Skills</h3>

                <ul>
                  {result.analysis.missing_keywords.map(
                    (skill) => (
                      <li key={skill}>{skill}</li>
                    )
                  )}
                </ul>
              </div>

            </div>

          </div>
        )}

      </div>
    </div>
  );
}

export default App;