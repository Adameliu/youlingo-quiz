import json, sys, re
sys.stdout.reconfigure(encoding="utf-8")

BASE = "C:/Users/yulau/Documents/Codex/2026-05-17/new-chat-2"
sections_data = json.load(open(BASE + "/english_section_cards.json", "r", encoding="utf-8"))
answers = json.load(open(BASE + "/english_card_answers.json", "r", encoding="utf-8"))
all_sections = json.load(open(BASE + "/english_sections.json", "r", encoding="utf-8"))

LEFT_Q = "\u201c"; RIGHT_Q = "\u201d"
def clean_answer(a):
    if not a: return ""
    a = re.sub(r"<[^>]+>", "", a)
    if a.startswith(LEFT_Q) and a.endswith(RIGHT_Q): a = a[1:-1]
    parts = re.split(r"\s*[或]\s*", a)
    cleaned = []
    for p in parts:
        p = p.strip().replace(LEFT_Q, "").replace(RIGHT_Q, "").replace("\"", "").strip()
        if p and p not in cleaned: cleaned.append(p)
    return " 或 ".join(cleaned)

def get_audio_url(front):
    m = re.search(r"src=\"([^\"]+\.mp3)\"", front)
    return m.group(1) if m else ""

def extract_options(back):
    options = []
    if "radio" not in back and "checkbox" not in back: return options
    for content in re.findall(r"<i\b[^>]*>(.*?)</i>", back, re.DOTALL):
        content = content.strip()
        if not content: continue
        text = re.sub(r"<[^>]+>", " ", content).strip()
        text = re.sub(r"\s+", " ", text)
        if not text or "I don" in text or "don't know" in text.lower() or "xxxxxx" in text: continue
        options.append(content)
    return options

# Build card lookup
card_lookup = {}
for sec_id, data in sections_data.items():
    for card in data["cards"]:
        card_lookup[card["id"]] = card

modules_out = []
total_cards = 0

for mod_name, sections in all_sections.items():
    sections_out = []
    for sec in sections:
        sec_data = sections_data.get(sec["id"], {})
        sec_cards = []
        for cid in sec_data.get("cards", []):
            card = card_lookup.get(cid["id"]) if isinstance(cid, dict) else card_lookup.get(cid)
            if not card: continue
            cid2 = card["id"] if isinstance(cid, dict) else cid
            front = card.get("front", "")
            back = card.get("back", "")
            ans = answers.get(cid2, {}).get("correct_answer", "")
            ct = answers.get(cid2, {}).get("card_type", "") or "一般"
            cleaned = clean_answer(ans)
            audio = get_audio_url(front)
            opts = extract_options(back)
            sec_cards.append({
                "i": cid2, "q": front, "a": cleaned, "t": ct, "au": audio, "opts": opts
            })
        sections_out.append({"name": sec["name"], "id": sec["id"], "cards": sec_cards})
        total_cards += len(sec_cards)
    modules_out.append({"name": mod_name, "sections": sections_out})

with open(BASE + "/english_data.json", "w", encoding="utf-8") as f:
    json.dump(modules_out, f, ensure_ascii=False)

print(f"English course: {len(modules_out)} modules, {total_cards} cards")

# Check card type distribution
types = {}
for mod in modules_out:
    for sec in mod["sections"]:
        for c in sec["cards"]:
            t = c["t"]
            types[t] = types.get(t, 0) + 1
print("\nCard types:")
for t, cnt in sorted(types.items(), key=lambda x: -x[1]):
    print(f"  {t}: {cnt}")

# Check options
with_opts = sum(1 for mod in modules_out for sec in mod["sections"] for c in sec["cards"] if c["opts"])
print(f"\nCards with options: {with_opts}")
