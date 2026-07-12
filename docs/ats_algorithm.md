# ATS Engine Algorithm (v2)

This document describes the inner workings of the structured ATS scoring engine. The goal of this engine is to provide deterministic, predictable, and heavily weighted scoring for technical skills extracted from resumes.

## 1. Skill Dictionary
The core of the engine is `skills.json`. It maps technical skills into logical categories:
- **Languages** (Weight: 3)
- **Frameworks** (Weight: 3)
- **Databases** (Weight: 2)
- **Cloud** (Weight: 2)
- **Tools** (Weight: 1)

Each skill inside a category can optionally define an individual weight (defaulting to 1 if not specified) and an array of aliases to help capture standard variations (e.g. `React`, `React.js`, `ReactJS`).

## 2. Text Normalization
When parsing text (either the Job Description or the Resume):
1. The text is lowercased.
2. All non-alphanumeric characters (excluding `+`, `.`, `#`) are converted into whitespace.
3. Multiple whitespaces are collapsed.
4. The string is padded with spaces to allow strict exact-word matching (avoiding substring false-positives like matching "java" inside "javascript").

## 3. Alias Matching
The engine iterates through the dictionary. If any of a skill's aliases are found in the normalized text, the canonical `name` of the skill is registered as "found".

## 4. Scoring Mechanism
The ATS score calculates how well a candidate matches the *required* skills found in the Job Description.

For every required skill found in the job description:
- `Points Possible += (Category Weight * Individual Skill Weight)`
- If the candidate's resume also contains the skill:
  - `Points Earned += (Category Weight * Individual Skill Weight)`

The final score is `(Points Earned / Points Possible) * 100`, bounded to two decimal places.

## 5. Structured Return
The engine calculates both the legacy flat lists and a new structured representation that groups missing/matched skills into their native categories. It also provides basic statistics:
- `total_required_skills`
- `total_matched_skills`
- `total_missing_skills`
- `coverage_percentage`
