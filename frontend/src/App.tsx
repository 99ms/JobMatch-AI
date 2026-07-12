import { useState } from "react";
import { analyzeResume } from "./services/api";
import type { AnalysisResponse } from "./types/resume";
import "./App.css";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const handleAnalyze = async () => {
    if (!file) {
      alert("Please select a resume.");
      return;
    }

    if (!jobDescription.trim()) {
      alert("Please enter a job description.");
      return;
    }

    setErrorMsg("");
    try {
      setLoading(true);
      const data = await analyzeResume({ file, jobDescription });
      setResult(data);
    } catch (error: any) {
      console.error(error);
      setErrorMsg(error.message || "Analysis failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">
        <h1 className="title">JobMatch AI</h1>
        <p className="subtitle">AI Resume & Job Match Analyzer</p>

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
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the job description here..."
          />
        </div>

        {errorMsg && <div className="error">{errorMsg}</div>}

        <button onClick={handleAnalyze} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Resume"}
        </button>

        {result && (
          <div className="results">
            <div className="score-card">
              <h2>ATS Match Score</h2>
              <div className="score">{result.match_score}%</div>
              
              <div className="statistics">
                <p>Required Skills Found: {result.statistics.total_required_skills}</p>
                <p>Skills Matched: {result.statistics.total_matched_skills}</p>
                <p>Coverage: {result.statistics.coverage_percentage}%</p>
              </div>
            </div>

            <div className="structured-grid">
              <div className="keyword-box">
                <h3>✅ Matched Skills</h3>
                {result.matched_skills.length === 0 ? (
                  <p>No matches found.</p>
                ) : (
                  result.matched_skills.map((cat, idx) => (
                    <div key={idx} className="category-group">
                      <h4 className="category-title">{cat.category.toUpperCase()}</h4>
                      <ul>
                        {cat.matched_skills.map((skill) => (
                          <li key={skill}>{skill}</li>
                        ))}
                      </ul>
                    </div>
                  ))
                )}
              </div>

              <div className="keyword-box">
                <h3>❌ Missing Skills</h3>
                {result.missing_skills.length === 0 ? (
                  <p>No missing skills!</p>
                ) : (
                  result.missing_skills.map((cat, idx) => (
                    <div key={idx} className="category-group">
                      <h4 className="category-title">{cat.category.toUpperCase()}</h4>
                      <ul>
                        {cat.missing_skills.map((skill) => (
                          <li key={skill}>{skill}</li>
                        ))}
                      </ul>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;