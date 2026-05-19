import requests, json, sys, time, os
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.stdout.reconfigure(encoding="utf-8")

BASE = "C:/Users/yulau/Documents/Codex/2026-05-17/new-chat-2"
section_cards = json.load(open(BASE + "/english_section_cards.json", "r", encoding="utf-8"))

all_cards = [{"id": card["id"], "module": data["module"]} 
             for sec_id, data in section_cards.items() for card in data["cards"]]

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
s.get("https://sharplingo.cn/", timeout=10)
s.post("https://sharplingo.cn/users/login-chinese",
       data={"email": "u861687@oakon.com", "password": "OOVXgWR0M0kh"}, timeout=10)
cookies = s.cookies.get_dict()

answers = json.load(open(BASE + "/english_card_answers.json", "r", encoding="utf-8"))
remaining = [c for c in all_cards if c["id"] not in answers]
print(f"Total: {len(all_cards)}, Already done: {len(answers)}, Remaining: {len(remaining)}", flush=True)

def fetch(cid):
    try:
        r = requests.post("https://sharplingo.cn/courses/validate-flashcard-answer",
                         data={"cardId": cid, "answer": ""},
                         cookies=cookies, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        res = r.json()
        fb = res.get("feedback", [])
        ans = fb[0].get("correctAnswer", "") if fb else ""
        return (cid, {"correct_answer": ans, "card_type": res.get("type", "")})
    except:
        return (cid, {"correct_answer": "", "card_type": ""})

togo = remaining[:]
done_count = len(answers)
start = time.time()

while togo:
    batch = togo[:3000]
    togo = togo[3000:]
    with ThreadPoolExecutor(max_workers=50) as ex:
        fs = {ex.submit(fetch, c["id"]): c for c in batch}
        for f in as_completed(fs):
            cid, result = f.result()
            answers[cid] = result
    done_count = len(answers)
    json.dump(answers, open(BASE + "/english_card_answers.json", "w", encoding="utf-8"))
    print(f"{done_count}/{len(all_cards)} ({time.time()-start:.0f}s)", flush=True)

print(f"DONE: {done_count} in {time.time()-start:.0f}s", flush=True)
