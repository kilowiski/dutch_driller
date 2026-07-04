import zipfile, os

root = r"C:\Users\jta99\Documents\dutch_driller"
out = root + "-clean.zip"
skip_dirs = {".venv", "__pycache__", ".git"}
skip_files = {"drills.db", "dutch_driller.zip", "dutch_driller-clean.zip"}

with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for f in filenames:
            if f in skip_files:
                continue
            full = os.path.join(dirpath, f)
            arcname = os.path.relpath(full, root)
            zf.write(full, arcname)

size = os.path.getsize(out) / 1024
print(f"Clean zip ready: {out} ({size:.1f} KB)")
