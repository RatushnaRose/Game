# ─────────────────────────────────────────────
# ФУНКЦІЇ МАЛЮВАННЯ
# ─────────────────────────────────────────────


def draw_card(idx, color):
    # Намалювати картку з заданим кольором за її індексом.
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
    # Перемалювати всі картки відповідно до поточного стану.
    for i in range(TOTAL_CARDS):
        if state["matched"][i]:
            draw_card(i, CARD_MATCHED_COLOR)
        elif state["open"][i]:
            draw_card(i, BG_COLOR)
        else:
            draw_card(i, CARD_COLOR)


def show_overlay(message, color):
    # Показує повідомлення посередині поля (перемога або час вийшов).
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


