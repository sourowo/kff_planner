"""把場次資料組進網頁：python3 build.py
讀 kff2026_screenings.json（長短片）＋ extra_data.py（XR、活動），
輸出更新後的 JSON 與 index.html，並做基本檢查。"""
import json, sys
from collections import defaultdict
from extra_data import *

OUT = "../"   # 輸出到上一層（網站根目錄）；在 build 資料夾裡執行
d = json.load(open(OUT + "kff2026_screenings.json"))

# 移除取消的場次；若影片因此沒有任何場次，一併移除
refs = lambda s: {v for v in s.values() if isinstance(v, str)}
gone = [s for s in d["screenings"] if (s["date"], s["venue_id"], s["start"]) in CANCELLED]
d["screenings"] = [s for s in d["screenings"] if s not in gone]
still = set().union(*map(refs, d["screenings"]))
gone_refs = set().union(*map(refs, gone)) if gone else set()
d["films"] = [f for f in d["films"] if not (f["id"] in gone_refs and f["id"] not in still)]
if gone:
    print(f"已移除取消場次 {len(gone)} 場")

# 活動場補說明（保留原本的 note）
for s in d["screenings"]:
    k = (s["date"], s["venue_id"], s["start"])
    if k in SCREENING_NOTES:
        base = s.get("note", "")
        extra = SCREENING_NOTES[k]
        if extra not in base:
            s["note"] = "；".join(x for x in [base, extra] if x)

for f in d["films"]:
    if f["title_zh"] in FILM_LINKS: f["url"] = FILM_LINKS[f["title_zh"]]
    if f["title_zh"] == "AI 無界限":
        f["section"] = "主題講堂：AI 無界限"; f.pop("section_inferred", None)

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
d["xr_setup_min"] = 10          # XR 觀影前說明與設備配戴，手冊說 5–15 分鐘
d["xr_programs"] = XR
d["events"] = EVENTS

# ---- 檢查 ----
vids = {v["id"] for v in d["venues"]}
err = []
for x in XR + EVENTS:
    if x["venue_id"] not in vids: err.append(f"未知場館 {x['venue_id']} ({x['id']})")
ids = [x["id"] for x in XR + EVENTS + d["films"]]
if len(ids) != len(set(ids)): err.append("id 重複")
titles = {f["title_zh"] for f in d["films"]}
for t in FILM_LINKS:                  # 片名改了會讓連結失效，提早發現
    if t not in titles: err.append(f"FILM_LINKS 找不到片名：{t}")
m = lambda t: int(t[:2])*60 + int(t[3:])
for p in XR:                      # 同一作品相鄰兩場不能比片長還近
    sch = p["schedule"]
    lists = [sch["times"]] if sch["type"] == "daily" else sch["times"].values()
    for ts in lists:
        for a, b in zip(ts, ts[1:]):
            if m(b) - m(a) < p["runtime_min"]: err.append(f"{p['code']} {a}→{b} 比片長短")
if err:
    print("\n".join(err)); sys.exit(1)

d = {k: d[k] for k in ["festival","dates","ticket_prices","xr_setup_min","sections","venues",
                       "films","screenings","xr_programs","events"]}
json.dump(d, open(OUT + "kff2026_screenings.json", "w"), ensure_ascii=False, indent=2)
tpl = open("template.html").read()
open(OUT + "index.html", "w").write(
    tpl.replace("__DATA__", json.dumps(d, ensure_ascii=False).replace("</", "<\\/")))
n_xr = sum(len(p["schedule"]["times"]) * 18 if p["schedule"]["type"] == "daily"
           else sum(map(len, p["schedule"]["times"].values())) for p in XR)
print(f"長短片 {len(d['screenings'])} 場、XR {len(XR)} 部 {n_xr} 個時段、活動 {len(EVENTS)} 項")
