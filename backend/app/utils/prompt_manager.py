import os
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent.parent.parent / "prompts"

class PromptManager:
    @staticmethod
    def get_prompt(prompt_name: str, version: str = "v1") -> str:
        """
        Loads a prompt template from disk by name and version.
        Example: get_prompt("resume_feedback", "v1")
        """
        file_path = PROMPTS_DIR / f"{prompt_name}_{version}.txt"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {file_path}")
            
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
