import config
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk, ImageFont

_BUTTON_IMAGE_CACHE = {}


def create_button_image(text, bg_color, width=220, height=55, fg_color="white", font_size=16):
    """Génère une image stylisée pour un bouton du jeu."""
    cache_key = (text, bg_color, width, height, fg_color, font_size)
    if cache_key in _BUTTON_IMAGE_CACHE:
        return _BUTTON_IMAGE_CACHE[cache_key]

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, width - 1, height - 1), radius=14, fill=bg_color)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()
    # Mesure la taille du texte de façon compatible Pillow
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except Exception:
        w, h = font.getsize(text)
    draw.text(((width - w) / 2, (height - h) / 2), text, fill=fg_color, font=font)
    photo = ImageTk.PhotoImage(img)
    _BUTTON_IMAGE_CACHE[cache_key] = photo
    return photo


def create_hud(root):
    """Crée la barre HUD affichant les informations principales du joueur."""
    diamond_score = tk.Label(root.hud, text=f"Diamants = {config.diamond}")
    diamond_score.pack(side="left", padx=10)

    diamond_prod = tk.Label(root.hud, text=f"Production = {config.effective_production()}/s")
    diamond_prod.pack(side="left", padx=10)

    rebirth_label = tk.Label(root.hud, text=f"Rebirth = {config.rebirth_count}")
    rebirth_label.pack(side="left", padx=10)

    buff_label = tk.Label(root.hud, text="Bonus = aucun")
    buff_label.pack(side="left", padx=10)

    root.diamond_score_label = diamond_score
    root.diamond_prod_label = diamond_prod
    root.rebirth_label = rebirth_label
    root.buff_label = buff_label


def create_start_frame(root):
    """Construit l'écran de démarrage du jeu."""
    frame = tk.Frame(root)

    background = ImageTk.PhotoImage(Image.open(config.background_path))
    root.background = background
    background_label = tk.Label(frame, image=root.background)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.lower()

    start_button = tk.Button(frame, text="Commencez à jouer", bg="green", height=8, command=root.start)
    start_button.pack(expand="yes", fill="x")

    return frame


def create_game_frame(root):
    """Construit l'écran principal où l'on clique et gère les menus."""
    frame = tk.Frame(root)

    background_label = tk.Label(frame, image=root.background)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.lower()

    diamond_clicker = tk.Button(frame, image=config.diamond_img, command=root.click)
    diamond_clicker.place(x=0, y=0)

    bat_button = tk.Button(frame, image=config.bat_img, command=root.shop_menu)
    bat_button.place(x=0, y=500)

    upgrade_img = create_button_image("Améliorations", "#ffd700", width=240, height=65, font_size=20)
    upgrade_button = tk.Button(frame, image=upgrade_img, command=root.upgrade_menu, borderwidth=0)
    upgrade_button.image = upgrade_img
    upgrade_button.place(x=930, y=500)

    # Bouton Statistiques plus grand et plus coloré
    stats_img = create_button_image("Statistiques", "#5dade2", width=220, height=60, font_size=18)
    stats_button = tk.Button(frame, image=stats_img, borderwidth=0)
    stats_button.image = stats_img
    stats_button.place(x=700, y=500)
    root.stats_button = stats_button

    reset_img = create_button_image("Réinitialiser", "#cc4444", width=150, height=45, fg_color="white", font_size=16)
    reset_button = tk.Button(frame, image=reset_img, command=root.reset_game, borderwidth=0)
    reset_button.image = reset_img
    reset_button.place(x=1120, y=10)

    # Bouton bonus aléatoire corrigé (centré, police plus grande, largeur adaptée)
    bonus_img = create_button_image("Bonus aléatoire", "#3cb371", width=250, height=60, fg_color="white", font_size=18)
    random_bonus_button = tk.Button(frame, image=bonus_img, text="", compound="center", borderwidth=0, relief="flat", font=("Arial", 16), fg="white", bg="#3cb371")
    random_bonus_button.image = bonus_img
    random_bonus_button.place_forget()
    root.random_bonus_button = random_bonus_button

    return frame



