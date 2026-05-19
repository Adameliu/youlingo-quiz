import requests, json, re, sys
sys.stdout.reconfigure(encoding="utf-8")

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
s.get("https://sharplingo.cn/", timeout=10)
r = s.post("https://sharplingo.cn/users/login-chinese",
           data={"email": "u861687@oakon.com", "password": "OOVXgWR0M0kh"}, timeout=10)
print("Login:", r.json().get("status"))

course_id = "5f543b6fcbbecf4bf8012850"

# Get course page
r = s.get(f"https://sharplingo.cn/courses/show/{course_id}", timeout=10)
print("Course page loaded:", len(r.text), "chars")

# Extract module names and IDs
modules = re.findall(r'href="[^"]*module/([a-f0-9]{24})/show"[^>]*>([^<]*)</a>', r.text)
print("\nModules:")
total_sections = 0
for midx, (mod_id, mod_name) in enumerate(modules):
    mod_name = mod_name.replace("&amp;", "&").strip()
    r2 = s.get(f"https://sharplingo.cn/courses/{course_id}/module/{mod_id}/show", timeout=10)
    section_ids = re.findall(r'/courses/show-flashcards/([a-f0-9]{24})/0', r2.text)
    total_sections += len(section_ids)
    print(f"  {mod_name}: {len(section_ids)} sections")
    
print(f"\nTotal modules: {len(modules)}")
print(f"Total sections: {total_sections}")

# Count cards in first 3 sections
total_cards = 0
for midx, (mod_id, mod_name) in enumerate(modules[:3]):
    mod_name = mod_name.replace("&amp;", "&").strip()
    r2 = s.get(f"https://sharplingo.cn/courses/{course_id}/module/{mod_id}/show", timeout=10)
    section_ids = re.findall(r'/courses/show-flashcards/([a-f0-9]{24})/0', r2.text)
    for sid in section_ids[:5]:
        r3 = s.get(f"https://sharplingo.cn/courses/get-module-flashcards/{sid}", timeout=10)
        cards = r3.json()
        total_cards += len(cards)
        if total_cards >= 200:
            break
    if total_cards >= 200:
        break

print(f"\nSample: ~{total_cards} cards in partial scan")
print(f"Estimated total: ~{total_cards * total_sections // 15} cards")

# Check if course has audio
sample_audio = 0
for midx, (mod_id, mod_name) in enumerate(modules[:1]):
    r2 = s.get(f"https://sharplingo.cn/courses/{course_id}/module/{mod_id}/show", timeout=10)
    section_ids = re.findall(r'/courses/show-flashcards/([a-f0-9]{24})/0', r2.text)
    for sid in section_ids[:3]:
        r3 = s.get(f"https://sharplingo.cn/courses/get-module-flashcards/{sid}", timeout=10)
        cards = r3.json()
        for card in cards[:20]:
            if "mp3" in card.get("front", "") or "mp3" in card.get("back", ""):
                sample_audio += 1
print(f"\nCards with audio in sample: {sample_audio}")

# Check a sample card type
if modules:
    r2 = s.get(f"https://sharplingo.cn/courses/{course_id}/module/{modules[0][0]}/show", timeout=10)
    section_ids = re.findall(r'/courses/show-flashcards/([a-f0-9]{24})/0', r2.text)
    if section_ids:
        r3 = s.get(f"https://sharplingo.cn/courses/get-module-flashcards/{section_ids[0]}", timeout=10)
        cards = r3.json()
        if cards:
            print("\nSample card:")
            print("  Front:", cards[0].get("front", "")[:200])
            print("  Back:", cards[0].get("back", "")[:200])
            # Check card type from validate
            r4 = s.post("https://sharplingo.cn/courses/validate-flashcard-answer",
                       data={"cardId": cards[0]["id"], "answer": ""}, timeout=10)
            res = r4.json()
            print("  Type:", res.get("type", ""))
            fb = res.get("feedback", [])
            print("  Feedback:", len(fb), "items")
            if fb:
                print("  CorrectAnswer:", fb[0].get("correctAnswer", "")[:60])
