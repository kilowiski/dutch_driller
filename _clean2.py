import os

# Clean models.py
p = r"C:\Users\jta99\Documents\dutch_driller\models.py"
with open(p, encoding="utf-8") as f:
    t = f.read()
t = t.replace("\n\n# ── Audio URL cache ───────────────────────────────────────────────────\n\ndef get_cached_audio_url(dutch_word):\n    \"\"\"Return cached Wiktionary audio URL or None.\"\"\"\n    conn = get_db()\n    try:\n        row = conn.execute(\"SELECT audio_url FROM vocab_words WHERE dutch = ? AND audio_url != ''\",\n                           (dutch_word,)).fetchone()\n        return row[\"audio_url\"] if row else None\n    except:\n        return None\n    finally:\n        conn.close()\n\ndef cache_audio_url(dutch_word, url):\n    \"\"\"Store fetched audio URL in vocab_words.\"\"\"\n    conn = get_db()\n    try:\n        conn.execute(\"UPDATE vocab_words SET audio_url = ? WHERE dutch = ?\", (url, dutch_word))\n        conn.commit()\n    except:\n        pass\n    conn.close()\n\n", "\n\n")
with open(p, "w", encoding="utf-8") as f:
    f.write(t)

# Cleanup temp file
os.remove(r"C:\Users\jta99\Documents\dutch_driller\_strip.py")
print("done")
