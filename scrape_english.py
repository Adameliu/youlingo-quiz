import requests, json, re, sys, time, os
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.stdout.reconfigure(encoding="utf-8")

BASE = "C:/Users/yulau/Documents/Codex/2026-05-17/new-chat-2"
s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
s.get("https://sharplingo.cn/", timeout=10)
s.post("https://sharplingo.cn/users/login-chinese",
       data={"email": "u861687@oakon.com", "password": "OOVXgWR0M0kh"}, timeout=10)

course_id = "5f543b6fcbbecf4bf8012850"

# Step 1: Get all modules and sections
print("Step 1: Getting modules...", flush=True)
r = s.get(f"https://sharplingo.cn/courses/show/{course_id}", timeout=10)
modules = re.findall(r'href="[^"]*module/([a-f0-9]{24})/show"[^>]*>([^<]*)</a>', r.text)
print(f"Found {len(modules)} modules", flush=True)

all_sections = {}
for midx, (mod_id, mod_name) in enumerate(modules):
    mod_name = mod_name.replace("&amp;", "&").strip()
    r = s.get(f"https://sharplingo.cn/courses/{course_id}/module/{mod_id}/show", timeout=10)
    section_ids = re.findall(r'/courses/show-flashcards/([a-f0-9]{24})/0', r.text)
    
    # Get section names
    sections = []
    li_matches = re.findall(r'<li[^>]*style="font-size:\s*20px[^"]*"[^>]*>(.*?)</li>', r.text, re.DOTALL)
    for li in li_matches:
        sid = re.search(r'/courses/show-flashcards/([a-f0-9]{24})/0', li)
        manage = re.search(r'/courses/manage-flashcards/([a-f0-9]{24})', li)
        sec_id = sid.group(1) if sid else (manage.group(1) if manage else "")
        if sec_id:
            li_clean = re.sub(r'<[^>]+>', ' ', li)
            li_clean = re.sub(r'\s+', ' ', li_clean).strip()
            for remove in ["习题列表", "全部习题"]:
                li_clean = li_clean.replace(remove, "").strip()
            li_clean = re.sub(r'\s+', ' ', li_clean).strip()
            sections.append({"id": sec_id, "name": li_clean})
    
    all_sections[mod_name] = sections
    print(f"  {mod_name}: {len(sections)} sections", flush=True)

# Save section data
json.dump(all_sections, open(BASE + "/english_sections.json", "w", encoding="utf-8"), ensure_ascii=False)
print(f"\nSaved sections. Total: {sum(len(v) for v in all_sections.values())}", flush=True)

# Step 2: Get card IDs for each section (concurrent)
print("\nStep 2: Getting card IDs for all sections...", flush=True)
cookies = s.cookies.get_dict()
flat = [(mod_name, sec["name"], sec["id"]) for mod_name, sections in all_sections.items() for sec in sections]

def get_cards(mod_name, sec_name, sec_id):
    try:
        r = requests.get(f"https://sharplingo.cn/courses/get-module-flashcards/{sec_id}",
                        cookies=cookies, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        cards = r.json()
        return (sec_id, {"module": mod_name, "section_name": sec_name, "cards": cards})
    except:
        return (sec_id, {"module": mod_name, "section_name": sec_name, "cards": []})

section_data = {}
done = 0; start = time.time()
with ThreadPoolExecutor(max_workers=20) as ex:
    futures = {ex.submit(get_cards, *f): f for f in flat}
    for f in as_completed(futures):
        sec_id, data = f.result()
        section_data[sec_id] = data
        done += 1
        if done % 100 == 0:
            print(f"  {done}/{len(flat)} ({time.time()-start:.0f}s)", flush=True)

total_cards = sum(len(v["cards"]) for v in section_data.values())
json.dump(section_data, open(BASE + "/english_section_cards.json", "w", encoding="utf-8"), ensure_ascii=False)
print(f"Done! {done} sections, {total_cards} cards", flush=True)
