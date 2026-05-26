import tkinter as tk

import config
import widgets


def set_button_image(button, text, bg_color):
    img = widgets.create_button_image(text, bg_color)
    button.config(image=img)
    button.image = img


def refresh_shop_frame(root):
    if not hasattr(root, "shop_info_labels"):
        return

    selected_building = getattr(root, "shop_selected_building", None)
    if selected_building is None:
        selected_building = next(iter(config.building_stats.values()))

    labels = root.shop_info_labels
    if not labels:
        return

    labels[0].config(
        text=f"Prix : {selected_building.get_price(config.building_price_reduction[selected_building.name])} diamants ; Production : {selected_building.get_production()}/s"
    )


def create_shop_frame(root):
    frame = tk.Frame(root)

    background_label = tk.Label(frame, image=root.background)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.lower()

    title_label = tk.Label(frame, text="Boutique des bâtiments", fg="gold", bg="black", font=("Arial", 18))
    title_label.pack(pady=10)

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

    building_display_names = {
        "dirt_farm": "Terre",
        "cobblestone_farm": "Cobblestone",
        "oak_farm": "Chêne",
        "coal_farm": "Charbon",
        "iron_farm": "Fer",
        "diamondbat_farm": "Diamant",
        "debris_farm": "Débris",
    }

    building_order = [
        "dirt_farm",
        "cobblestone_farm",
        "oak_farm",
        "coal_farm",
        "iron_farm",
        "diamondbat_farm",
        "debris_farm",
    ]

    root.shop_selected_building = config.dirt_building_stats
    root.shop_building_var = tk.StringVar(value=building_display_names[root.shop_selected_building.name])

    building_dropdown = tk.OptionMenu(
        frame,
        root.shop_building_var,
        *[building_display_names[name] for name in building_order],
        command=lambda value: root.shop_select_building(value),
    )
    building_dropdown.pack(pady=10)

    building_image_label = tk.Label(frame, image=config.dirt_building_img)
    building_image_label.pack(pady=10)
    root.shop_building_image_label = building_image_label

    info_label = tk.Label(
        frame,
        text=f"Prix : {config.dirt_building_stats.get_price()} diamants ; Production : {config.dirt_building_stats.get_production()}/s",
        fg="white",
        bg="black",
    )
    info_label.pack(pady=10)
    root.shop_info_labels = [info_label]

    button_frame = tk.Frame(frame, bg="black")
    button_frame.pack(pady=10)

    for quantity in (1, 10, 100):
        button = tk.Button(
            button_frame,
            text=f"Acheter {quantity}",
            command=lambda q=quantity: root.buying(root.shop_selected_building, q),
        )
        button.pack(side="left", padx=10)

    building_images = {
        "dirt_farm": config.dirt_building_img,
        "cobblestone_farm": config.cobblestone_img,
        "oak_farm": config.oak_img,
        "coal_farm": config.coal_img,
        "iron_farm": config.iron_img,
        "diamondbat_farm": config.diamondbat_img,
        "debris_farm": config.debris_img,
    }

    def update_shop_selection(value):
        selected_name = next(name for name, label in building_display_names.items() if label == value)
        root.shop_selected_building = config.building_stats[selected_name]
        root.shop_building_image_label.config(image=building_images[selected_name])
        root.shop_info_labels[0].config(
            text=f"Prix : {root.shop_selected_building.get_price(config.building_price_reduction[root.shop_selected_building.name])} diamants ; Production : {root.shop_selected_building.get_production()}/s"
        )

    root.shop_select_building = update_shop_selection
    update_shop_selection(root.shop_building_var.get())

    return frame


def open_shop_menu(root, switch_window):
    if getattr(root, "shop_frame", None) is None:
        root.shop_frame = create_shop_frame(root)
    switch_window(root.shop_frame)
    return root.shop_frame
