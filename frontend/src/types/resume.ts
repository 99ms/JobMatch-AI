export interface AnalysisRequest {
  jobDescription: string;
  file: File;
}

export interface SkillCategory {
  category: string;
  weight: number;
  matched_skills: string[];
  missing_skills: string[];
}

export interface Statistics {
  total_required_skills: number;
  total_matched_skills: number;
  total_missing_skills: number;
  coverage_percentage: number;
}

export interface AnalysisResponse {
  filename: string;
  match_score: number;
  matching_keywords: string[];
  missing_keywords: string[];
  matched_skills: SkillCategory[];
  missing_skills: SkillCategory[];
  statistics: Statistics;
}
