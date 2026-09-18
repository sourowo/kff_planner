"""把場次資料組進網頁：python3 build.py
讀 kff2026_screenings.json（長短片）＋ extra_data.py（XR、活動），
輸出更新後的 JSON 與 index.html，並做基本檢查。"""
import json, sys
from collections import defaultdict
from extra_data import *

OUT = ""   # 直接在根目錄執行

d = json.load(open(OUT + "kff2026_screenings.json"))

# 移除取消的場次；若影片因此沒有任何場次，一併移除
refs = lambda s: {v for v in s.values() if isinstance(v, str)}
gone = [s for s in d["screenings"] if (s["date"], s["venue_id"], s["start"]) in CANCELLED]
d["screenings"] = [s for s in d["screenings"] if s not in gone]
still = set().union(*map(refs, d["screenings"]))
gone_refs = set().union(*map(refs, gone)) if gone else set()
removed_films = [f["title_zh"] for f in d["films"] if f["id"] in gone_refs and f["id"] not in still]
d["films"] = [f for f in d["films"] if f["title_zh"] not in removed_films]
if gone:
    print(f"已移除取消場次 {len(gone)} 場")
if removed_films:
    print("已移除沒有場次的影片：" + "、".join(removed_films))

# 活動場補說明（保留原本的 note）
for s in d["screenings"]:
    k = (s["date"], s["venue_id"], s["start"])
    if k in SCREENING_NOTES:
        base = s.get("note", "")
        extra = SCREENING_NOTES[k]
        if extra not in base:
            s["note"] = "；".join(x for x in [base, extra] if x)

# 影人出席名單（官網公告）：寫進場次，並補上「影人出席」標記
import re
for s in d["screenings"]:
    k = (s["date"], s["venue_id"], s["start"])
    if k in GUESTS:
        s["guests"] = GUESTS[k]
        tags = [t for t in s.get("tags", []) if t]
        if "filmmaker_talk" not in tags: tags.append("filmmaker_talk")
        if k in GREETING and "pre_greeting" not in tags: tags.append("pre_greeting")
        s["tags"] = tags

# 臺灣代理發行：官網片名對應到 title_zh，再算出短標籤
def _norm(t): return re.sub(r"\s+", "", t).replace("《", "").replace("》", "")
def _short(plan):
    m = re.match(r"(\d{4})年(\d{1,2})月(\d{1,2})日(.+)", plan)
    if m:
        y, mo, dd, what = m.groups()
        head = f"{mo}/{dd}" if y == "2026" else f"{y}/{mo}/{dd}"
        return f"{head} {what.replace('上線', '上線').replace('電視台首播', '電視首播')}"
    m = re.match(r"(\d{4})年(\d{1,2})月(.+)", plan)
    if m:
        y, mo, what = m.groups()
        head = f"{mo}月" if y == "2026" else f"{y}/{mo}"
        return f"{head} {what.replace('串流平臺上線', '串流上線')}"
    m = re.match(r"(\d{4})年?(第.季)?(.+)", plan)
    if m:
        y, q, what = m.groups()
        return f"{y}{' ' + q if q else ''} {what.replace('串流平臺上線', '串流上線')}"
    return plan
dist_err = []
for name, plan in DISTRIBUTION.items():
    hit = [f for f in d["films"] if _norm(name) in _norm(f["title_zh"])]
    if len(hit) != 1:
        dist_err.append(f"代理發行對不到片名（{len(hit)} 筆）：{name}")
        continue
    hit[0]["distribution"] = plan
    hit[0]["distribution_short"] = _short(plan)

for f in d["films"]:
    if f["title_zh"] in FILM_LINKS: f["url"] = FILM_LINKS[f["title_zh"]]
    if f["title_zh"] == "AI 無界限":
        f["section"] = "主題講堂：AI 無界限"; f.pop("section_inferred", None)

seen = {(s["date"], s["venue_id"], s["start"]) for s in d["screenings"]}
guest_err = [f"影人名單對不到場次：{k}" for k in GUESTS if k not in seen]

known = {v["id"] for v in d["venues"]}
d["venues"] += [{"id":k,"name":v} for k,v in NEW_VENUES.items() if k not in known]
secs = [s for s in d["sections"] if s != "其他"]
for s in ["主題講堂：AI 無界限"] + EXTRA_SECTIONS:
    if s not in secs: secs.append(s)
d["sections"] = secs + ["其他"]
d["ticket_prices"].update({
    "xr":{"early":250,"regular":300},
    "xr_special":{"early":699,"regular":799},
    "free":{"early":0,"regular":0},
})
d["xr_setup_min"] = 10  # XR 觀影前說明與設備配戴，手冊說 5–15 分鐘
d["xr_programs"] = XR
d["events"] = EVENTS

# ---- 檢查 ----
vids = {v["id"] for v in d["venues"]}
err = dist_err + guest_err
for x in XR + EVENTS:
    if x["venue_id"] not in vids: err.append(f"未知場館 {x['venue_id']} ({x['id']})")
ids = [x["id"] for x in XR + EVENTS + d["films"]]
if len(ids) != len(set(ids)): err.append("id 重複")
titles = {f["title_zh"] for f in d["films"]}
for t in FILM_LINKS:  # 片名改了會讓連結失效，提早發現（已取消的影片略過）
    if t not in titles and t not in removed_films: err.append(f"FILM_LINKS 找不到片名：{t}")
m = lambda t: int(t[:2])*60 + int(t[3:])
for p in XR:  # 同一作品相鄰兩場不能比片長還近
    sch = p["schedule"]
    lists = [sch["times"]] if sch["type"] == "daily" else sch["times"].values()
    for ts in lists:
        for a, b in zip(ts, ts[1:]):
            if m(b) - m(a) < p["runtime_min"]: err.append(f"{p['code']} {a}→{b} 比片長短")
if err:
    print("\n".join(err)); sys.exit(1)

print(f"影人出席 {sum('guests' in s for s in d['screenings'])} 場、"
      f"代理發行 {sum('distribution' in f for f in d['films'])} 部")
d = {k: d[k] for k in ["festival","dates","ticket_prices","xr_setup_min","sections","venues",
                       "films","screenings","xr_programs","events"]}
json.dump(d, open(OUT + "kff2026_screenings.json", "w"), ensure_ascii=False, indent=2)
tpl = open("template.html").read()
open(OUT + "index.html", "w").write(
    tpl.replace("__DATA__", json.dumps(d, ensure_ascii=False).replace("</", "<\\/")))

n_xr = sum(len(p["schedule"]["times"]) * 18 if p["schedule"]["type"] == "daily"
           else sum(map(len, p["schedule"]["times"].values())) for p in XR)
print(f"長短片 {len(d['screenings'])} 場、XR {len(XR)} 部 {n_xr} 個時段、活動 {len(EVENTS)} 項")
