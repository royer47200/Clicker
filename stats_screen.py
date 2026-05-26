import tkinter as tk

import config


def refresh_stats_tab(root):
    if not hasattr(root, "stats_diamonds_label"):
        return

    root.stats_diamonds_label.config(text=f"Diamants : {config.diamond}")
    root.stats_production_label.config(text=f"Production : {config.effective_production()}/s")
    root.stats_rebirth_label.config(text=f"Rebirth : {config.rebirth_count}")
    root.stats_bonus_label.config(text=f"Bonus rebirth : {int(config.rebirth_bonus_pct * 100)}%")
    root.stats_fortune_label.config(text=f"Fortune : x{config.bonus_strength}")

    root.achievements_list.delete(0, tk.END)
    for line in config.get_achievement_lines():
        root.achievements_list.insert(tk.END, line)


def create_stats_frame(root):
    frame = tk.Frame(root)

    back_button = tk.Button(frame, image=config.go_back_img, command=root.go_back, borderwidth=0)
    back_button.image = config.go_back_img
    back_button.place(x=20, y=20)

    stats_label = tk.Label(frame, text="Statistiques", font=("Arial", 20), fg="gold", bg="black")
    stats_label.pack(pady=20)

    root.stats_diamonds_label = tk.Label(frame, text=f"Diamants : {config.diamond}", fg="white", bg="black")
    root.stats_diamonds_label.pack(pady=5)

    root.stats_production_label = tk.Label(frame, text=f"Production : {config.effective_production()}/s", fg="white", bg="black")
    root.stats_production_label.pack(pady=5)

    root.stats_rebirth_label = tk.Label(frame, text=f"Rebirth : {config.rebirth_count}", fg="white", bg="black")
    root.stats_rebirth_label.pack(pady=5)

    root.stats_bonus_label = tk.Label(frame, text=f"Bonus rebirth : {int(config.rebirth_bonus_pct * 100)}%", fg="white", bg="black")
    root.stats_bonus_label.pack(pady=5)

    root.stats_fortune_label = tk.Label(frame, text=f"Fortune : x{config.bonus_strength}", fg="white", bg="black")
    root.stats_fortune_label.pack(pady=5)

    achievements_label = tk.Label(frame, text="Succès", font=("Arial", 16), fg="white", bg="black")
    achievements_label.pack(pady=10)

    root.achievements_list = tk.Listbox(frame, bg="black", fg="white")
    root.achievements_list.pack(fill="both", expand=True, padx=20, pady=10)

    return frame


def open_stats_tab(root, switch_window):
    if getattr(root, "stats_frame", None) is None:
        root.stats_frame = create_stats_frame(root)
    refresh_stats_tab(root)
    switch_window(root.stats_frame)
    return root.stats_frame
