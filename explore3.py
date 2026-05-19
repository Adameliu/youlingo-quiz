import re

with open("C:/Users/yulau/Documents/Codex/2026-05-17/new-chat-2/english_course.html", "r", encoding="utf-8") as f:
    text = f.read()

# Find all <a> tags with href
all_links = re.findall(r"<a[^>]*href=\"([^\"]+)\"[^>]*>([^<]*)</a>", text)
print("All links with text:")
for url, name in all_links:
    name = name.strip()
    if name and len(url) < 100:
        print(f"  {url[:80]}: {name[:60]}")

# Also find module IDs directly
mod_ids = re.findall(r"[a-f0-9]{24}", text)
print(f"\nTotal MongoDB IDs: {len(mod_ids)}")

# Look for the course title/level info
import html
body_part = text[text.find("course-info-div"):text.find("footer_info")] if "footer_info" in text else text[text.find("course-info-div"):text.find("course-info-div")+5000]
text_only = re.sub(r"<[^>]+>", "\n", body_part)
lines = [l.strip() for l in text_only.split("\n") if l.strip()]
for line in lines[:30]:
    print(line)
