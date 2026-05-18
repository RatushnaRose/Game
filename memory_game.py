import tkinter as tk
import random

# ─────────────────────────────────────────────
# НАЛАШТУВАННЯ ГРИ — змінюй тут
# ─────────────────────────────────────────────

GRID_ROWS = 4          # кількість рядків
GRID_COLS = 4          # кількість стовпців

CARD_SIZE  = 80        # розмір сторони/діаметра картки в пікселях
CARD_GAP   = 14        # відстань між картками

CARD_SHAPE = "rect"    # форма картки: "rect" — квадрат, "oval" — коло

BG_COLOR           = "#fce4ec"   # блідо-рожевий фон
CARD_COLOR         = "#f48fb1"   # закрита картка (рожева)
CARD_HOVER_COLOR   = "#f06292"   # наведення миші (яскравіша рожева)
CARD_OPEN_COLOR    = "#fff9c4"   # відкрита картка (кремово-жовта)
CARD_MATCHED_COLOR = "#ce93d8"   # знайдена пара (бузкова)
CARD_OUTLINE       = "#e91e63"   # обведення карток
PANEL_COLOR        = "#f8bbd0"   # панель зверху/знизу

# текст на картках
FONT_NAME  = "Arial"
FONT_SIZE  = 28
FONT_COLOR = "#880e4f"   # темно-малиновий

# таймер та кнопки
TIMER_SECONDS    = 60            # час на гру в секундах
TIMER_WARN_SECS  = 10            # за скільки секунд до кінця таймер стає червоним
TIMER_FONT       = ("Arial", 20, "bold")
TIMER_COLOR      = "#880e4f"
TIMER_WARN       = "#d32f2f"     # колір таймера коли <= TIMER_WARN_SECS
BTN_BG         = "#e91e63"     # фон кнопки "Нова гра"
BTN_FG         = "#ffffff"     # текст кнопки
BTN_FONT       = ("Arial", 13, "bold")

FLIP_DELAY = 900  # мс — затримка перед тим як перевернути картки назад

# символи-пари (потрібно >= GRID_ROWS*GRID_COLS//2 штук)
SYMBOLS = ["♥", "✿", "★", "♛", "♫", "☁", "✦", "❋", "☘", "❀"]

# ─────────────────────────────────────────────
# РОЗРАХУНОК РОЗМІРІВ
# ─────────────────────────────────────────────

TOTAL_CARDS = GRID_ROWS * GRID_COLS
CANVAS_W    = GRID_COLS * (CARD_SIZE + CARD_GAP) + CARD_GAP
CANVAS_H    = GRID_ROWS * (CARD_SIZE + CARD_GAP) + CARD_GAP


# ─────────────────────────────────────────────
# СТАН ГРИ
# ─────────────────────────────────────────────

state = {
    "open":       [False] * TOTAL_CARDS,
    "matched":    [False] * TOTAL_CARDS,
    "first":      None,
    "locked":     False,
    "timer_id":   None,   # id планувальника таймера
    "time_left":  TIMER_SECONDS,
    "game_over":  False,
}

pairs = []  # заповнюється в new_game()


# ─────────────────────────────────────────────
# НОВА ГРА — скидання стану
# ─────────────────────────────────────────────

def new_game():
    """Починає нову гру: перемішує картки, скидає стан, запускає таймер."""

    global pairs

    # скасовуємо попередній таймер якщо є
    if state["timer_id"] is not None:
        root.after_cancel(state["timer_id"])

    # скидаємо стан
    state["open"]      = [False] * TOTAL_CARDS
    state["first"]     = None
    state["locked"]    = False
    state["time_left"] = TIMER_SECONDS
    state["game_over"] = False

    # перемішуємо символи
    selected = SYMBOLS[: TOTAL_CARDS // 2]  # рівно половина — унікальні символи
    pairs = selected * 2                     # кожен символ зустрічається двічі
    random.shuffle(pairs)

    # оновлюємо поле
    canvas.delete("all")
    redraw_all()
    # запускаємо таймер
    tick()

# ─────────────────────────────────────────────
# ТАЙМЕР
# ─────────────────────────────────────────────
def tick():
        """Щосекундно зменшує лічильник часу."""
        if state["game_over"]:
            return

        # оновлюємо підпис
        secs = state["time_left"]
        mins = secs // 60
        sec_part = secs % 60
        label_timer.config(
            text=f"⏱ {mins:01d}:{sec_part:02d}",
            fg=TIMER_WARN if secs <= TIMER_WARN_SECS else TIMER_COLOR
        )
        if secs == 0:
            # час вийшов!
            state["game_over"] = True
            state["locked"] = True
            show_overlay("⏰ Час вийшов!", "#d32f2f")
            return

        state["time_left"] -= 1
        state["timer_id"] = root.after(1000, tick)

def draw_card(idx, color):
    pass

def redraw_all():
   pass


def show_overlay(message, color):
    pass

def get_card_idx(x, y):
    pass


def on_click(event):
    pass

def flip_back(f, s):
    state["open"][f] = state["open"][s] = False
    state["locked"] = False
    draw_card(f, CARD_COLOR);
    draw_card(s, CARD_COLOR)

def check_win():
    """Перевіряє, чи гра закінчена."""
    if all(state["matched"]):
        state["game_over"] = True
        # зупиняємо таймер
        if state["timer_id"] is not None:
            root.after_cancel(state["timer_id"])
        show_overlay("♥️ Вітаємо! Ви перемогли! ♥️", "#880e4f")

def on_hover(event):
    if state["locked"] or state["game_over"]:
        return

    idx = get_card_idx(event.x, event.y)
    for i in range(TOTAL_CARDS):
        if not (state["matched"][i] or state["open"][i]):
            draw_card(i, CARD_HOVER_COLOR if i == idx else CARD_COLOR)

# ─────────────────────────────────────────────
# ПОБУДОВА ВІКНА
# ─────────────────────────────────────────────

root = tk.Tk()
root.title("Гра на пам ять")
root.resizable(False, False)
root.configure(bg=PANEL_COLOR)

# ── верхня панель: назва + таймер ────────────
top_frame = tk.Frame(root, bg=PANEL_COLOR)
top_frame.pack(fill="x", padx=10, pady=(8, 0))

label_title = tk.Label(top_frame, text="✿  Гра на пам ять  ✿",
                       font=("Arial", 16, "bold"),
                       bg=PANEL_COLOR, fg="#880e4f")
label_title.pack(side="left")

label_timer = tk.Label(top_frame, text="⏱ 1:00",
                       font=TIMER_FONT, bg=PANEL_COLOR, fg=TIMER_COLOR)
label_timer.pack(side="right")

# ── ігровий холст ─────────────────────────────
canvas = tk.Canvas(root, width=CANVAS_W, height=CANVAS_H,
                   bg=BG_COLOR, highlightthickness=0)
canvas.pack(padx=10, pady=8)

# ── нижня панель: кнопка ─────────────────────
bottom_frame = tk.Frame(root, bg=PANEL_COLOR)
bottom_frame.pack(fill="x", padx=10, pady=(0, 10))

btn_new = tk.Button(bottom_frame, text="Нова гра",
                    font=BTN_FONT, bg=BTN_BG, fg=BTN_FG,
                    activebackground="#c2185b", activeforeground="#ffffff",
                    relief="flat", padx=16, pady=6,
                    command=new_game)
btn_new.pack()

# підв язуємо події миші
canvas.bind("<Button-1>", on_click)
canvas.bind("<Motion>",   on_hover)

# запускаємо першу гру
new_game()

root.mainloop()
