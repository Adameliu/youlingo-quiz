import re, html

with open(r"C:\Users\yulau\Documents\Codex\2026-05-17\new-chat-2\english_course.html", "r", encoding="utf-8") as f:
    text = f.read()

# Find course-info-div content
idx = text.find("course-info-div")
if idx >= 0:
    end = text.find("</div>", idx + 5000)
    body = text[idx:end+5000] if end > 0 else text[idx:idx+10000]
else:
    body = text

# Find all links with show-flashcards or module
for pat in ["module", "show-flashcard", "manage-flashcard", "get-module"]:
    matches = re.findall(r"href=\"([^\"]*" + pat + r"[^\"]*)\"", body)
    if matches:
        print(f"Links with '{pat}':")
        for m in matches[:10]:
            print(f"  {m}")

# Find course content structure  
text_only = re.sub(r"<[^>]+>", "\n", body)
lines = [l.strip() for l in text_only.split("\n") if l.strip()]
print("\nCourse page text content:")
for line in lines[:40]:
    print(f"  {line}")
