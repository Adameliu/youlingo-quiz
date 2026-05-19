import re
path = "C:/Users/yulau/Documents/Codex/2026-05-17/new-chat-2/study_app.html"
lines = open(path, "r", encoding="utf-8").readlines()
fixed = 0
for i in range(len(lines)):
    line = lines[i]
    if '.innerHTML = "<div' in line and 'class="' in line and '"+' in line:
        # Fix by replacing outer double-quotes with single quotes
        # Only fix lines where the JS string starts with "<div (has HTML inside)
        idx = line.find('.innerHTML = "')
        if idx >= 0:
            before = line[:idx+14]
            after = line[idx+14:]
            # The closing is "; or
            if after.rstrip().endswith('";'):
                after = after.rstrip()[:-2] + "';"
            elif after.rstrip().endswith('"'):
                after = after.rstrip()[:-1] + "'"
            lines[i] = before + "'" + after + "\n"
            fixed += 1
open(path, "w", encoding="utf-8").writelines(lines)
print(f"Fixed {fixed} lines")