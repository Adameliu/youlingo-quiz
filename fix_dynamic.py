import re
path = r"C:\Users\yulau\Documents\Codex\2026-05-17\new-chat-2\study_app.html"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

# 1. Remove combined data file reference
c = c.replace('const DATA_FILE = "combined_data.json";\n', "")
c = c.replace('const DATA_FILE = "combined_data.json";', "")

# 2. Remove var data = {}
c = c.replace("var data = {};", "")

# 3. Replace switchLang with dynamic loading
old = c[c.find("function switchLang("):c.find("\n\n// ===== Module Grid =====")]
# Find the actual end
start = c.find("function switchLang(")
end = c.find("// ===== Module Grid =====", start)
old = c[start:end]

new = """var langData = [];
var langFiles = {"german": "study_data_compact.json", "english": "english_data.json"};
var langInfo = {"german": {"name": "Deutsch", "flag": "\\ud83c\\udde9\\ud83c\\uddea"}, "english": {"name": "English", "flag": "\\ud83c\\uddec\\ud83c\\udde7"}};

function switchLang(lang) {
    currentLang = lang;
    document.getElementById("btn-lang-de").className = lang==="german" ? "btn btn-lg btn-primary" : "btn btn-lg btn-outline-secondary";
    document.getElementById("btn-lang-en").className = lang==="english" ? "btn btn-lg btn-primary" : "btn btn-lg btn-outline-secondary";
    var info = langInfo[lang];
    document.getElementById("lang-desc").textContent = info.flag + " " + info.name + " 加载中...";
    document.getElementById("mod-grid").innerHTML = "<div class=\\'text-center mt-3\\'><div class=\\'spinner-border text-primary\\'></div></div>";
    fetch(langFiles[lang]).then(function(r){ return r.json(); }).then(function(d) {
        langData = d;
        document.getElementById("lang-desc").textContent = info.flag + " " + info.name + " \\u00b7 " + langData.length + " \\u4e2a\\u6a21\\u5757";
        renderMods();
    }).catch(function(e) {
        document.getElementById("mod-grid").innerHTML = "<div class=\\'alert alert-danger\\'>加载失败: " + e.message + "</div>";
    });
}

// ===== Module Grid ====="""

c = c.replace(old, new, 1)

# 4. Update init - remove old fetch(DATA_FILE)
old_init = c[c.find("// Init"):c.rfind("</script>")]
# Find the fetch(DATA_FILE) part
fetch_idx = c.find("fetch(DATA_FILE)", c.find("// Init"))
if fetch_idx > 0:
    catch_idx = c.find('["catch"]', fetch_idx)
    end_script = c.find("</script>", catch_idx)
    if end_script > catch_idx:
        # Remove from fetch to end of catch
        line_end = c.find("\n", end_script - 10)
        to_remove = c[fetch_idx:end_script]
        c = c.replace(to_remove, "", 1)

# 5. Add simple init
init_marker = "// Init"
after_init = c[c.find(init_marker):]
# Replace the old btn-start-study onclick and subsequent init
old_init_section = after_init[:after_init.find("</script>")]

new_init_section = """// Init
document.getElementById("btn-start-study").onclick = startStudyAll;
switchLang("german");"""

c = c.replace(old_init_section, new_init_section, 1)

# 6. Clean up any remaining duplicates
for fn in ["renderMods","showSecs","startStudy","showCard","submitAns","loadProg","saveProg","goHome","startStudyAll","switchLang","resetAll","resetModule"]:
    cnt = c.count("function " + fn)
    if cnt > 1:
        print(f"{fn}: {cnt} - still duplicate!")
    else:
        print(f"{fn}: {cnt}")

print("script:", c.count("<script>"), c.count("</script>"))

with open(path, "w", encoding="utf-8") as f:
    f.write(c)
print("Done!")
