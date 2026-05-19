import requests, re, json, sys, time
sys.stdout.reconfigure(encoding="utf-8")

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
s.get("https://sharplingo.cn/", timeout=10)
r = s.post("https://sharplingo.cn/users/login-chinese",
           data={"email": "u861687@oakon.com", "password": "OOVXgWR0M0kh"}, timeout=10)
print("Login:", r.json().get("status"))

course_id = "5f543b6fcbbecf4bf8012850"

# Try to access the course show page while logged in
r = s.get(f"https://sharplingo.cn/courses/show/{course_id}", timeout=10)
print("\nCourse page URL:", r.url)
print("Course page size:", len(r.text))

# Look for module links
modules = re.findall(r'href="([^"]*module/([a-f0-9]{24})/show)"[^>]*>([^<]*)</a>', r.text)
print("\nModule links found:", len(modules))
for url, mid, name in modules[:10]:
    name = name.replace("&amp;", "&").strip()
    print(f"  {name}: {mid}")

if not modules:
    # Try to find any course-related links
    all_links = re.findall(r'href="([^"]*)"[^>]*>([^<]{2,})</a>', r.text)
    course_links = [(u,n) for u,n in all_links if "course" in u.lower() or "learn" in u.lower() or "study" in u.lower()]
    print("\nCourse-related links:")
    for u,n in course_links[:10]:
        print(f"  {u}: {n.strip()}")
    
    # Check what"s in the logged-in page body
    idx = r.text.find("course-info-div")
    if idx >= 0:
        body = r.text[idx:idx+8000]
        text_only = re.sub(r"<[^>]+>", "\n", body)
        lines = [l.strip() for l in text_only.split("\n") if l.strip()]
        print("\nCourse page content (logged in):")
        for line in lines[:30]:
            print(f"  {line}")

# Also try the study/manage-flashcards URL
r2 = s.get(f"https://sharplingo.cn/courses/manage-flashcards/", timeout=10)
print("\n\nManage flashcards:", r2.status_code, len(r2.text), r2.url)

# Try to find the course in user progress
r3 = s.get("https://sharplingo.cn/users/get-learned-words", timeout=10)
try:
    data = r3.json()
    print("\nLearned words status:", data.get("status"))
except:
    print("\nLearned words: not JSON")
