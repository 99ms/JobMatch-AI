import { useState } from "react";
import api from "./services/api";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState<any>(null);

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
      const response = await api.post("/resume/process", formData);

      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Analysis failed.");
    }
  };

  return (
    <div
      style={{
        maxWidth: "800px",
        margin: "40px auto",
        fontFamily: "Arial",
      }}
    >
      <h1>JobMatch AI</h1>
      <p>AI Resume & Job Match Analyzer</p>

      <hr />

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

      <br />
      <br />

      {file && (
        <p>
          <strong>Selected File:</strong> {file.name}
        </p>
      )}

      <h3>Job Description</h3>

      <textarea
        rows={8}
        style={{ width: "100%" }}
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
      />

      <br />
      <br />

      <button onClick={handleAnalyze}>
        Analyze Resume
      </button>

      {result && (
        <div style={{ marginTop: "30px" }}>
          <hr />

          <h2>Analysis Results</h2>

          <p>
            <strong>Match Score:</strong>{" "}
            {result.analysis.match_score}%
          </p>

          <h3>Matching Keywords</h3>

          <ul>
            {result.analysis.matching_keywords.map((word: string) => (
              <li key={word}>{word}</li>
            ))}
          </ul>

          <h3>Missing Keywords</h3>

          <ul>
            {result.analysis.missing_keywords.map((word: string) => (
              <li key={word}>{word}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;