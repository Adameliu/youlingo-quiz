import re
path = "C:/Users/yulau/Documents/Codex/2026-05-17/new-chat-2/study_app.html"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(len(lines)):
    line = lines[i]
    # Fix SVG line - change to single-quoted JS string
    if 'sp.innerHTML = "<svg viewBox="0 0 24 24"' in line:
        lines[i] = line.replace(
            'sp.innerHTML = "<svg viewBox="0 0 24 24" width="28" height="28"><path fill="#17a2b8" d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>";',
            "sp.innerHTML = '<svg viewBox=\"0 0 24 24\" width=\"28\" height=\"28\"><path fill=\"#17a2b8\" d=\"M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z\"/></svg>';"
        )
        print("Fixed SVG line " + str(i+1))

    # Fix module card line
    if 'div.innerHTML = "<div class="name">"+m.name+"</div>' in line:
        lines[i] = line.replace(
            'div.innerHTML = "<div class="name">"+m.name+"</div><div class="count">"+learned+"/"+total+" ("+pct+"%)</div><div class="bar"><div class="fill" style="width:'+pct+'%"></div></div>";',
            "div.innerHTML = '<div class=\"name\">'+m.name+'</div><div class=\"count\">'+learned+'/'+total+' ('+pct+'%)</div><div class=\"bar\"><div class=\"fill\" style=\"width:'+pct+'%\"></div></div>';"
        )
        print("Fixed mod card line " + str(i+1))

    # Fix stats line
    if 'document.getElementById("gstats").innerHTML = "<div class="stat"><div class="n">"+tl+' in line:
        lines[i] = line.replace(
            'document.getElementById("gstats").innerHTML = "<div class="stat"><div class="n">'+tl+'</div><div class="l">已学</div></div><div class="stat"><div class="n">'+tm+'</div><div class="l">已掌握</div></div><div class="stat"><div class="n">'+(tc?Math.round(tl/tc*100):0)+'%</div><div class="l">总进度</div></div><div class="stat"><div class="n">'+tc+'</div><div class="l">总卡片</div></div>";',
            "document.getElementById(\"gstats\").innerHTML = '<div class=\"stat\"><div class=\"n\">'+tl+'</div><div class=\"l\">已学</div></div><div class=\"stat\"><div class=\"n\">'+tm+'</div><div class=\"l\">已掌握</div></div><div class=\"stat\"><div class=\"n\">'+(tc?Math.round(tl/tc*100):0)+'%</div><div class=\"l\">总进度</div></div><div class=\"stat\"><div class=\"n\">'+tc+'</div><div class=\"l\">总卡片</div></div>';"
        )
        print("Fixed stats line " + str(i+1))

    # Fix section item line
    if 'div.innerHTML = "<div><div class="sn">'+dn+'</div>' in line and '已学' in line:
        lines[i] = line.replace(
            'div.innerHTML = "<div><div class="sn">'+dn+'</div><div class="sm">'+learned+'/'+total+' 已学 · '+mastered+' 已掌握</div><div class="sb"><div class="fill" style="width:'+pct+'%"></div></div></div><div><span class="badge bg-info">'+total+'</span></div>";',
            "div.innerHTML = '<div><div class=\"sn\">'+dn+'</div><div class=\"sm\">'+learned+'/'+total+' 已学 · '+mastered+' 已掌握</div><div class=\"sb\"><div class=\"fill\" style=\"width:'+pct+'%\"></div></div></div><div><span class=\"badge bg-info\">'+total+'</span></div>';"
        )
        print("Fixed section line " + str(i+1))

with open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)
print("All fixes applied!")
