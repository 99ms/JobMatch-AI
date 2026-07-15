from app.services.analysis_service import analyze_resume, extract_skills_by_category, calculate_weighted_score

def test_empty_resume():
    job_desc = "Looking for a Python and React developer."
    resume = ""
    result = analyze_resume(resume, job_desc)
    
    assert result["match_score"] == 0.0
    assert result["statistics"]["total_matched_skills"] == 0
    assert result["statistics"]["total_required_skills"] > 0
    assert len(result["sections"]) == 0

def test_empty_job_description():
    job_desc = ""
    resume = "I am a Python and React developer."
    result = analyze_resume(resume, job_desc)
    
    assert result["match_score"] == 0.0
    assert result["statistics"]["total_required_skills"] == 0
    assert result["statistics"]["total_matched_skills"] == 0
    # Sections might be parsed, but since there are no required skills, matched_skills in sections should be empty
    assert len(result["sections"]) == 0

def test_unknown_skills():
    job_desc = "Looking for a developer with SomeMadeUpSkill and AnotherFakeSkill."
    resume = "I have SomeMadeUpSkill and AnotherFakeSkill."
    result = analyze_resume(resume, job_desc)
    
    # Since these skills aren't in SKILLS_DB, they shouldn't be matched
    assert result["statistics"]["total_required_skills"] == 0
    assert result["statistics"]["total_matched_skills"] == 0

def test_alias_matching():
    job_desc = "Looking for a ReactJS developer."
    resume = "I am a React developer."
    result = analyze_resume(resume, job_desc)
    
    assert "react" in [s for cat in result["matched_skills"] for s in cat["matched_skills"]]
    assert result["statistics"]["total_matched_skills"] == 1

def test_duplicate_skills():
    job_desc = "Python Python Python"
    resume = "Python is great. I love Python."
    result = analyze_resume(resume, job_desc)
    
    # Sets should deduplicate
    assert result["statistics"]["total_required_skills"] == 1
    assert result["statistics"]["total_matched_skills"] == 1

def test_mixed_capitalization():
    job_desc = "Looking for pYtHoN and ReAcT"
    resume = "I know PYTHON and react"
    result = analyze_resume(resume, job_desc)
    
    assert result["statistics"]["total_matched_skills"] == 2

def test_explainable_scoring():
    job_desc = "React and Python"
    resume = "React and Python"
    result = analyze_resume(resume, job_desc)
    
    assert result["statistics"]["total_points_earned"] > 0
    assert result["statistics"]["total_points_possible"] == result["statistics"]["total_points_earned"]
    assert result["match_score"] == 100.0  # 3/6 = 50%

def test_section_skill_mapping():
    job_desc = "Looking for a Python and React developer."
    resume = """
    EXPERIENCE
    Worked with Python for 5 years.
    
    SKILLS
    React, Java.
    """
    result = analyze_resume(resume, job_desc)
    
    # Check sections array
    sections = result["sections"]
    assert len(sections) == 2
    
    exp_sec = next(s for s in sections if s["section_name"] == "experience")
    assert "python" in exp_sec["matched_skills"]
    assert "react" not in exp_sec["matched_skills"]
    
    skill_sec = next(s for s in sections if s["section_name"] == "skills")
    assert "react" in skill_sec["matched_skills"]
    assert "python" not in skill_sec["matched_skills"]
