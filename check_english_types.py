import json, sys, re
sys.stdout.reconfigure(encoding="utf-8")

section_cards = json.load(open(r"C:\Users\yulau\Documents\Codex\2026-05-17\new-chat-2\english_section_cards.json", "r", encoding="utf-8"))

# Check card types - look at back HTML structure
type_samples = {}
total = 0
for sec_id, data in section_cards.items():
    for card in data["cards"]:
        total += 1
        cid = card["id"]
        back = card.get("back", "")
        if cid not in type_samples:
            has_radio = "radio" in back
            has_checkbox = "checkbox" in back
            has_multi_input = len(re.findall(r"<label>(.*?)</label>\s*<input", back)) > 1
            has_audio = "mp3" in card.get("front", "") or "mp3" in card.get("back", "")
            type_samples[cid] = {
                "front": card.get("front", "")[:200],
                "has_radio": has_radio,
                "has_checkbox": has_checkbox,
                "has_multi_input": has_multi_input,
                "has_audio": has_audio
            }
        if len(type_samples) >= 20:
            break
    if len(type_samples) >= 20:
        break

print("Total cards in English course:", total)
print("\nSample cards structure:")
for cid, ts in type_samples.items():
    q = re.sub(r"<[^>]+>", " ", ts["front"]).strip()
    q = re.sub(r"\s+", " ", q)[:100]
    print(f"  Radio:{ts["has_radio"]} MultiInp:{ts["has_multi_input"]} Audio:{ts["has_audio"]} Q:{q}")

# Count types
radio_count = 0
multi_count = 0
audio_count = 0
for sec_id, data in section_cards.items():
    for card in data["cards"]:
        back = card.get("back", "")
        if "radio" in back: radio_count += 1
        if len(re.findall(r"<label>(.*?)</label>\s*<input", back)) > 1: multi_count += 1
        if "mp3" in card.get("front", "") or "mp3" in card.get("back", ""): audio_count += 1

print(f"\nCards with radio: {radio_count}")
print(f"Cards with multi-input: {multi_count}")
print(f"Cards with audio: {audio_count}")
