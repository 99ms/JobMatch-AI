export interface AnalysisRequest {
  jobDescription: string;
  file: File;
}

export interface SkillCategory {
  category: string;
  weight: number;
  matched_skills: string[];
  missing_skills: string[];
  points_earned: number;
  points_possible: number;
}

export interface Statistics {
  total_required_skills: number;
  total_matched_skills: number;
  total_missing_skills: number;
  coverage_percentage: number;
  total_points_earned: number;
  total_points_possible: number;
}

export interface SectionMatch {
  section_name: string;
  matched_skills: string[];
}

export interface AnalysisResponse {
  filename: string;
  match_score: number;
  matching_keywords: string[];
  missing_keywords: string[];
  matched_skills: SkillCategory[];
  missing_skills: SkillCategory[];
  statistics: Statistics;
  sections: SectionMatch[];
}
