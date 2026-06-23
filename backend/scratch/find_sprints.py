with open(r"d:\project_owm\Collobration_sami\frontend\index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for idx, line in enumerate(lines):
        if 'id="reg' in line or 'id="log' in line or '<form' in line or 'localStorage.setItem' in line:
            print(f"Line {idx+1}: {line.strip()}")
