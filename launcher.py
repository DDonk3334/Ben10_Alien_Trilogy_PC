import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json, os, subprocess, sys, time
try:
from PIL import Image, ImageTk
PIL_OK = True
except ImportError:
PIL_OK = False
BASE = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else file))
CFG_P = os.path.join(BASE, "trilogy_cfg.json")
def rpath(p):
return os.path.join(getattr(sys, "_MEIPASS", BASE), p)
GAMES = [
("af", "ALIEN FORCE", "art_af.png", "ULUS10381"),
("va", "VILGAX ATTACKS", "art_va.png", "ULUS10488"),
("cd", "COSMIC DESTRUCTION", "art_cd.png", "ULUS10542")
]
LNG = {
"en": ("TRILOGY REMASTERED | 60 FPS", "PLAYTIME: {h}h {m}m", (" PLAY ", " SETTINGS ", " CONTROLS "), "SELECT GAME", "GAME FILE (.ISO/.CSO)", "SELECT", "Not selected", "Loaded: ", "▶ PLAY GAME", "RUNNING...", "RESOLUTION", "Native", "PERFORMANCE", "Unlock 60 FPS", "Low-End PC Mode", "Fullscreen (16:9)", "ART:", "CUSTOM", "RESET", "Select file for this game first!", [("WASD", "Move"), ("SPACE", "Jump"), ("LMB / J", "Light Attack"), ("RMB / K", "Heavy Attack"), ("SHIFT / L", "Block / Grab"), ("1-4 / ARROWS", "Select Alien"), ("Q / E", "Omnitrix / Cam"), ("ESC / TAB", "Pause / Upgrades")]),
"ru": ("ТРИЛОГИЯ REMASTERED | 60 FPS", "В ИГРЕ: {h} ч {m} м", (" ИГРАТЬ ", " НАСТРОЙКИ ", " УПРАВЛЕНИЕ "), "ВЫБЕРИТЕ ИГРУ", "ОБРАЗ ИГРЫ (.ISO/.CSO)", "ВЫБРАТЬ", "Не выбран", "Выбран: ", "▶ ЗАПУСТИТЬ", "ИГРА ЗАПУЩЕНА...", "РАЗРЕШЕНИЕ", "Родное", "ПРОИЗВОДИТЕЛЬНОСТЬ", "Разблокировать 60 FPS", "Режим для слабых ПК", "Полный экран (16:9)", "ФОН:", "СВОЁ", "СБРОС", "Сначала выберите файл для этой игры!", [("WASD", "Движение"), ("ПРОБЕЛ", "Прыжок"), ("ЛКМ / J", "Лёгкая атака"), ("ПКМ / K", "Сильная атака"), ("SHIFT / L", "Блок / Захват"), ("1-4 / СТРЕЛКИ", "Выбор пришельца"), ("Q / E", "Омнитрикс / Камера"), ("ESC / TAB", "Пауза / Улучшения")]),
"de": ("TRILOGIE REMASTERED | 60 FPS", "SPIELZEIT: {h}h {m}m", (" SPIELEN ", " OPTIONEN ", " STEUERUNG "), "SPIEL WÄHLEN", "SPIELDATEI (.ISO/.CSO)", "WÄHLEN", "Nicht gewählt", "Geladen: ", "▶ STARTEN", "LÄUFT...", "AUFLÖSUNG", "Nativ", "LEISTUNG", "60 FPS freischalten", "Schwacher PC Modus", "Vollbild (16:9)", "BILD:", "FOTO", "RESET", "Bitte erst Spieldatei wählen!", [("WASD", "Bewegen"), ("SPACE", "Springen"), ("LMB / J", "Leichter Angriff"), ("RMB / K", "Starker Angriff"), ("SHIFT / L", "Blocken / Greifen"), ("1-4 / PFEILE", "Alien wählen"), ("Q / E", "Omnitrix / Kamera"), ("ESC / TAB", "Pause / Upgrades")]),
"ja": ("トリロジー REMASTERED | 60 FPS", "プレイ時間: {h}時間 {m}分", (" プレイ ", " 設定 ", " 操作 "), "ゲーム選択", "ゲームデータ (.ISO/.CSO)", "選択", "未選択", "選択済: ", "▶ ゲーム開始", "起動中...", "解像度", "標準", "設定", "60 FPS 有効化", "低スペックPCモード", "フルスクリーン (16:9)", "背景:", "変更", "戻す", "先にゲームファイルを選択してください！", [("WASD", "移動"), ("SPACE", "ジャンプ"), ("LMB / J", "弱攻撃"), ("RMB / K", "強攻撃"), ("SHIFT / L", "ガード / つかむ"), ("1-4 / 矢印", "エイリアン選択"), ("Q / E", "オムニトリックス"), ("ESC / TAB", "ポーズ / 強化")])
}
class TrilogyApp:
def init(self, r):
self.r = r
self.r.title("Ben 10: Alien Trilogy — Remastered PC")
self.r.configure(bg="#0D1117")
self.r.geometry("960x560")
self.r.minsize(820, 480)
ico = rpath(os.path.join("assets", "icon.ico"))
if os.path.exists(ico):
try: self.r.iconbitmap(ico)
except Exception: pass
self.cfg = {"lang": "en", "sel": 0, "paths": ["", "", ""], "art": "", "res": "3", "fs": True, "fps": True, "low": False, "sec": 0}
if os.path.exists(CFG_P):
try: self.cfg.update(json.load(open(CFG_P, "r", encoding="utf-8")))
except Exception: pass
if self.cfg.get("lang") not in LNG: self.cfg["lang"] = "en"
self.pil = self.img = self.fj = self.pr = None
self.t0 = 0.0
self.aw, self.ah = 320, 500
s = ttk.Style()
s.theme_use("clam")
s.configure("TNotebook", background="#0D1117", borderwidth=0)
s.configure("TNotebook.Tab", background="#161B22", foreground="#C9D1D9", padding=(12, 6), font=("Arial", 9, "bold"))
s.map("TNotebook.Tab", background=[("selected", "#21262D")], foreground=[("selected", "#39FF14")])
s.configure("D.TFrame", background="#0D1117")
s.configure("C.TFrame", background="#161B22")
s.configure("D.TRadiobutton", background="#161B22", foreground="#FFF", font=("Arial", 9))
s.configure("D.TCheckbutton", background="#161B22", foreground="#FFF", font=("Arial", 9))
w = tk.Frame(r, bg="#0D1117")
w.pack(fill="both", expand=True, padx=16, pady=16)
l = tk.Frame(w, bg="#0D1117")
l.pack(side="left", fill="both", expand=True, padx=(0, 16))
h = tk.Frame(l, bg="#0D1117")
h.pack(fill="x", pady=(0, 10))
cv = tk.Canvas(h, width=54, height=54, bg="#0D1117", highlightthickness=0)
cv.pack(side="left", padx=(0, 10))
cv.create_oval(4, 4, 50, 50, fill="#161B22", outline="#39FF14", width=3)
cv.create_polygon(14, 11, 40, 11, 27, 27, fill="#39FF14")
cv.create_polygon(14, 43, 40, 43, 27, 27, fill="#39FF14")
tf = tk.Frame(h, bg="#0D1117")
tf.pack(side="left")
tk.Label(tf, text="BEN 10: ALIEN TRILOGY", font=("Arial", 14, "bold"), bg="#0D1117", fg="#FFF").pack(anchor="w")
self.l_sub = tk.Label(tf, font=("Arial", 8, "bold"), bg="#0D1117", fg="#39FF14")
self.l_sub.pack(anchor="w")
self.l_tm = tk.Label(tf, font=("Consolas", 8, "bold"), bg="#0D1117", fg="#8B949E")
self.l_tm.pack(anchor="w")
lf = tk.Frame(h, bg="#0D1117")
lf.pack(side="right", anchor="n")
self.lb = {c: tk.Button(lf, text=tx, font=("Arial", 7, "bold"), relief="flat", padx=5, pady=2, command=lambda x=c: self.set_lang(x)) for c, tx in [("en","US"),("ru","RU"),("de","DE"),("ja","JP")]}
for b in self.lb.values(): b.pack(side="left", padx=1)
self.nb = ttk.Notebook(l)
self.nb.pack(fill="both", expand=True)
t1, t2, t3 = ttk.Frame(self.nb, style="D.TFrame"), ttk.Frame(self.nb, style="D.TFrame"), ttk.Frame(self.nb, style="D.TFrame")
for t in (t1, t2, t3): self.nb.add(t, text=" ")
c1 = ttk.Frame(t1, style="C.TFrame", padding=15)
c1.pack(fill="both", expand=True, pady=(8, 0))
self.l_sg = tk.Label(c1, font=("Arial", 8, "bold"), bg="#161B22", fg="#39FF14")
self.l_sg.pack(anchor="w")
gf = tk.Frame(c1, bg="#161B22")
gf.pack(fill="x", pady=(6, 12))
self.gbtns = []
for idx, (_, name, _, _) in enumerate(GAMES):
b = tk.Button(gf, text=name, font=("Arial", 8, "bold"), relief="flat", pady=8, command=lambda i=idx: self.sel_game(i))
b.pack(side="left", fill="x", expand=True, padx=2)
self.gbtns.append(b)
self.l_gd = tk.Label(c1, font=("Arial", 8, "bold"), bg="#161B22", fg="#8B949E")
self.l_gd.pack(anchor="w")
rf = tk.Frame(c1, bg="#0D1117", padx=10, pady=8)
rf.pack(fill="x", pady=(6, 12))
self.l_rom = tk.Label(rf, font=("Arial", 9), bg="#0D1117", fg="#E6EDF3", wraplength=360, justify="left")
self.l_rom.pack(side="left", fill="x", expand=True)
self.b_sel = tk.Button(rf, font=("Arial", 8, "bold"), bg="#21262D", fg="#39FF14", relief="flat", padx=10, pady=5, command=self.pick_rom)
self.b_sel.pack(side="right")
self.b_play = tk.Button(c1, font=("Arial", 13, "bold"), bg="#39FF14", fg="#0D1117", relief="flat", pady=12, command=self.play)
self.b_play.pack(side="bottom", fill="x")
c2 = ttk.Frame(t2, style="C.TFrame", padding=14)
c2.pack(fill="both", expand=True, pady=(8, 0))
self.l_res = tk.Label(c2, font=("Arial", 8, "bold"), bg="#161B22", fg="#39FF14")
self.l_res.pack(anchor="w")
self.vr = tk.StringVar(value=str(self.cfg["res"]))
rf2 = tk.Frame(c2, bg="#161B22")
rf2.pack(anchor="w", pady=(2, 8))
self.rbs = [ttk.Radiobutton(rf2, text=tx, variable=self.vr, value=vl, style="D.TRadiobutton", command=self.save) for tx, vl in [("Native","1"),("720p","2"),("1080p","3"),("4K","6")]]
for rb in self.rbs: rb.pack(side="left", padx=(0, 12))
self.l_prf = tk.Label(c2, font=("Arial", 8, "bold"), bg="#161B22", fg="#39FF14")
self.l_prf.pack(anchor="w")
self.vf = tk.BooleanVar(value=self.cfg["fps"])
self.vl = tk.BooleanVar(value=self.cfg["low"])
self.vfs = tk.BooleanVar(value=self.cfg["fs"])
self.c_fps = ttk.Checkbutton(c2, variable=self.vf, style="D.TCheckbutton", command=self.save)
self.c_fps.pack(anchor="w")
self.c_low = ttk.Checkbutton(c2, variable=self.vl, style="D.TCheckbutton", command=self.tgl_low)
self.c_low.pack(anchor="w")
self.c_fs = ttk.Checkbutton(c2, variable=self.vfs, style="D.TCheckbutton", command=self.save)
self.c_fs.pack(anchor="w")
tb = tk.Frame(c2, bg="#0D1117", padx=8, pady=6)
tb.pack(fill="x", side="bottom")
self.l_art = tk.Label(tb, font=("Arial", 8, "bold"), bg="#0D1117", fg="#8B949E")
self.l_art.pack(side="left")
self.b_rsta = tk.Button(tb, font=("Arial", 8, "bold"), bg="#21262D", fg="#C9D1D9", relief="flat", padx=8, pady=3, command=self.rsta)
self.b_rsta.pack(side="right", padx=(4, 0))
self.b_csta = tk.Button(tb, font=("Arial", 8, "bold"), bg="#21262D", fg="#39FF14", relief="flat", padx=8, pady=3, command=self.csta)
self.b_csta.pack(side="right")
self.c3 = ttk.Frame(t3, style="C.TFrame", padding=14)
self.c3.pack(fill="both", expand=True, pady=(8, 0))
af = tk.Frame(w, bg="#39FF14", padx=2, pady=2)
af.pack(side="right", fill="y")
self.cv = tk.Canvas(af, width=320, height=500, bg="#161B22", highlightthickness=0)
self.cv.pack(fill="both", expand=True)
self.cv.bind("", self.on_resize)
self.set_lang(self.cfg["lang"])
self.sync_low()
self.sel_game(self.cfg["sel"], True)
def t(self, i): return LNG[self.cfg["lang"]][i]
def save(self):
self.cfg.update({"res": self.vr.get(), "fs": self.vfs.get(), "fps": self.vf.get(), "low": self.vl.get()})
json.dump(self.cfg, open(CFG_P, "w", encoding="utf-8"), indent=4)
def set_lang(self, c):
self.cfg["lang"] = c
self.save()
for k, b in self.lb.items():
b.configure(bg="#39FF14" if k == c else "#161B22", fg="#0D1117" if k == c else "#8B949E")
sec = int(self.cfg.get("sec", 0))
self.l_sub.config(text=self.t(0))
self.l_tm.config(text=self.t(1).format(h=sec // 3600, m=(sec % 3600) // 60))
for i, tx in enumerate(self.t(2)): self.nb.tab(i, text=tx)
self.l_sg.config(text=self.t(3))
self.l_gd.config(text=self.t(4))
self.b_sel.config(text=self.t(5))
self.upd_rom()
self.b_play.config(text=self.t(8))
self.l_res.config(text=self.t(10))
self.rbs[0].config(text=self.t(11))
self.l_prf.config(text=self.t(12))
self.c_fps.config(text=self.t(13))
self.c_low.config(text=self.t(14))
self.c_fs.config(text=self.t(15))
self.l_art.config(text=self.t(16))
self.b_csta.config(text=self.t(17))
self.b_rsta.config(text=self.t(18))
for ch in self.c3.winfo_children(): ch.destroy()
for k, d in self.t(20):
row = tk.Frame(self.c3, bg="#161B22")
row.pack(fill="x", pady=2)
tk.Label(row, text=k, font=("Consolas", 8, "bold"), bg="#0D1117", fg="#39FF14", width=16).pack(side="left", padx=(0, 10))
tk.Label(row, text=d, font=("Arial", 8), bg="#161B22", fg="#C9D1D9").pack(side="left")
def sel_game(self, idx, inst=False):
self.cfg["sel"] = idx
self.save()
for i, b in enumerate(self.gbtns):
b.configure(bg="#39FF14" if i == idx else "#21262D", fg="#0D1117" if i == idx else "#C9D1D9")
self.upd_rom()
self.load_art(inst)
def upd_rom(self):
p = self.cfg["paths"][self.cfg["sel"]]
self.l_rom.config(text=f"{self.t(7)}{os.path.basename(p)}" if p and os.path.exists(p) else self.t(6))
def pick_rom(self):
p = filedialog.askopenfilename(filetypes=[("PSP Game", ".iso .cso"), ("All", ".")])
if p:
self.cfg["paths"][self.cfg["sel"]] = p
self.save()
self.upd_rom()
def on_resize(self, e):
if e.width > 50 and e.height > 50:
self.aw, self.ah = e.width, e.height
self.load_art(True)
def load_art(self, inst=False):
c = self.cfg.get("art", "")
pt = c if (c and os.path.exists(c)) else rpath(os.path.join("assets", GAMES[self.cfg["sel"]][2]))
im = Image.open(pt).convert("RGB").resize((self.aw, self.ah), Image.Resampling.LANCZOS) if (PIL_OK and pt and os.path.exists(pt)) else None
if not im:
self.cv.delete("all")
self.cv.create_text(self.aw // 2, self.ah // 2, text="BEN 10\nTRILOGY PC", fill="#39FF14", font=("Arial", 14, "bold"), justify="center")
return
if self.fj: self.r.after_cancel(self.fj); self.fj = None
if inst or not self.pil:
self.pil = im
self.img = ImageTk.PhotoImage(im)
self.cv.delete("all")
self.cv.create_image(0, 0, anchor="nw", image=self.img)
else:
self.fade(self.pil, im, 1)
def fade(self, i1, i2, st):
if i1.size != i2.size: i1 = i1.resize(i2.size)
self.img = ImageTk.PhotoImage(Image.blend(i1, i2, st / 8.0))
self.cv.delete("all")
self.cv.create_image(0, 0, anchor="nw", image=self.img)
if st < 8: self.fj = self.r.after(28, lambda: self.fade(i1, i2, st + 1))
else: self.pil = i2; self.fj = None
def csta(self):
p = filedialog.askopenfilename(filetypes=[("Image", "*.png *.jpg *.jpeg *.webp")])
if p: self.cfg["art"] = p; self.save(); self.load_art()
def rsta(self):
self.cfg["art"] = ""; self.save(); self.load_art()
def sync_low(self):
low = self.vl.get()
for rb in self.rbs: rb.configure(state="disabled" if low else "normal")
if low: self.vr.set("1")
def tgl_low(self):
self.sync_low(); self.save()
def wcfg(self):
sd = os.path.join(BASE, "Engine", "memstick", "PSP", "SYSTEM")
os.makedirs(sd, exist_ok=True)
low, fps = self.cfg["low"], self.cfg["fps"]
res = "1" if low else {"1":"1","2":"3","3":"4","6":"8"}.get(str(self.cfg["res"]), "4")
lg = {"en":"1","ru":"11","de":"3","ja":"0"}.get(self.cfg["lang"], "1")
open(os.path.join(sd, "ppsspp.ini"), "w", encoding="utf-8").write(f"[General]\nFirstRun = False\nRunCount = 5\nEnableCheats = True\nPauseWhenMinimized = True\nIgnoreBadMemAccess = True\n[SystemParam]\nLanguage = {lg}\n[CPU]\nCPUCore = 1\nSeparateCPUThread = True\nFastMemory = True\nLockedCPUSpeed = {333 if fps else 222}\n[Graphics]\nGraphicsBackend = 0 (OPENGL)\nFullScreen = {self.cfg['fs']}\nInternalResolution = {res}\nFrameSkip = 0\nAutoFrameSkip = False\nHardwareTransform = True\nSoftwareSkinning = True\nAnisotropyLevel = {0 if low else 4}\nTexScalingLevel = {1 if low else 2}\n[Control]\nShowTouchControls = False\nMouseControl = True\n")
open(os.path.join(sd, "controls.ini"), "w", encoding="utf-8").write("[ControlMapping]\nUp = 1-38,1-49,10-19\nDown = 1-40,1-50,10-20\nLeft = 1-37,1-51,10-21\nRight = 1-39,1-52,10-22\nCircle = 1-16,1-76,10-97\nCross = 1-32,10-96\nSquare = 1-1000,1-74,10-99\nTriangle = 1-1001,1-75,10-100\nStart = 1-27,10-108\nSelect = 1-9,10-109\nL = 1-81,10-102\nR = 1-69,10-103\nAn.Up = 1-87,10-4003\nAn.Down = 1-83,10-4002\nAn.Left = 1-65,10-4001\nAn.Right = 1-68,10-4000\n")
def watch(self):
if not self.pr: return
if self.pr.poll() is None:
self.r.after(1000, self.watch)
return
self.cfg["sec"] = int(self.cfg.get("sec", 0)) + max(0, int(time.time() - self.t0))
self.save()
self.pr = None
self.r.deiconify()
self.set_lang(self.cfg["lang"])
self.b_play.configure(state="normal", text=self.t(8))
def play(self):
gp = self.cfg["paths"][self.cfg["sel"]]
if not gp or not os.path.exists(gp):
messagebox.showwarning("Warning", self.t(19))
return
self.b_play.configure(state="disabled", text=self.t(9))
self.r.update_idletasks()
try:
self.wcfg()
exe = os.path.join(BASE, "Engine", "Ben10Game.exe")
if not sys.platform.startswith("win"):
messagebox.showinfo("OK", "Config ready!")
self.b_play.configure(state="normal", text=self.t(8))
return
if not os.path.exists(exe):
messagebox.showerror("Error", "Engine/Ben10Game.exe not found.")
self.b_play.configure(state="normal", text=self.t(8))
return
self.t0 = time.time()
self.pr = subprocess.Popen([exe, "--fullscreen", gp])
self.r.withdraw()
self.r.after(1000, self.watch)
except Exception as e:
self.r.deiconify()
messagebox.showerror("Error", str(e))
self.b_play.configure(state="normal", text=self.t(8))
if name == "main":
root = tk.Tk()
TrilogyApp(root)
root.mainloop()
