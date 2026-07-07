import re

# Common words we don't want to score
STOP_WORDS = {
    "the", "a", "an", "and", "or", "for", "to", "of",
    "with", "in", "on", "at", "is", "are", "be", "as",
    "by", "from", "your", "you", "our", "we", "will",
    "looking", "developer", "engineer", "experience",
    "years", "year", "work", "ability", "skills",
    "knowledge", "team", "good", "strong", "using"
}


def tokenize(text: str) -> set[str]:
    words = re.findall(r"\b[a-zA-Z0-9+#.]+\b", text.lower())

    return {
        word
        for word in words
        if len(word) > 2 and word not in STOP_WORDS
    }


def analyze_resume(resume_text: str, job_description: str):
    resume_words = tokenize(resume_text)
    job_words = tokenize(job_description)

    matching = sorted(resume_words & job_words)
    missing = sorted(job_words - resume_words)

    score = round(
        (len(matching) / max(len(job_words), 1)) * 100,
        2
    )

    return {
        "match_score": score,
        "matching_keywords": matching,
        "missing_keywords": missing[:20]
    }