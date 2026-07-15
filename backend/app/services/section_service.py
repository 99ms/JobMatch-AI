import re

# Common headers found in resumes
SECTION_HEADERS = [
    r"experience",
    r"work experience",
    r"employment history",
    r"professional experience",
    r"education",
    r"academic background",
    r"skills",
    r"technical skills",
    r"core competencies",
    r"projects",
    r"personal projects",
    r"summary",
    r"professional summary",
    r"objective",
    r"certifications",
    r"awards",
    r"publications"
]

def is_section_header(line: str) -> str:
    """
    Checks if a line is a likely section header.
    Returns the normalized header name if found, else None.
    """
    line = line.strip().lower()
    
    # Remove some common punctuation from the end of headers like "Experience:"
    line = re.sub(r'[:\-]$', '', line).strip()
    
    if line in [h.replace('\\', '') for h in SECTION_HEADERS]:
        return line
    return None

def parse_sections(text: str) -> dict:
    """
    Parses raw resume text into logical sections.
    Returns a dict mapping section_name -> section_text.
    """
    sections = {}
    current_section = "summary" # default starting section
    current_text = []
    
    for line in text.split('\n'):
        # Check if the line is a standalone header
        # Resumes often have headers on their own line, capitalized or otherwise distinct
        # Here we do a simple check against our known list
        
        # Heuristic: headers are usually short
        if len(line.strip()) < 40:
            header_name = is_section_header(line)
            if header_name:
                # Save previous section
                if current_text:
                    if current_section not in sections:
                        sections[current_section] = ""
                    sections[current_section] += "\n".join(current_text) + "\n"
                
                # Start new section
                current_section = header_name
                current_text = []
                continue
                
        current_text.append(line)
        
    # Save the last section
    if current_text:
        if current_section not in sections:
            sections[current_section] = ""
        sections[current_section] += "\n".join(current_text) + "\n"
        
    return sections
