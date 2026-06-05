import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import os, sys

def resource(name):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, name)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), name)

# ── Janela ─────────────────────────────────────────────────────
root = tk.Tk()
root.title("VS StatReelCounter")
root.configure(bg="#00ff00")
root.resizable(False, False)

# ── Fontes ─────────────────────────────────────────────────────
mono_val = tkfont.Font(family="Courier New", size=24, weight="bold", slant="italic")
mono_btn = tkfont.Font(family="Courier New", size=12, weight="bold")
mono_rst = tkfont.Font(family="Courier New", size=9,  weight="bold")

# ── Imagem de fundo ────────────────────────────────────────────
IMG_W, IMG_H = 420, 140
img_orig = Image.open(resource("VS_StatReelCounter.png")).resize((IMG_W, IMG_H), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(img_orig)
root.bg_photo = bg_photo  # evita garbage collection

# ── Exclamação ─────────────────────────────────────────────────
EXCL_SIZE = 40
excl_orig = Image.open(resource("exclamacao.png")).resize((EXCL_SIZE, EXCL_SIZE), Image.LANCZOS)
excl_photo = ImageTk.PhotoImage(excl_orig)
root.excl_photo = excl_photo  # evita garbage collection

# Frame superior para botões +
top_frame = tk.Frame(root, bg="#00ff00")
top_frame.pack(padx=10, pady=(10, 0))

canvas = tk.Canvas(root, width=IMG_W, height=IMG_H, highlightthickness=0, bg="#00ff00")
canvas.pack(padx=10, pady=0)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# Frame inferior para botões −
bot_frame = tk.Frame(root, bg="#00ff00")
bot_frame.pack(padx=10, pady=(0, 0))

# ── Dados ──────────────────────────────────────────────────────
STATS = ["STR", "INT", "AGL"]
stat_values = {s: 0 for s in STATS}

X_POS  = {"STR": 95, "INT": 200, "AGL": 305}
Y_VAL  = 80   # posição dos números
Y_EXCL = 20   # posição da exclamação (entre o texto da imagem e o botão +)
NORMAL = "#222222"

val_ids  = {}
excl_ids = {}

# ── Lógica ─────────────────────────────────────────────────────
def get_dominant():
    min_val = min(stat_values[s] for s in STATS)
    for s in STATS:
        if stat_values[s] == min_val:
            return s

def refresh():
    dominant = get_dominant()
    for s in STATS:
        canvas.itemconfig(val_ids[s], text=str(stat_values[s]), state="normal", fill=NORMAL)
        if s == dominant:
            canvas.itemconfig(excl_ids[s], state="normal")
        else:
            canvas.itemconfig(excl_ids[s], state="hidden")

def change(stat, delta):
    new_val = stat_values[stat] + delta
    if new_val < 0:
        return
    stat_values[stat] = new_val
    refresh()

def reset_all():
    for s in STATS:
        stat_values[s] = 0
    refresh()

# ── Desenha valores, exclamações e botões ──────────────────────
EXCL_OFFSET_X = 15  # ajuste esse valor até alinhar

for s in STATS:
    x = X_POS[s]

    # Valor numérico
    vid = canvas.create_text(x, Y_VAL, text="0", font=mono_val, fill=NORMAL, anchor="center")
    val_ids[s] = vid

    # Exclamação — entre o texto da imagem e o botão +
    eid = canvas.create_image(x + EXCL_OFFSET_X, Y_EXCL, image=excl_photo, anchor="center", state="hidden")
    excl_ids[s] = eid

    # Botão +
    btn_p = tk.Button(top_frame, text="+", font=mono_btn,
                      bg="#666660", fg="white", relief="flat",
                      width=2, cursor="hand2",
                      command=lambda st=s: change(st, +1))
    btn_p.place(x=x - 15, y=0)

    # Botão −
    btn_m = tk.Button(bot_frame, text="−", font=mono_btn,
                      bg="#666660", fg="white", relief="flat",
                      width=2, cursor="hand2",
                      command=lambda st=s: change(st, -1))
    btn_m.place(x=x - 15, y=0)

# Tamanho fixo dos frames
top_frame.config(width=IMG_W, height=35)
top_frame.pack_propagate(False)
bot_frame.config(width=IMG_W, height=35)
bot_frame.pack_propagate(False)

# ── Botão Reset ────────────────────────────────────────────────
reset_btn = tk.Button(
    root, text="↺  RESET",
    bg="#333330", fg="#aaaaaa",
    font=mono_rst, relief="flat",
    cursor="hand2", padx=8, pady=3,
    command=reset_all
)
reset_btn.pack(pady=(6, 12))

refresh()
root.mainloop()