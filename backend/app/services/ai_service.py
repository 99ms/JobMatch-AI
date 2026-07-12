class AIService:
    @staticmethod
    def generate_resume_feedback(resume_text: str, job_description: str):
        raise NotImplementedError("AI feedback generation not yet implemented")

    @staticmethod
    def tailor_resume(resume_text: str, job_description: str):
        raise NotImplementedError("Resume tailoring not yet implemented")

    @staticmethod
    def generate_cover_letter(resume_text: str, job_description: str):
        raise NotImplementedError("Cover letter generation not yet implemented")

    @staticmethod
    def generate_interview_questions(resume_text: str, job_description: str):
        raise NotImplementedError("Interview question generation not yet implemented")

ai_service = AIService()
