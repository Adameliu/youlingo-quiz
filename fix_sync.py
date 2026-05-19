path = r"C:\Users\yulau\Documents\Codex\2026-05-17\new-chat-2\study_app.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace loadProg and saveProg to sync with server
old_prog = """function loadProg() { try { var p = localStorage.getItem(STORAGE_KEY); if(p) prog = JSON.parse(p); } catch(e) {} }
function saveProg() { localStorage.setItem(STORAGE_KEY, JSON.stringify(prog)); }"""

new_prog = """function loadProg() {
    // Try server first, fallback to local
    try { var p = localStorage.getItem(STORAGE_KEY); if(p) prog = JSON.parse(p); } catch(e) {}
    fetch("/progress").then(function(r){ return r.json(); }).then(function(d){
        if(d && Object.keys(d).length > 0) { prog = d; saveProg(); renderMods(); }
    }).catch(function(){});
}
function saveProg() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(prog));
    // Sync to server (async, don"t block)
    try {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/progress", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify(prog));
    } catch(e) {}
}"""

content = content.replace(old_prog, new_prog, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated progress sync")
