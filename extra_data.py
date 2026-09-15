# XR DREAMLAND 與活動資料（來源：2026 高雄電影節活動手冊）
T9  = "11:20 12:10 13:00 13:50 14:40 15:30 16:20 17:10 18:00".split()
T7a = "11:10 12:20 13:30 14:40 15:50 17:00 18:10".split()
T13 = "11:10 11:45 12:20 12:55 13:30 14:05 14:40 15:15 15:50 16:25 17:00 17:35 18:10".split()
T7b = "11:20 12:30 13:40 14:50 16:00 17:10 18:20".split()
T7c = "11:30 12:40 13:50 15:00 16:10 17:20 18:30".split()
T12 = "11:10 11:50 12:30 13:10 13:50 14:30 15:10 15:50 16:30 17:10 17:50 18:30".split()
T7d = "11:30 12:35 13:40 14:45 15:50 16:55 18:00".split()
T8a = "11:30 12:30 13:30 14:30 15:30 16:30 17:30 18:30".split()
T10 = "11:30 12:15 13:00 13:45 14:30 15:15 16:00 16:45 17:30 18:15".split()
T9b = "11:30 12:20 13:10 14:00 14:50 15:40 16:30 17:20 18:10".split()
T8b = "11:20 12:20 13:20 14:20 15:20 16:20 17:20 18:20".split()
T11 = "11:30 12:10 12:50 13:30 14:10 14:50 15:30 16:10 16:50 17:30 18:10".split()
T13b= "11:30 12:05 12:40 13:15 13:50 14:25 15:00 15:35 16:10 16:45 17:20 17:55 18:30".split()
RANGE = ["2026-10-09","2026-10-26"]

def daily(times): return {"type":"daily","range":RANGE,"times":times}

# 360 影廳：每 5 天循環一次（10/9 = A 型）
CYCLE = [
 {"C7":["11:10","16:40"],"C3":["12:40","18:10"],"C8C1":["13:40"],"C4C5":["14:40"],"C2C6":["15:40"]},
 {"C7":["15:10"],"C3":["11:10","16:40"],"C8C1":["12:10","17:40"],"C4C5":["13:10"],"C2C6":["14:10"]},
 {"C7":["14:10"],"C3":["15:40"],"C8C1":["11:10","16:40"],"C4C5":["12:10","17:40"],"C2C6":["13:10"]},
 {"C7":["13:10"],"C3":["14:40"],"C8C1":["15:40"],"C4C5":["11:10","16:40"],"C2C6":["12:10","17:40"]},
 {"C7":["12:10","17:40"],"C3":["13:40"],"C8C1":["14:40"],"C4C5":["15:40"],"C2C6":["11:10","16:40"]},
]
def by_date(code):
    out = {}
    for i in range(18):
        out[f"2026-10-{9+i:02d}"] = CYCLE[i % 5][code]
    return {"type":"by_date","times":out}

S360 = "XR DREAMLAND：360 影廳"
SP3  = "XR DREAMLAND：駁二 P3 倉庫"
SBK  = "XR DREAMLAND：駁二自行車倉庫"
SZN  = "XR DREAMLAND：互動展演區"
MP = "multi_participant"
def xr(id, code, zh, en, venue, sec, rt, rating, seats, sched, ticket="xr", flags=(), note=""):
    return dict(id=id, code=code, title_zh=zh, title_en=en, venue_id=venue, section=sec,
                runtime_min=rt, rating=rating, seats=seats, ticket=ticket,
                tags=list(flags), note=note, schedule=sched)

XR = [
 xr("x-c7","C7","極限飛行","Touching the Sky","vr360",S360,59,"0+",30,by_date("C7")),
 xr("x-c3","C3","蜂嘲男孩","Honeyboys","vr360",S360,36,"15+",30,by_date("C3")),
 xr("x-c8c1","C8 & C1","媽媽走了，或許是昨天＋靈魂出竅後","Yesterday Maybe & AFTER THE SHELL","vr360",S360,30,"0+",30,by_date("C8C1")),
 xr("x-c4c5","C4 & C5","亞馬遜聖洞的秘密＋矽利克","Kamukuwaka - The Call of the Forest & SILIQ","vr360",S360,36,"12+",30,by_date("C4C5")),
 xr("x-c2c6","C2 & C6","反未來迷幻音樂祭＋亡靈電陰派對","Feedback VR - an anti futurist musical & The Venue","vr360",S360,41,"12+",30,by_date("C2C6")),
 xr("x-p","P","三麗鷗虛擬音樂祭","Sanrio Virtual Festival Project","vrzone",SZN,40,"0+",2,
    daily("12:00 13:00 14:00 15:00 16:00 17:00 18:00".split()),ticket="free",
    note="免費，需上 OPENTIX 索票；可自選 P1–P4 作品，總時長 40 分鐘內"),
 xr("x-c9","C9","漫長的告別","A Long Goodbye","p3",SP3,30,"0+",1,daily(T9)),
 xr("x-c10","C10","眾人之城：阿姆斯特丹 1652","Amsterdam 1652","p3",SP3,45,"0+",4,daily(T7a),flags=[MP]),
 xr("x-c13","C13","快樂鳥拾光","Empathy Creatures","p3",SP3,15,"0+",2,daily(T13)),
 xr("x-c14","C14","世紀首登：聖母峰 1953","Everest, the first Ascent","p3",SP3,37,"0+",6,daily(T7b),ticket="xr_special",flags=[MP]),
 xr("x-c15","C15","虛擬化身大作戰","First Virtual Suit","p3",SP3,36,"0+",6,daily(T7c),flags=[MP]),
 xr("x-c18","C18","拉拉 LAND 模擬器","Lesbian Simulator","p3",SP3,40,"12+",1,daily(T7a)),
 xr("x-c19","C19","清醒夢","Lúcido","p3",SP3,20,"0+",2,daily(T12)),
 xr("x-c20","C20/O2","我的時光機","My Time Machine","p3",SP3,23,"0+",1,daily(T12)),
 xr("x-c24","C24","艾娜的書房","Sweet Dreams","p3",SP3,40,"18+",1,daily(T7d),flags=["nudity"]),
 xr("x-c25","C25","幻影狂想曲","The Double","p3",SP3,30,"0+",2,daily(T9)),
 xr("x-c26","C26","煙硝下的雪夜","THE FORGOTTEN WAR","p3",SP3,30,"6+",3,daily(T8a),flags=[MP]),
 xr("x-c27","C27","花嘿盆","The Great Escape","p3",SP3,25,"6+",2,daily(T10)),
 xr("x-c28","C28","大水淹沒的世界","The World Came Flooding In","p3",SP3,25,"0+",1,daily(T12)),
 xr("x-c29","C29/O1","前往力馬卡伍得","Towards Jimagawod","p3",SP3,23,"0+",3,daily(T9),flags=[MP]),
 xr("x-s2","S2","一起跳舞吧","Collective Body","p3",SP3,20,"0+",4,daily(T9b)),
 xr("x-o3","O3","貝殼島","The Island of Shells","p3",SP3,32,"12+",2,daily(T8b)),
 xr("x-c11","C11","蒙娜麗莎失竊案","Crafting Crimes","bike",SBK,20,"0+",2,daily(T11)),
 xr("x-c12","C12","暗室","Dark Rooms","bike",SBK,45,"18+",3,daily(T7a),ticket="xr_special",flags=[MP]),
 xr("x-c16","C16","看見幻貓又何妨","IF YOU SEE A CAT","bike",SBK,37,"0+",2,daily(T8b)),
 xr("x-c17","C17","紐約地下世界","Katabasis","bike",SBK,45,"0+",2,daily(T7a),flags=["variable_length"]),
 xr("x-c21","C21","Nox：長夜將盡","Nox","bike",SBK,20,"12+",1,daily(T13)),
 xr("x-c22","C22","超越黑色：皮耶．蘇拉吉","Outrenoir","bike",SBK,12,"0+",2,daily(T13b)),
 xr("x-c23","C23","列","RETSU (The Line)","bike",SBK,30,"6+",1,daily(T9)),
 xr("x-s1","S1","阿提米絲：登月任務","Mission to the Moon","bike",SBK,29,"0+",6,daily(T8b),ticket="xr_special",flags=[MP]),
 xr("x-s3","S3","畢卡索：格爾尼卡的蛻變","The metamorphoses of Guernica","bike",SBK,15,"0+",3,daily(T11),flags=[MP]),
]

# ---------------- 活動 ----------------
def ev(id, title, cat, venue, date, start=None, end=None, *, est=False, date_to=None,
       fee="免費", register=None, people=None, note=None, page=None, free_flow=False):
    return {k:v for k,v in dict(id=id,title=title,category=cat,venue_id=venue,date=date,date_to=date_to,
        start=start,end=end,end_estimated=est or None,free_flow=free_flow or None,fee=fee,register=register,
        people=people,note=note,page=page).items() if v is not None}

EVENTS = [
 ev("e-ad1","口述影像共融場《熱帶魚》","展前活動","n1","2026-09-13","11:00","13:00",est=True,
    register="免費報名，視障朋友優先（見官網）",people="陳玉勳（導演）",page=11),
 ev("e-ad2","口述影像共融場《我家的事》","展前活動","n1","2026-09-13","15:00","17:00",est=True,
    register="免費報名，視障朋友優先（見官網）",people="潘客印（導演）、黃珮琪（演員）",page=11),
 ev("e-guide","選片指南","展前活動","kfa3f","2026-09-19","14:00","16:30",
    fee="免費，座位有限",people="黃晧傑、鄭秉泓、陳奕婷、王冠人、林子閎",note="入場送特別版桌上型活動手冊",page=2),
 ev("e-book","新書發表：港都扛棒仔的故事","展前活動","lib3f","2026-09-20","14:00","16:00",
    register="詳見「高雄市立圖書館－閱讀心視界」臉書",people="陳坤毅、謝一麟",page=14),
 ev("e-exhibit","青少年創作美展","展覽","kfa_stair","2026-10-06",date_to="2026-10-26",
    note="國際短片競賽 × 鳳新高中美術班",page=16),
 ev("e-corner","交流角落：影像之後，故事之間","交流活動","kfa2f_room","2026-10-10","12:00","22:00",
    date_to="2026-10-11",free_flow=True,people="曾威量、陳瑭羚、劉純佑、邱予慧",note="自由進出",page=15),
 ev("e-xr1","XR 跨國產業對談","XR 產業活動","pinway","2026-10-16","11:00","16:25",
    register="免費，需上 OPENTIX 索票",page=20),
 ev("e-villa","福爾摩沙藝術駐村計畫發表會","XR 產業活動","pier2","2026-10-16",
    note="時間請見 2026 TTXC 產業活動頁面",page=21),
 ev("e-xr2","XR 產業前驅講座","XR 產業活動","pinway","2026-10-17","10:30","16:40",
    register="免費，需上 OPENTIX 索票",page=20),
 ev("e-pitch","推一把工作坊：劇本提案","工作坊","taicca","2026-10-17",date_to="2026-10-18",
    note="限錄取學員（已有故事大綱的創作者）",page=10),
 ev("e-master","導演講堂：康斯坦蒂娜．柯薩瑪尼","專題講座","n1","2026-10-17","17:10","18:10",est=True,
    fee="請見官網",people="康斯坦蒂娜．柯薩瑪尼（導演）",note="接在《人魚戀習曲》15:00 場之後",page=9),
 ev("e-ai","主題講堂：AI 無界限","專題講座","n1","2026-10-18","14:30","15:30",est=True,
    fee="請見官網",people="主持：黃茂昌；講者：奚岳隆、曾敬懿、劉炯葰、仇晟",note="接在《AI 無界限》13:00 場之後",page=9),
 ev("e-industry","推一把工作坊：產業講座","工作坊","kfa3f","2026-10-19",
    register="需報名（手冊 QR Code）",people="洪子烜、管偉傑、黃鐙輝、朱芷瑩、黃靖祖；主持：何星冉",
    note="時間請見報名頁",page=10),
]

# 已在場次表中的活動場，補上說明
SCREENING_NOTES = {
 ("2026-10-10","kfa","13:20"):"黏土英雄 GO!（提供 12 歲以下手作材料）",
 ("2026-10-11","kfa","13:00"):"兒童劇：咕嚕嚕大風吹（豆子劇團）",
 ("2026-10-17","n1","10:30"):"森森運動會（鴨子老師）",
 ("2026-10-24","kfa","13:00"):"動畫說書人（現場配音）",
 ("2026-10-25","n1","13:00"):"法式腹語術（小強老師）",
 ("2026-10-11","n1","13:30"):"《廚師發辦》好好味場：散場享香港美食",
 ("2026-10-24","n1","19:30"):"怪物村派對場（歌舞互動、備有服裝道具）",
 ("2026-10-25","lib","19:30"):"Awww! 歌舞狂歡場（扮裝比賽）",
 ("2026-10-26","lib","13:00"):"好膽就來場（首映劇集、復刻場景）",
 ("2026-10-26","lib","15:50"):"我好興奮場（主創見面、簽名）",
 ("2026-10-17","n1","15:00"):"映後接導演講堂 17:10",
 ("2026-10-18","n1","13:00"):"映後接主題講堂 14:30",
}

NEW_VENUES = {
 "kfa3f":"高雄市電影館 3F 放映廳",
 "kfa2f_room":"高雄市電影館 2F 個人視聽室",
 "kfa_stair":"高雄市電影館 梯間展示區",
 "lib3f":"高雄市立圖書館總館 3F 階梯閣樓",
 "vr360":"VR 體感劇院 360 影廳（駁二大義區 C9-8）",
 "vrzone":"VR 體感劇院 互動展演區（駁二大義區 C9-8）",
 "p3":"駁二藝術特區 大勇 P3 倉庫",
 "bike":"駁二藝術特區 自行車倉庫",
 "pinway":"駁二藝術特區 PINWAY（大勇區 8 號倉庫）",
 "pier2":"駁二藝術特區",
 "taicca":"文策院南部營運中心交流區",
}
EXTRA_SECTIONS = [S360, SP3, SBK, SZN,
  "展前活動","專題講座","XR 產業活動","工作坊","展覽","交流活動"]
