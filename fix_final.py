import re, sys
sys.stdout.reconfigure(encoding="utf-8")
path = r"C:\Users\yulau\Documents\Codex\2026-05-17\new-chat-2\study_app.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

script_end = content.rfind("</script>")
before = content[:script_end]
after = content[script_end:]

# Remove old incomplete init
markers = [
    'var currentLang = "german";\n// Init\ndocument.getElementById("btn-start-study").onclick = startStudyAll;\n\n',
    'var currentLang = "german";\n// Init\ndocument.getElementById("btn-start-study").onclick = startStudyAll;',
]
for m in markers:
    before = before.replace(m, "")

# Add complete code
before += '''
function goHome() {
    document.getElementById("scr-sections").classList.add("hide");
    document.getElementById("scr-study").classList.add("hide");
    document.getElementById("scr-modules").classList.remove("hide");
    renderMods();
}

function startStudyAll() {
    var keys = Object.keys(data);
    var langData = data[keys[currentLang]].modules;
    var now = Date.now();
    var curMi = -1, curSi = -1;
    for(var mi=0; mi<langData.length; mi++) {
        for(var si=0; si<langData[mi].sections.length; si++) {
            var sec = langData[mi].sections[si];
            for(var ci=0; ci<sec.cards.length; ci++) {
                var p = prog[sec.cards[ci].i];
                if(!p || !p.m) { curMi = mi; curSi = si; break; }
            }
            if(curMi >= 0) break;
        }
        if(curMi >= 0) break;
    }
    if(curMi < 0) { alert("全部学习完成！"); return; }
    var reviewCards = [], newCards = [];
    var typeOrder = ["dictation","dictationChinese","meaningChinese","word","multi","gender","plural","feminine","pastParticiple","isSeparable","presentTenseConjugation","pastTenseConjugation","konjunktivII","imperativ","comparativ","superlativ","phrase","custom","array","一般"];
    for(var mi=0; mi<=curMi; mi++) {
        var maxSi = (mi === curMi) ? curSi : langData[mi].sections.length - 1;
        for(var si=0; si<=maxSi; si++) {
            var sec = langData[mi].sections[si];
            for(var ci=0; ci<sec.cards.length; ci++) {
                var c = sec.cards[ci]; var p = prog[c.i];
                if(p && p.m) continue;
                if(p && p.n && p.n < now) reviewCards.push({card:c, modIdx:mi, secIdx:si});
                else if(!p || (!p.r && !p.m)) newCards.push({card:c, modIdx:mi, secIdx:si});
            }
        }
    }
    if(reviewCards.length === 0 && newCards.length === 0) { alert("该节已全部学习完成！"); return; }
    function sortCards(arr) {
        var groups = {};
        for(var i=0; i<arr.length; i++) {
            var t = arr[i].card.t || "一般";
            if(!groups[t]) groups[t] = []; groups[t].push(arr[i]);
        }
        var result = [];
        for(var ti=0; ti<typeOrder.length; ti++) {
            var t = typeOrder[ti];
            if(groups[t]) {
                var g = groups[t].slice();
                for(var i=g.length-1; i>0; i--) { var j=Math.floor(Math.random()*(i+1)); var tmp=g[i]; g[i]=g[j]; g[j]=tmp; }
                for(var i=0; i<g.length; i++) result.push(g[i]);
            }
        }
        return result;
    }
    cards = sortCards(reviewCards).concat(sortCards(newCards));
    curModIdx = curMi; curSecIdx = curSi;
    cards = cards.map(function(x){ return x.card; });
    cardIdx = 0; sessStats = {ok:0, no:0, tot:0};
    document.getElementById("scr-modules").classList.add("hide");
    document.getElementById("scr-sections").classList.add("hide");
    document.getElementById("scr-study").classList.remove("hide");
    document.getElementById("study-sec-name").textContent = "智能学习 - " + langData[curMi].name;
    showCard();
}

function resetAll() {
    if(!confirm("确定要重置全部进度吗？")) return;
    localStorage.removeItem("sharplingo_progress_v2");
    prog = {}; renderMods();
}

function resetModule() {
    if(!confirm("确定要重置当前模块的进度吗？")) return;
    var modName = document.getElementById("sec-mod-name").textContent;
    var keys = Object.keys(data);
    var langData = data[keys[currentLang]].modules;
    for(var mi=0; mi<langData.length; mi++) {
        if(langData[mi].name === modName) {
            for(var si=0; si<langData[mi].sections.length; si++)
                for(var ci=0; ci<langData[mi].sections[si].cards.length; ci++)
                    delete prog[langData[mi].sections[si].cards[ci].i];
            break;
        }
    }
    saveProg();
    showSecs(curModIdx);
}

// Init
document.getElementById("btn-start-study").onclick = startStudyAll;

fetch(DATA_FILE).then(function(r){ return r.json(); }).then(function(d) {
    data = d;
    switchLang("german");
})["catch"](function(e) {
    document.getElementById("mod-grid").innerHTML = "<div class=\"alert alert-danger\">加载失败: " + e.message + "</div>";
});
'''

content = before + after
with open(path, "w", encoding="utf-8") as f:
    f.write(content)

for fn in ["renderMods","showSecs","startStudy","showCard","submitAns","loadProg","saveProg","goHome","startStudyAll","switchLang","resetAll","resetModule"]:
    cnt = content.count("function " + fn)
    print(f"{fn}: {cnt}")
print("OK" if content.count("<script>") == content.count("</script>") else "MISMATCH!")
