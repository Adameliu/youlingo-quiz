import requests, re, json, sys, time
sys.stdout.reconfigure(encoding="utf-8")

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
s.get("https://sharplingo.cn/", timeout=10)
s.post("https://sharplingo.cn/users/login-chinese",
       data={"email": "u861687@oakon.com", "password": "OOVXgWR0M0kh"}, timeout=10)

course_id = "5f543b6fcbbecf4bf8012850"

# Get all modules
r = s.get(f"https://sharplingo.cn/courses/show/{course_id}", timeout=10)
modules = re.findall(r'href="[^"]*module/([a-f0-9]{24})/show"[^>]*>([^<]*)</a>', r.text)
print(f"Modules: {len(modules)}")

# Get sections for each module and count cards
total_cards = 0
total_sections = 0
for midx, (mod_id, mod_name) in enumerate(modules[:23]):
    mod_name = mod_name.replace("&amp;", "&").strip()
    r = s.get(f"https://sharplingo.cn/courses/{course_id}/module/{mod_id}/show", timeout=10)
    section_ids = re.findall(r'/courses/show-flashcards/([a-f0-9]{24})/0', r.text)
    total_sections += len(section_ids)
    
    # Count cards in first 2 sections of each module for estimation
    module_cards = 0
    for sid in section_ids[:2]:
        r2 = s.get(f"https://sharplingo.cn/courses/get-module-flashcards/{sid}", timeout=10)
        try:
            cards = r2.json()
            module_cards += len(cards)
        except:
            pass
    avg = module_cards / min(len(section_ids), 2) if section_ids else 0
    est = int(avg * len(section_ids))
    total_cards += est
    time.sleep(0.1)
    print(f"  {mod_name}: {len(section_ids)} sections, ~{est} cards")

print(f"\nTotal sections: {total_sections}")
print(f"Estimated total cards: ~{total_cards}")
