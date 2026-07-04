# Dutch Driller

A no-bullshit Dutch language training web app. Flask + SQLite. Dark theme.
Keyboard-driven drills. Zero gamification.

## Stack

- **Backend**: Python 3, Flask
- **Database**: SQLite via `sqlite3` (stdlib), auto-created at `drills.db`
- **Frontend**: Jinja2 templates, vanilla JS, dark CSS (GitHub-dark palette)
- **Env**: `uv` venv at `.venv/`, deps in `requirements.txt` (only `flask` + `gunicorn`)

## Run it

```powershell
.venv\Scripts\python.exe app.py        # dev, port 5080
# or double-click run.bat
```

## Project structure

```
app.py              # Flask routes + app factory
models.py           # SQLite schema, init_db(), record/query helpers
data/
  verbs.py          # Verb bank (24 verbs) + conjugation engine
  vocabulary.py     # ~100 words across 11 themed categories
templates/
  base.html         # Nav + layout
  index.html        # Home: two drill cards with accuracy stats
  vocab.html        # Vocabulary drill (NL↔EN, category filter)
  conjugate.html    # Conjugation drill (tense selector)
static/
  style.css         # Dark theme, responsive
drills.db           # SQLite DB (auto-created, gitignored)
run.bat             # Double-click launcher
```

## Architecture notes

- **Conjugation engine** (`data/verbs.py`): regular verbs use stem + `-t`/`-te(n)`/`ge-...-t` with `'t kofschip` rule. Irregulars have full override tables per tense+pronoun. `check_answer()` handles alternate forms like `kan/kunt`.
- **Vocabulary** (`data/vocabulary.py`): tuples of `(dutch, english, category)`. `BY_CATEGORY` is an auto-built lookup dict.
- **Drills work via AJAX**: each card is a `<div>` with data attributes. JS sends `POST /vocab/check` or `/conjugate/check` on Enter, updates card border (green/red) and shows correct answer.
- **Auto-focus**: first input gets focus on page load; after answering, focus jumps to next unanswered card.
- **Stats**: home page queries `vocab_overall()` and `conjugate_overall()` from `models.py`.

## Vibe / design rules

- No gamification: no hearts, no streaks, no XP, no sound effects, no animations
- Fast: type, Enter, next. No transitions or delays
- Dark theme only (GitHub-dark palette: `#0d1117` bg, `#161b22` cards, `#c9d1d9` text)
- Mobile-responsive via CSS media queries at 600px breakpoint
- No JavaScript frameworks — vanilla fetch + DOM manipulation

## Hosting plan

Target: Render free tier. Push to GitHub, connect, start command: `gunicorn app:app`.
Cold starts are acceptable for a personal drill app.

## Future ideas (not built yet)

- AI chat tutor via DeepSeek API (`/chat` route)
- Weighted review based on wrong-answer history
- Speech synthesis for pronunciation (`SpeechSynthesis` with `nl-NL`)
- Separable verbs, more irregulars
- Sentence fill-in-the-blank drills
