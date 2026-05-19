import requests, json, sys, time, os
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.stdout.reconfigure(encoding="utf-8")

BASE = "C:/Users/yulau/Documents/Codex/2026-05-17/new-chat-2"
section_cards = json.load(open(BASE + "/english_section_cards.json", "r", encoding="utf-8"))

# Get all card IDs
all_cards = []
for sec_id, data in section_cards.items():
    for card in data["cards"]:
        all_cards.append({"id": card["id"], "module": data["module"]})

print("Total cards to process:", len(all_cards), flush=True)

# Login
s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
s.get("https://sharplingo.cn/", timeout=10)
s.post("https://sharplingo.cn/users/login-chinese",
       data={"email": "u861687@oakon.com", "password": "OOVXgWR0M0kh"}, timeout=10)
cookies = s.cookies.get_dict()

# Load existing progress if any
answers = {}
progress_file = BASE + "/english_card_answers.json"
if os.path.exists(progress_file):
    with open(progress_file, "r", encoding="utf-8") as f:
        answers = json.load(f)
    print(f"Loaded {len(answers)} existing answers", flush=True)

remaining = [c for c in all_cards if c["id"] not in answers]
print(f"Remaining: {len(remaining)}", flush=True)

def fetch(card):
    cid = card["id"]
    if cid in answers:
        return (cid, answers[cid], True)
    try:
        r = requests.post("https://sharplingo.cn/courses/validate-flashcard-answer",
                         data={"cardId": cid, "answer": ""},
                         cookies=cookies, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        res = r.json()
        fb = res.get("feedback", [])
        ans = fb[0].get("correctAnswer", "") if fb else ""
        return (cid, {"correct_answer": ans, "card_type": res.get("type", "")}, True)
    except:
        return (cid, {"correct_answer": "", "card_type": ""}, True)

todo = remaining[:]
done_count = len(answers)
start = time.time()
batch = 0
while todo:
    batch += 1
    batch_cards = todo[:2000]
    todo = todo[2000:]
    with ThreadPoolExecutor(max_workers=30) as ex:
        for cid, result, _ in [f.result() for f in as_completed({ex.submit(fetch, c): c for c in batch_cards})]:
            answers[cid] = result
            done_count += 1
    json.dump(answers, open(progress_file, "w", encoding="utf-8"))
    elapsed = time.time() - start
    print(f"Batch {batch}: {done_count}/{len(all_cards)} ({elapsed:.0f}s)", flush=True)

print(f"\nDONE: {done_count} cards in {time.time()-start:.0f}s", flush=True)
