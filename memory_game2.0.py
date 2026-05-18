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
    state["matched"]   = [False] * TOTAL_CARDS
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

    if secs <= 0:
        # час вийшов!
        state["game_over"] = True
        state["locked"]    = True
        show_overlay("⏰ Час вийшов!", "#d32f2f")
        return

    state["time_left"] -= 1
    state["timer_id"] = root.after(1000, tick)  # наступний тік через 1 секунду


# ─────────────────────────────────────────────
# ФУНКЦІЇ МАЛЮВАННЯ
# ─────────────────────────────────────────────

def draw_card(idx, color):
    """Намалювати картку з заданим кольором за її індексом."""
    row = idx // GRID_COLS
    col = idx %  GRID_COLS

    x1 = CARD_GAP + col * (CARD_SIZE + CARD_GAP)
    y1 = CARD_GAP + row * (CARD_SIZE + CARD_GAP)
    x2 = x1 + CARD_SIZE
    y2 = y1 + CARD_SIZE

    canvas.delete(f"card_{idx}")

    if CARD_SHAPE == "oval":
        canvas.create_oval(x1, y1, x2, y2,
                           fill=color, outline=CARD_OUTLINE, width=2,
                           tags=f"card_{idx}")
    else:
        canvas.create_rectangle(x1, y1, x2, y2,
                                fill=color, outline=CARD_OUTLINE, width=2,
                                tags=f"card_{idx}")

    # показуємо символ тільки для відкритих або знайдених карток
    if state["open"][idx] or state["matched"][idx]:
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        canvas.create_text(cx, cy,
                           text=pairs[idx],
                           font=(FONT_NAME, FONT_SIZE),
                           fill=FONT_COLOR,
                           tags=f"card_{idx}")


def redraw_all():
    """Перемалювати всі картки відповідно до поточного стану."""
    for i in range(TOTAL_CARDS):
        if state["matched"][i]:
            draw_card(i, CARD_MATCHED_COLOR)
        elif state["open"][i]:
            draw_card(i, CARD_OPEN_COLOR)
        else:
            draw_card(i, CARD_COLOR)


def show_overlay(message, color):
    """Показує повідомлення посередині поля (перемога або час вийшов)."""
    cx = CANVAS_W // 2
    cy = CANVAS_H // 2
    canvas.create_rectangle(cx - 170, cy - 55, cx + 170, cy + 55,
                             fill="#fce4ec", outline=color, width=4,
                             tags="overlay")
    canvas.create_text(cx, cy - 12,
                        text=message,
                        font=("Arial", 18, "bold"),
                        fill=color,
                        tags="overlay")
    canvas.create_text(cx, cy + 28,
                        text='Натисни "Нова гра" для перезапуску',
                        font=("Arial", 11),
                        fill="#880e4f",
                        tags="overlay")


# ─────────────────────────────────────────────
# ЛОГІКА ГРИ
# ─────────────────────────────────────────────

def get_card_idx(x, y):
    """Повертає індекс картки за координатами миші, або None."""
    for i in range(TOTAL_CARDS):
        row = i // GRID_COLS
        col = i %  GRID_COLS
        x1 = CARD_GAP + col * (CARD_SIZE + CARD_GAP)
        y1 = CARD_GAP + row * (CARD_SIZE + CARD_GAP)
        x2 = x1 + CARD_SIZE
        y2 = y1 + CARD_SIZE
        if x1 <= x <= x2 and y1 <= y <= y2:
            return i
    return None


def on_click(event):
    """Обробник лівого кліку — відкриває картку."""
    if state["locked"] or state["game_over"]:
        return

    idx = get_card_idx(event.x, event.y)
    if idx is None:
        return
    if state["matched"][idx] or state["open"][idx]:
        return

    state["open"][idx] = True
    draw_card(idx, CARD_OPEN_COLOR)

    if state["first"] is None:
        # перша картка ходу
        state["first"] = idx
    else:
        # друга картка — перевіряємо пару
        first = state["first"]
        state["first"] = None
        state["locked"] = True

        if pairs[first] == pairs[idx]:
            # пара знайдена!
            state["matched"][first] = True
            state["matched"][idx]   = True
            state["open"][first]    = False
            state["open"][idx]      = False
            state["locked"]         = False
            draw_card(first, CARD_MATCHED_COLOR)
            draw_card(idx,   CARD_MATCHED_COLOR)
            check_win()
        else:
            # пара не збіглась — перевернути назад через затримку
            root.after(FLIP_DELAY, lambda: flip_back(first, idx))


def flip_back(first, second):
    """Перевертає дві картки назад після невдалої спроби."""
    state["open"][first]  = False
    state["open"][second] = False
    state["locked"]       = False
    draw_card(first,  CARD_COLOR)
    draw_card(second, CARD_COLOR)


def check_win():
    """Перевіряє, чи гра закінчена."""
    if all(state["matched"]):
        state["game_over"] = True
        # зупиняємо таймер
        if state["timer_id"] is not None:
            root.after_cancel(state["timer_id"])
        show_overlay("♥ Вітаємо! Ви перемогли! ♥", "#880e4f")


def on_hover(event):
    """Підсвічує картку при наведенні миші."""
    if state["locked"] or state["game_over"]:
        return

    idx = get_card_idx(event.x, event.y)
    for i in range(TOTAL_CARDS):
        if state["matched"][i] or state["open"][i]:
            continue
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
