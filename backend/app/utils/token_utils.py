def estimate_tokens(text: str) -> int:
    """
    Provides a lightweight, deterministic estimation of tokens in a string.
    A common heuristic is 1 token ~= 4 chars or 1 token ~= 0.75 words.
    Here we split by whitespace and multiply by 1.3 to be safe for sub-word tokenization.
    """
    if not text:
        return 0
    words = text.split()
    return int(len(words) * 1.3)
