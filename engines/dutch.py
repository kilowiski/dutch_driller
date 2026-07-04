"""
Dutch conjugation engine — 't kofschip, regular + irregular + modal verbs.
"""

from engines import ConjugationEngine
from models import get_verbs as _db_get_verbs


class DutchEngine(ConjugationEngine):
    pronouns = {
        "ik": "I", "jij": "you (sg inf)", "u": "you (formal)",
        "hij": "he", "zij": "she", "het": "it",
        "wij": "we", "jullie": "you (pl)", "zij_pl": "they",
    }

    tenses = ["present", "past", "perfect"]

    tense_labels = {
        "present": "present tense (tegenwoordige tijd)",
        "past":    "simple past (onvoltooid verleden tijd)",
        "perfect": "present perfect (voltooid tegenwoordige tijd)",
    }

    def get_verbs(self, lang="nl"):
        return _db_get_verbs(lang)

    # ── Conjugation logic ──────────────────────────────────────────

    def conjugate(self, verb, tense, pronoun):
        import json
        irr = verb.get("irregular", {})
        if isinstance(irr, str):
            irr = json.loads(irr)
        if tense in irr and pronoun in irr[tense]:
            return irr[tense][pronoun]
        stem = verb.get("stem", "")
        if tense == "present":
            return self._present(stem, pronoun, verb["infinitive"])
        if tense == "past":
            return self._past(stem, pronoun)
        if tense == "perfect":
            return self._perfect(stem)
        return "?"

    def check_answer(self, verb, tense, pronoun, user_answer):
        correct = self.conjugate(verb, tense, pronoun)
        alts = [a.strip().lower() for a in correct.split("/")]
        return user_answer.strip().lower() in alts, correct

    # ── Dutch-specific rules ───────────────────────────────────────

    def _present(self, stem, pronoun, infinitive):
        if pronoun == "ik":
            return stem
        if pronoun in ("jij", "u", "hij", "zij", "het"):
            return stem + "t"
        return infinitive  # plural = infinitive form

    def _past(self, stem, pronoun):
        soft_endings = set("tkfschp")  # 't kofschip
        is_soft = stem[-1] in soft_endings if stem else False
        sg = "te" if is_soft else "de"
        pl = "ten" if is_soft else "den"
        if pronoun in ("ik", "jij", "u", "hij", "zij", "het"):
            return stem + sg
        return stem + pl

    def _perfect(self, stem):
        soft_endings = set("tkfschp")
        is_soft = stem[-1] in soft_endings if stem else False
        suffix = "t" if is_soft else "d"
        return "ge" + stem + suffix
