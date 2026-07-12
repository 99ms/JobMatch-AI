import type { AnalysisRequest, AnalysisResponse } from "../types/resume";

const API_BASE_URL = 'http://127.0.0.1:8000';

export const analyzeResume = async (request: AnalysisRequest): Promise<AnalysisResponse> => {
  const formData = new FormData();
  formData.append('file', request.file);
  formData.append('job_description', request.jobDescription);

  const response = await fetch(`${API_BASE_URL}/resume/analyze`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'An error occurred during analysis');
  }

  return response.json();
};