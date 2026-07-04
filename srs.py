"""
SM-2 Lite spaced repetition algorithm.
Based on SuperMemo-2, simplified for binary correct/wrong feedback.

Each item tracks three values:
  ef       — easiness factor (starts at 2.5, clamped to ≥1.3)
  interval — days until next review
  reps     — consecutive correct streak

After each review:
  Wrong    → reset reps to 0, interval to 1 day
  Correct  → grow interval, adjust EF per SM-2 formula
"""

from datetime import date, timedelta


def quality(is_correct):
    """Map binary correct/wrong to SM-2 quality score (0-5 scale)."""
    return 4 if is_correct else 0


def update(ef, interval, reps, is_correct):
    """
    Apply one SM-2 review step.
    Returns (new_ef, new_interval, new_reps, next_review_iso).
    """
    q = quality(is_correct)

    if q < 3:
        # Failed — reset streak, review again tomorrow
        new_ef = ef
        new_interval = 1
        new_reps = 0
    else:
        # Passed — grow interval
        if reps == 0:
            new_interval = 1
        elif reps == 1:
            new_interval = 6
        else:
            new_interval = round(interval * ef)

        # SM-2 easiness factor update
        new_ef = ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        new_ef = max(1.3, new_ef)

        new_reps = reps + 1

    next_review = date.today() + timedelta(days=new_interval)

    return new_ef, new_interval, new_reps, next_review.isoformat()
