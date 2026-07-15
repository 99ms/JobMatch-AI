import re
import json
import os
from pathlib import Path
from .section_service import parse_sections

# Load skills database
SKILLS_FILE = Path(__file__).parent.parent / "core" / "skills.json"

def load_skills_db():
    if not SKILLS_FILE.exists():
        return {}
    with open(SKILLS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

SKILLS_DB = load_skills_db()

def normalize_text(text: str) -> str:
    """Normalizes text by lowercasing and standardizing spacing."""
    # Convert to lowercase
    text = text.lower()
    # Replace non-alphanumeric characters (except + and . for c++, node.js) with spaces
    text = re.sub(r'[^a-z0-9\+\.#]', ' ', text)
    # Standardize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return f" {text} " # Pad with spaces for exact word matching

def find_skills_in_text(normalized_text: str, category_data: dict) -> set:
    """Finds all canonical skills present in the text based on aliases."""
    found_skills = set()
    for skill_obj in category_data.get("skills", []):
        canonical_name = skill_obj["name"]
        for alias in skill_obj.get("aliases", []):
            # Check for exact word match using padded spaces
            if f" {alias.lower()} " in normalized_text:
                found_skills.add(canonical_name)
                break # Move to next skill once one alias is found
    return found_skills

def extract_skills_by_category(text: str) -> dict:
    """Extracts skills from text and groups them by category."""
    normalized_text = normalize_text(text)
    extracted = {}
    
    for category, data in SKILLS_DB.items():
        found = find_skills_in_text(normalized_text, data)
        if found:
            extracted[category] = found
            
    return extracted

def calculate_weighted_score(matched_categories: dict, missing_categories: dict) -> tuple[float, float, float, dict]:
    """Calculates the ATS match score based on individual skill weights and category weights."""
    total_points_earned = 0.0
    total_points_possible = 0.0
    category_points = {}
    
    for category, data in SKILLS_DB.items():
        cat_weight = data.get("category_weight", 1)
        
        matched_set = matched_categories.get(category, set())
        missing_set = missing_categories.get(category, set())
        
        cat_earned = 0.0
        cat_possible = 0.0
        
        for skill_obj in data.get("skills", []):
            name = skill_obj["name"]
            skill_weight = skill_obj.get("weight", 1)
            
            # The total weight of a skill is its individual weight * category weight
            point_value = skill_weight * cat_weight
            
            if name in matched_set or name in missing_set:
                cat_possible += point_value
                total_points_possible += point_value
                if name in matched_set:
                    cat_earned += point_value
                    total_points_earned += point_value
                    
        category_points[category] = {
            "earned": cat_earned,
            "possible": cat_possible
        }
                    
    if total_points_possible == 0:
        return 0.0, 0.0, 0.0, category_points
        
    score = round((total_points_earned / total_points_possible) * 100, 2)
    return score, total_points_earned, total_points_possible, category_points

def analyze_resume(resume_text: str, job_description: str) -> dict:
    """Orchestrates the ATS scoring process."""
    resume_skills_grouped = extract_skills_by_category(resume_text)
    job_skills_grouped = extract_skills_by_category(job_description)
    
    matched_structured = {}
    missing_structured = {}
    
    flat_matched = set()
    flat_missing = set()
    
    total_req = 0
    total_matched = 0
    total_missing = 0
    
    # Compute intersections and differences per category
    for category, data in SKILLS_DB.items():
        job_set = job_skills_grouped.get(category, set())
        if not job_set:
            continue
            
        resume_set = resume_skills_grouped.get(category, set())
        
        matched = job_set & resume_set
        missing = job_set - resume_set
        
        matched_structured[category] = sorted(list(matched))
        missing_structured[category] = sorted(list(missing))
        
        flat_matched.update(matched)
        flat_missing.update(missing)
        
        total_req += len(job_set)
        total_matched += len(matched)
        total_missing += len(missing)

    score, total_earned, total_possible, cat_points = calculate_weighted_score(matched_structured, missing_structured)
    coverage = round((total_matched / max(total_req, 1)) * 100, 2)
    
    # Process sections
    sections_dict = parse_sections(resume_text)
    sections_list = []
    
    for sec_name, sec_text in sections_dict.items():
        sec_skills_grouped = extract_skills_by_category(sec_text)
        sec_matched = []
        # Only include skills that are actually in the job description (matched skills)
        for category, sec_set in sec_skills_grouped.items():
            job_set = job_skills_grouped.get(category, set())
            valid_matches = sec_set & job_set
            sec_matched.extend(list(valid_matches))
            
        if sec_matched:
            sections_list.append({
                "section_name": sec_name,
                "matched_skills": sorted(sec_matched)
            })
    
    # Format for response
    matched_list = []
    missing_list = []
    
    for category, data in SKILLS_DB.items():
        if category in matched_structured or category in missing_structured:
            m_skills = matched_structured.get(category, [])
            miss_skills = missing_structured.get(category, [])
            
            c_points = cat_points.get(category, {"earned": 0.0, "possible": 0.0})
            
            if m_skills or miss_skills:
                cat_obj = {
                    "category": category,
                    "weight": data.get("category_weight", 1),
                    "matched_skills": m_skills,
                    "missing_skills": miss_skills,
                    "points_earned": c_points["earned"],
                    "points_possible": c_points["possible"]
                }
                
                if m_skills:
                    matched_list.append(cat_obj)
                if miss_skills:
                    missing_list.append(cat_obj)

    return {
        "match_score": score,
        "matching_keywords": sorted(list(flat_matched)),
        "missing_keywords": sorted(list(flat_missing)),
        "matched_skills": matched_list,
        "missing_skills": missing_list,
        "statistics": {
            "total_required_skills": total_req,
            "total_matched_skills": total_matched,
            "total_missing_skills": total_missing,
            "coverage_percentage": coverage,
            "total_points_earned": total_earned,
            "total_points_possible": total_possible
        },
        "sections": sections_list
    }