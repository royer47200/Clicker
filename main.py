import random
import tkinter as tk

window = tk.Tk()
window.geometry("1280x720")
window.minsize(1280, 720)
window.maxsize(1280, 720)
window.title("Minecraft clicker")

import tkinter.messagebox as messagebox

import config
import shop_screen
import stats_screen
import upgrade_screen
import widgets

window.iconbitmap(config.game_path)
config.load_game()


def on_close():
    config.save_game()
    window.destroy()


window.protocol("WM_DELETE_WINDOW", on_close)


def switch_window(frame):
    """Masque les autres écrans et affiche l'écran demandé."""
    for other_frame in (frame_start, frame_game, frame_shop, frame_upgrades, frame_stats):
        if other_frame is not None:
            other_frame.pack_forget()
    frame.pack(fill="both", expand=True)
    window.current_screen = frame


def update_hud():
    """Rafraîchit les labels principaux et sauvegarde l'état du jeu."""
    window.diamond_score_label.config(text=f"Diamants = {config.diamond}")
    window.diamond_prod_label.config(text=f"Production = {config.effective_production()}/s")
    window.rebirth_label.config(text=f"Rebirth = {config.rebirth_count}")

    if config.bonus_click_timer > 0:
        window.buff_label.config(text=f"Bonus clic actif ({config.bonus_click_timer}s)")
    elif config.bonus_production_timer > 0:
        window.buff_label.config(text=f"Bonus production actif ({config.bonus_production_timer}s)")
    else:
        window.buff_label.config(text="Bonus = aucun")

    if window.current_screen is frame_shop:
        shop_screen.refresh_shop_frame(window)
    if window.current_screen is frame_upgrades:
        upgrade_screen.refresh_upgrade_menu(window)
    if window.current_screen is frame_stats:
        stats_screen.refresh_stats_tab(window)

    window.save_counter = getattr(window, "save_counter", 0) + 1
    if window.save_counter >= 10:
        config.save_game()
        window.save_counter = 0


def screen_actualize():
    """Met à jour la production passive et l'UI chaque seconde."""
    if not config.game_is_running:
        return

    earned = config.effective_production()
    config.diamond += earned
    config.total_diamonds_earned += earned
    config.tick_buffs()
    config.check_achievements()
    update_hud()
    window.after(1000, screen_actualize)


def start():
    """Lance la partie et démarre les boucles de jeu."""
    config.game_is_running = True
    switch_window(frame_game)

    if not getattr(window, "game_loop_started", False):
        window.game_loop_started = True
        window.after(1000, screen_actualize)

    if not getattr(window, "bonus_loop_started", False):
        window.bonus_loop_started = True
        window.after(10000, spawn_random_bonus)


def hide_random_bonus():
    """Cache le bouton de bonus aléatoire à l'écran."""
    window.random_bonus_button.place_forget()
    window.random_bonus_button.config(text="")


def spawn_random_bonus():
    """Fait apparaître périodiquement un bonus aléatoire."""
    if not config.game_is_running:
        return

    def apply_bonus(action):
        if action == "diamonds":
            reward = int(40 * config.bonus_strength * config.rebirth_cash_bonus)
            config.diamond += reward
            config.total_diamonds_earned += reward
        elif action == "click":
            config.bonus_click = 1
            config.bonus_click_timer = 10
        elif action == "production":
            config.bonus_production = 2
            config.bonus_production_timer = 10

        config.check_achievements()
        hide_random_bonus()
        update_hud()

    action = random.choice(["diamonds", "click", "production"])

    if action == "diamonds":
        text = f"+{int(40 * config.bonus_strength * config.rebirth_cash_bonus)} diamants"
    elif action == "click":
        text = "Bonus clic x2 10s"
    else:
        text = "Bonus prod +2/s 10s"

    img = widgets.create_button_image(text, "#3cb371", width=250, height=60, fg_color="white", font_size=18)
    window.random_bonus_button.config(image=img, text="", command=lambda action=action: apply_bonus(action))
    window.random_bonus_button.image = img
    window.random_bonus_button.place(x=random.randint(100, 900), y=random.randint(120, 500))
    window.after(7000, hide_random_bonus)
    window.after(10000, spawn_random_bonus)


def click():
    """Gère un clic sur le diamant principal et met à jour l'UI."""
    current_click = config.effective_click_multiplier()
    config.diamond += current_click
    config.total_clicks += 1
    config.total_diamonds_earned += current_click
    config.check_achievements()
    update_hud()


def shop_menu():
    """Affiche la boutique des bâtiments."""
    global frame_shop
    frame_shop = shop_screen.open_shop_menu(window, switch_window)


def buying(building, quantity=1):
    """Achète un bâtiment via la boutique, avec quantité optionnelle."""
    success, message = config.buy_building(building, quantity)
    if success:
        update_hud()
    else:
        window.buff_label.config(text=message)


def upgrade_menu():
    """Affiche le menu des améliorations."""
    global frame_upgrades
    frame_upgrades = upgrade_screen.open_upgrade_menu(window, switch_window)


def purchase_upgrade(name):
    """Traite l'achat d'une amélioration depuis l'écran d'améliorations."""
    upgrade_screen.purchase_upgrade(window, name)


def rebirth():
    """Effectue un rebirth si le seuil requis est atteint."""
    upgrade_screen.rebirth(window)


def go_back():
    """Retourne au gameplay principal depuis les menus secondaires."""
    switch_window(frame_game)


def reset_game():
    """Supprime la sauvegarde et relance une partie neuve."""
    if not messagebox.askyesno("Réinitialiser la partie", "Supprimer la sauvegarde et recommencer à zéro ?"):
        return

    config.reset_save()
    window.game_loop_started = False
    window.bonus_loop_started = False
    hide_random_bonus()
    switch_window(frame_start)
    update_hud()


window.go_back = go_back
window.reset_game = reset_game
window.start = start
window.click = click
window.shop_menu = shop_menu
window.buying = buying
window.upgrade_menu = upgrade_menu
window.purchase_upgrade = purchase_upgrade
window.rebirth = rebirth
window.update_hud = update_hud

hud = tk.Frame(window)
hud.pack(fill="x")
window.hud = hud
widgets.create_hud(window)
window.current_screen = None
window.save_counter = 0

frame_shop = None
frame_upgrades = None
frame_stats = None


def show_stats_tab():
    global frame_stats
    frame_stats = stats_screen.open_stats_tab(window, switch_window)


window.show_stats_tab = show_stats_tab

frame_start = widgets.create_start_frame(window)
frame_game = widgets.create_game_frame(window)
window.stats_button.config(command=window.show_stats_tab)

switch_window(frame_start)

window.mainloop()
