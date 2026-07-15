from app.services.section_service import parse_sections, is_section_header

def test_is_section_header():
    assert is_section_header("Experience") == "experience"
    assert is_section_header("WORK EXPERIENCE:") == "work experience"
    assert is_section_header("Education-") == "education"
    assert is_section_header("  SKILLS  ") == "skills"
    assert is_section_header("Projects") == "projects"
    
    # Negative cases
    assert is_section_header("I have 5 years of experience") is None
    assert is_section_header("High School Education") is None
    assert is_section_header("Skills include Python, Java") is None

def test_parse_sections_standard():
    resume_text = """
    John Doe
    Software Engineer

    SUMMARY
    I am a great engineer.

    EXPERIENCE
    Google
    Software Engineer 2020-Present
    Did some cool stuff.

    EDUCATION
    MIT
    B.S. Computer Science

    SKILLS
    Python, React, TypeScript
    """
    
    sections = parse_sections(resume_text)
    
    assert "summary" in sections
    assert "I am a great engineer." in sections["summary"]
    
    assert "experience" in sections
    assert "Google" in sections["experience"]
    
    assert "education" in sections
    assert "MIT" in sections["education"]
    
    assert "skills" in sections
    assert "Python, React, TypeScript" in sections["skills"]

def test_parse_sections_no_headers():
    # If no recognized headers, everything should go to 'summary'
    resume_text = """
    John Doe
    Software Engineer
    I worked at Google.
    I studied at MIT.
    My tools are Python and React.
    """
    sections = parse_sections(resume_text)
    assert len(sections) == 1
    assert "summary" in sections
    assert "I worked at Google." in sections["summary"]

def test_parse_sections_multiple_same_headers():
    # It should concatenate them or overwrite?
    # Our implementation concatenates because if the same header is hit, it appends to it.
    resume_text = """
    EXPERIENCE
    Job 1
    EXPERIENCE
    Job 2
    """
    sections = parse_sections(resume_text)
    assert "experience" in sections
    assert "Job 1" in sections["experience"]
    assert "Job 2" in sections["experience"]
