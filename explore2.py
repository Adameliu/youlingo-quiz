import requests, re, sys, json
sys.stdout.reconfigure(encoding="utf-8")

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
s.get("https://sharplingo.cn/", timeout=10)
s.post("https://sharplingo.cn/users/login-chinese",
       data={"email": "u861687@oakon.com", "password": "OOVXgWR0M0kh"}, timeout=10)

course_id = "5f543b6fcbbecf4bf8012850"
r = s.get(f"https://sharplingo.cn/courses/show/{course_id}", timeout=10)
text = r.text

# Check the title
title = re.search(r"<title>(.*?)</title>", text)
print("Title:", title.group(1) if title else "N/A")

# Check for course info
course_info = re.findall(r"class=\"course-info[^\"]*\"", text)
print("Course info classes:", course_info[:5])

# Look for any links with module in them
mod_links = re.findall(r'href="([^"]*module[^"]*)"[^>]*>([^<]*)<', text)
print("\nModule links:", mod_links[:5])

# Check if there's a redirect
print("Final URL:", r.url)

# Search for the word English or 英语
import html
if "英语" in text or "English" in text:
    idx = text.find("英语") if "英语" in text else text.find("English")
    context = text[max(0,idx-100):idx+200]
    context = re.sub(r"<[^>]+>", " ", context).strip()
    context = re.sub(r"\s+", " ", context)
    print("\nContext around English/英语:", context[:300])
else:
    print("No English/英语 found in page")

# Save page for inspection
with open("english_course.html", "w", encoding="utf-8") as f:
    f.write(text)
print("\nSaved to english_course.html")
