import json, sys, re
sys.stdout.reconfigure(encoding="utf-8")

section_cards = json.load(open(r"C:\Users\yulau\Documents\Codex\2026-05-17\new-chat-2\english_section_cards.json", "r", encoding="utf-8"))

radio_count = 0
multi_count = 0
audio_count = 0
total = 0

for sec_id, data in section_cards.items():
    for card in data["cards"]:
        total += 1
        back = card.get("back", "")
        if "radio" in back: radio_count += 1
        if len(re.findall(r"<label>(.*?)</label>\s*<input", back)) > 1: multi_count += 1
        if "mp3" in card.get("front", "") or "mp3" in card.get("back", ""): audio_count += 1

print("Total cards:", total)
print("Radio buttons:", radio_count)
print("Multi-input fields:", multi_count)
print("Has audio:", audio_count)

# Sample card
for sec_id, data in section_cards.items():
    for card in data["cards"]:
        cid = card["id"]
        front = card.get("front", "")
        back = card.get("back", "")
        q = re.sub(r"<[^>]+>", " ", front).strip()
        q = re.sub(r"\s+", " ", q)[:120]
        print("\nSample card:")
        print("  ID:", cid)
        print("  Q:", q)
        print("  Has radio:", "radio" in back)
        print("  Has multi-input:", len(re.findall(r"<label>(.*?)</label>\s*<input", back)) > 1)
        print("  Front (raw):", front[:300])
        break
    break
