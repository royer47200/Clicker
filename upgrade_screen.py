import tkinter as tk

import config
import widgets


def set_button_image(button, text, bg_color):
    img = widgets.create_button_image(text, bg_color)
    button.config(image=img)
    button.image = img


def refresh_upgrade_menu(root):
    if not hasattr(root, "upgrade_status_label"):
        return

    root.upgrade_status_label.config(text="Sélectionnez une amélioration.")

    set_button_image(root.click_upgrade_button, f"Clic +1 ({config.get_upgrade_cost('click')})", "#3cb371")
    set_button_image(root.production_upgrade_button, f"Production +1 ({config.get_upgrade_cost('production')})", "#3cb371")
    set_button_image(root.fortune_upgrade_button, f"Bonus aléatoire ({config.get_upgrade_cost('fortune')})", "#3cb371")
    set_button_image(root.rebirth_button, f"Rebirth ({int(config.rebirth_threshold())})", "#ff8c00")

    for index, button in enumerate(root.slot_buttons):
        set_button_image(button, get_slot_label(index), "#5dade2")

    set_button_image(root.dirt_prod_button, f"Terre : +10% de prod ({config.get_building_upgrade_cost('dirt_farm', 'production')})", "#85c1e9")
    set_button_image(root.dirt_discount_button, f"Terre : -5% de prix ({config.get_building_upgrade_cost('dirt_farm', 'discount')})", "#82e0aa")
    set_button_image(root.cobblestone_prod_button, f"Cobblestone : +10% de prod ({config.get_building_upgrade_cost('cobblestone_farm', 'production')})", "#85c1e9")
    set_button_image(root.cobblestone_discount_button, f"Cobblestone : -5% de prix ({config.get_building_upgrade_cost('cobblestone_farm', 'discount')})", "#82e0aa")
    set_button_image(root.oak_prod_button, f"Chêne : +10% de prod ({config.get_building_upgrade_cost('oak_farm', 'production')})", "#85c1e9")
    set_button_image(root.oak_discount_button, f"Chêne : -5% de prix ({config.get_building_upgrade_cost('oak_farm', 'discount')})", "#82e0aa")
    set_button_image(root.coal_prod_button, f"Charbon : +10% de prod ({config.get_building_upgrade_cost('coal_farm', 'production')})", "#85c1e9")
    set_button_image(root.coal_discount_button, f"Charbon : -5% de prix ({config.get_building_upgrade_cost('coal_farm', 'discount')})", "#82e0aa")
    set_button_image(root.iron_prod_button, f"Fer : +10% de prod ({config.get_building_upgrade_cost('iron_farm', 'production')})", "#85c1e9")
    set_button_image(root.iron_discount_button, f"Fer : -5% de prix ({config.get_building_upgrade_cost('iron_farm', 'discount')})", "#82e0aa")
    set_button_image(root.diamond_prod_button, f"Diamant : +10% de prod ({config.get_building_upgrade_cost('diamondbat_farm', 'production')})", "#85c1e9")
    set_button_image(root.diamond_discount_button, f"Diamant : -5% de prix ({config.get_building_upgrade_cost('diamondbat_farm', 'discount')})", "#82e0aa")
    set_button_image(root.debris_prod_button, f"Débris : +10% de prod ({config.get_building_upgrade_cost('debris_farm', 'production')})", "#85c1e9")
    set_button_image(root.debris_discount_button, f"Débris : -5% de prix ({config.get_building_upgrade_cost('debris_farm', 'discount')})", "#82e0aa")


def create_upgrade_frame(root):
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    back_button = tk.Button(
        frame,
        text="Retour",
        bg="#3cb371",
        fg="white",
        font=("Arial", 14, "bold"),
        command=root.go_back,
        borderwidth=0,
        width=10,
        height=2,
    )
    back_button.place(x=20, y=20)

    title_label = tk.Label(frame, text="Améliorations", font=("Arial", 20), fg="gold", bg="black")
    title_label.pack(pady=10)

    root.upgrade_status_label = tk.Label(frame, text="Sélectionnez une amélioration.", fg="white", bg="black")
    root.upgrade_status_label.pack(fill="x", padx=20, pady=(0, 10))

    canvas = tk.Canvas(frame, bg="black", highlightthickness=0)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    upgrades_frame = tk.Frame(canvas, bg="black")
    canvas.create_window((0, 0), window=upgrades_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
    scrollbar.pack(side="right", fill="y")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    upgrades_frame.bind("<Configure>", on_frame_configure)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    upgrades_frame.bind_all("<MouseWheel>", _on_mousewheel)

    general_title = tk.Label(upgrades_frame, text="Améliorations générales", fg="white", bg="black", font=("Arial", 14))
    general_title.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

    root.click_upgrade_button = tk.Button(
        upgrades_frame,
        image=widgets.create_button_image(f"Clic +1 ({config.get_upgrade_cost('click')})", "#3cb371"),
        borderwidth=0,
        command=lambda: purchase_upgrade(root, "click"),
    )
    root.click_upgrade_button.image = root.click_upgrade_button.cget("image")
    root.click_upgrade_button.grid(row=1, column=0, padx=8, pady=8)

    root.production_upgrade_button = tk.Button(
        upgrades_frame,
        image=widgets.create_button_image(f"Production +1 ({config.get_upgrade_cost('production')})", "#3cb371"),
        borderwidth=0,
        command=lambda: purchase_upgrade(root, "production"),
    )
    root.production_upgrade_button.image = root.production_upgrade_button.cget("image")
    root.production_upgrade_button.grid(row=1, column=1, padx=8, pady=8)

    root.fortune_upgrade_button = tk.Button(
        upgrades_frame,
        image=widgets.create_button_image(f"Bonus aléatoire ({config.get_upgrade_cost('fortune')})", "#3cb371"),
        borderwidth=0,
        command=lambda: purchase_upgrade(root, "fortune"),
    )
    root.fortune_upgrade_button.image = root.fortune_upgrade_button.cget("image")
    root.fortune_upgrade_button.grid(row=1, column=2, padx=8, pady=8)

    root.rebirth_button = tk.Button(
        upgrades_frame,
        image=widgets.create_button_image(f"Rebirth ({int(config.rebirth_threshold())})", "#ff8c00"),
        borderwidth=0,
        command=lambda: rebirth(root),
    )
    root.rebirth_button.image = root.rebirth_button.cget("image")
    root.rebirth_button.grid(row=1, column=3, padx=8, pady=8)

    building_title = tk.Label(upgrades_frame, text="Améliorations par bâtiment", fg="white", bg="black", font=("Arial", 14))
    building_title.grid(row=2, column=0, columnspan=4, sticky="w", pady=(20, 10))

    buildings = [
        ("dirt_farm", "Terre", "dirt_prod_button", "dirt_discount_button"),
        ("cobblestone_farm", "Cobblestone", "cobblestone_prod_button", "cobblestone_discount_button"),
        ("oak_farm", "Chêne", "oak_prod_button", "oak_discount_button"),
        ("coal_farm", "Charbon", "coal_prod_button", "coal_discount_button"),
        ("iron_farm", "Fer", "iron_prod_button", "iron_discount_button"),
        ("diamondbat_farm", "Diamant", "diamond_prod_button", "diamond_discount_button"),
        ("debris_farm", "Débris", "debris_prod_button", "debris_discount_button"),
    ]

    for row_index, (building_name, label, prod_attr, discount_attr) in enumerate(buildings, start=3):
        name_label = tk.Label(upgrades_frame, text=label, fg="white", bg="black")
        name_label.grid(row=row_index, column=0, sticky="w", padx=8)

        prod_button = tk.Button(
            upgrades_frame,
            image=widgets.create_button_image(f"{label} : +10% prod", "#85c1e9"),
            borderwidth=0,
            command=lambda b=building_name: purchase_upgrade(root, f"{b.split('_')[0]}_prod" if b != "diamondbat_farm" else "diamondbat_prod"),
        )
        prod_button.image = prod_button.cget("image")
        prod_button.grid(row=row_index, column=1, padx=8, pady=6)

        discount_button = tk.Button(
            upgrades_frame,
            image=widgets.create_button_image(f"{label} : -5% prix", "#82e0aa"),
            borderwidth=0,
            command=lambda b=building_name: purchase_upgrade(root, f"{b.split('_')[0]}_discount" if b != "diamondbat_farm" else "diamondbat_discount"),
        )
        discount_button.image = discount_button.cget("image")
        discount_button.grid(row=row_index, column=2, padx=8, pady=6)

        setattr(root, prod_attr, prod_button)
        setattr(root, discount_attr, discount_button)

    root.slot_buttons = []
    slot_title = tk.Label(upgrades_frame, text="Slots permanents", fg="white", bg="black", font=("Arial", 14))
    slot_title.grid(row=10, column=0, columnspan=4, sticky="w", pady=(20, 10))

    for index in range(3):
        if index == 0:
            font_size = 16
            width = 270
        else:
            font_size = 11
            width = 340
        slot_button = tk.Button(
            upgrades_frame,
            image=widgets.create_button_image(get_slot_label(index), "#5dade2", width=width, font_size=font_size),
            borderwidth=0,
            command=lambda i=index: purchase_upgrade(root, f"slot_{i + 1}"),
        )
        slot_button.image = slot_button.cget("image")
        slot_button.grid(row=11 + index, column=0, columnspan=4, padx=8, pady=6)
        root.slot_buttons.append(slot_button)

    return frame


def open_upgrade_menu(root, switch_window):
    if getattr(root, "upgrade_frame", None) is None:
        root.upgrade_frame = create_upgrade_frame(root)
    switch_window(root.upgrade_frame)
    refresh_upgrade_menu(root)
    return root.upgrade_frame


def purchase_upgrade(root, name):
    if name == "click":
        success, message = config.buy_upgrade("click")
    elif name == "production":
        success, message = config.buy_upgrade("production")
    elif name == "fortune":
        success, message = config.buy_upgrade("fortune")
    elif name == "slot_1":
        success, message = config.buy_slot_upgrade(0)
    elif name == "slot_2":
        success, message = config.buy_slot_upgrade(1)
    elif name == "slot_3":
        success, message = config.buy_slot_upgrade(2)
    elif name == "dirt_prod":
        success, message = config.buy_building_upgrade("dirt_farm", "production")
    elif name == "dirt_discount":
        success, message = config.buy_building_upgrade("dirt_farm", "discount")
    elif name == "cobblestone_prod":
        success, message = config.buy_building_upgrade("cobblestone_farm", "production")
    elif name == "cobblestone_discount":
        success, message = config.buy_building_upgrade("cobblestone_farm", "discount")
    elif name == "oak_prod":
        success, message = config.buy_building_upgrade("oak_farm", "production")
    elif name == "oak_discount":
        success, message = config.buy_building_upgrade("oak_farm", "discount")
    elif name == "coal_prod":
        success, message = config.buy_building_upgrade("coal_farm", "production")
    elif name == "coal_discount":
        success, message = config.buy_building_upgrade("coal_farm", "discount")
    elif name == "iron_prod":
        success, message = config.buy_building_upgrade("iron_farm", "production")
    elif name == "iron_discount":
        success, message = config.buy_building_upgrade("iron_farm", "discount")
    elif name == "diamondbat_prod":
        success, message = config.buy_building_upgrade("diamondbat_farm", "production")
    elif name == "diamondbat_discount":
        success, message = config.buy_building_upgrade("diamondbat_farm", "discount")
    elif name == "debris_prod":
        success, message = config.buy_building_upgrade("debris_farm", "production")
    elif name == "debris_discount":
        success, message = config.buy_building_upgrade("debris_farm", "discount")
    else:
        success, message = False, "Amélioration inconnue."

    root.upgrade_status_label.config(text=message)
    root.update_hud()


def rebirth(root):
    if config.diamond < config.rebirth_threshold():
        root.upgrade_status_label.config(text=f"Rebirth bloqué : il vous faut {int(config.rebirth_threshold())} diamants.")
        return

    config.rebirth_progress()
    root.update_hud()
    root.upgrade_status_label.config(text="Renaissance réussie ! Vos bâtiments repartent à zéro, mais vos bonus de rebirth augmentent.")

# Mapping slot type to user-friendly label
_SLOT_LABELS = {
    "global_click": "+1 clic",
    "global_production": "+1 production",
    "global_fortune": "+1 bonus aléatoire",
}

def get_slot_label(index):
    slot_types = getattr(config, "permanent_slots", ["global_click", "global_production", "global_fortune"])
    slot_type = slot_types[index] if index < len(slot_types) else "global_click"
    label = _SLOT_LABELS.get(slot_type, "+1 bonus")
    return f"Slot {index+1} : {label}"
