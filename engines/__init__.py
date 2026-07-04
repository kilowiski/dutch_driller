"""
Conjugation engine base interface.
To add a new language, subclass ConjugationEngine and implement all methods.
"""

class ConjugationEngine:
    """Each language gets its own subclass. The app only calls these methods."""

    # ── Must override ──────────────────────────────────────────────────

    pronouns: dict = {}       # {"ik": "I", "jij": "you", ...}
    tenses: list = []         # ["present", "past", ...]
    tense_labels: dict = {}   # {"present": "present tense (description)", ...}

    def get_verbs(self) -> list:
        """Return all verb entries for this language."""
        raise NotImplementedError

    def conjugate(self, verb: dict, tense: str, pronoun: str) -> str:
        """Return the conjugated form for a verb in a given tense + pronoun."""
        raise NotImplementedError

    def check_answer(self, verb: dict, tense: str, pronoun: str, user_answer: str) -> tuple:
        """Return (is_correct: bool, correct_form: str)."""
        raise NotImplementedError
