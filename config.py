import json
import pathlib
from PIL import Image, ImageTk

BASE_DIR = pathlib.Path(__file__).parent
IMG_DIR = BASE_DIR / "icons"
SAVE_PATH = BASE_DIR / "save.txt"

game_path = IMG_DIR / "icon.ico"
diamond_path = IMG_DIR / "diamant.png"
shop_path = IMG_DIR / "shop.png"
dirt_farm = IMG_DIR / "dirt_farm_img.png"
cobblestone_path = IMG_DIR / "cobblestone_farm.png"
oak_path = IMG_DIR / "oak_farm.png"
coal_path = IMG_DIR / "coal_farm.png"
iron_path = IMG_DIR / "iron_farm.png"
diamondbat_path = IMG_DIR / "diamondbat_farm.png"
debris_path = IMG_DIR / "debris_farm.png"
background_path = IMG_DIR / "background.png"
go_back_path = IMG_DIR / "retour.png"

# Open all images so they remain alive while the UI is running.
diamond_img = ImageTk.PhotoImage(Image.open(diamond_path))
bat_img = ImageTk.PhotoImage(Image.open(shop_path))

dirt_building_img = ImageTk.PhotoImage(Image.open(dirt_farm))
cobblestone_img = ImageTk.PhotoImage(Image.open(cobblestone_path))
oak_img = ImageTk.PhotoImage(Image.open(oak_path))
coal_img = ImageTk.PhotoImage(Image.open(coal_path))
iron_img = ImageTk.PhotoImage(Image.open(iron_path))
diamondbat_img = ImageTk.PhotoImage(Image.open(diamondbat_path))
debris_img = ImageTk.PhotoImage(Image.open(debris_path))

go_back_img = ImageTk.PhotoImage(Image.open(go_back_path))


class Building:
    """Représente un bâtiment du jeu et sa progression."""
    def __init__(self, name, base_price, production):
        self.name = name
        self.base_price = base_price
        self.price = base_price
        self.production = production
        self.amount = 0

    def get_name(self):
        """Retourne le nom du bâtiment."""
        return self.name

    def get_price(self, discount=0.0):
        """Calcule le prix du bâtiment en tenant compte d'une réduction."""
        return max(1, int(self.price * (1 - discount)))

    def get_production(self):
        """Retourne la production de base du bâtiment."""
        return self.production

    def get_amount(self):
        """Retourne la quantité possédée du bâtiment."""
        return self.amount

    def buy(self):
        """Ajoute un bâtiment et augmente son coût de réachat."""
        self.amount += 1
        self.price = int(self.base_price * (1.18 ** self.amount))

    def reset(self):
        """Réinitialise le bâtiment au début d'une renaissance."""
        self.amount = 0
        self.price = self.base_price


# Game state
diamond = 0
click_multiplier = 1
diamond_prod = 0
rebirth_count = 0
rebirth_points = 0
rebirth_bonus_pct = 0.0
rebirth_cash_bonus = 1.0
bonus_strength = 1
bonus_click = 0
bonus_production = 0
bonus_click_timer = 0
bonus_production_timer = 0
total_clicks = 0
total_diamonds_earned = 0
achievement_unlocked = {}
upgrade_levels = {"click": 0, "production": 0, "fortune": 0}
upgrade_costs = {"click": 100, "production": 250, "fortune": 350}

building_list = {
    "dirt_farm": 0,
    "cobblestone_farm": 0,
    "oak_farm": 0,
    "coal_farm": 0,
    "iron_farm": 0,
    "diamondbat_farm": 0,
    "debris_farm": 0,
}

building_prod_bonus = {
    "dirt_farm": 0.0,
    "cobblestone_farm": 0.0,
    "oak_farm": 0.0,
    "coal_farm": 0.0,
    "iron_farm": 0.0,
    "diamondbat_farm": 0.0,
    "debris_farm": 0.0,
}

building_price_reduction = {
    "dirt_farm": 0.0,
    "cobblestone_farm": 0.0,
    "oak_farm": 0.0,
    "coal_farm": 0.0,
    "iron_farm": 0.0,
    "diamondbat_farm": 0.0,
    "debris_farm": 0.0,
}

permanent_slots = [None, None, None]
permanent_slot_levels = [0, 0, 0]
permanent_slot_costs = [700, 1200, 2400]

# Building instances
dirt_building_stats = Building("dirt_farm", 15, 1)
cobblestone_building_stats = Building("cobblestone_farm", 35, 3)
oak_building_stats = Building("oak_farm", 70, 6)
coal_building_stats = Building("coal_farm", 150, 10)
iron_building_stats = Building("iron_farm", 320, 16)
diamondbat_building_stats = Building("diamondbat_farm", 650, 28)
debris_building_stats = Building("debris_farm", 1200, 50)

game_is_running = True

building_stats = {
    "dirt_farm": dirt_building_stats,
    "cobblestone_farm": cobblestone_building_stats,
    "oak_farm": oak_building_stats,
    "coal_farm": coal_building_stats,
    "iron_farm": iron_building_stats,
    "diamondbat_farm": diamondbat_building_stats,
    "debris_farm": debris_building_stats,
}

achievement_data = {
    "first_diamond": {
        "title": "Premier diamant",
        "description": "Obtenez votre premier diamant.",
        "reward": "Débloque le mode rebirth.",
    },
    "clicker": {
        "title": "Clic rapide",
        "description": "Atteignez 25 clics.",
        "reward": "+1 de bonus de clic.",
    },
    "miner": {
        "title": "Mineur hors pair",
        "description": "Atteignez 100 diamants gagnés.",
        "reward": "+1 de fortune.",
    },
    "builder": {
        "title": "Constructeur",
        "description": "Achetez votre premier bâtiment.",
        "reward": "Accès aux améliorations avancées.",
    },
    "factory": {
        "title": "Usine de diamants",
        "description": "Atteignez 20 diamants/s de production.",
        "reward": "Production permanente +1.",
    },
    "rebirth": {
        "title": "Renaissance",
        "description": "Faites votre premier rebirth.",
        "reward": "Bonus de renaissance +1%.",
    },
}

slot_effects = [
    "global_click",
    "global_production",
    "global_price",
]


def can_afford(price):
    """Indique si le joueur a assez de diamants pour payer un achat."""
    return diamond >= price


def build_upgrade_cost(level, base_cost):
    """Calcule le coût d'une amélioration selon son niveau."""
    return int(base_cost * (1.35 ** level))


def get_upgrade_cost(name):
    """Retourne le coût actuel d'une amélioration globale."""
    return build_upgrade_cost(upgrade_levels[name], upgrade_costs[name])


def buy_upgrade(name):
    """Achète une amélioration globale et applique son effet."""
    cost = get_upgrade_cost(name)
    if not can_afford(cost):
        return False, f"Il vous faut {cost} diamants pour acheter cette amélioration."

    global diamond
    diamond -= cost
    upgrade_levels[name] += 1

    if name == "click":
        global click_multiplier
        click_multiplier += 1
        return True, "Votre clic est plus puissant !"

    if name == "production":
        global diamond_prod
        diamond_prod += 1
        return True, "La production passe à +1 diamants/s."

    if name == "fortune":
        global bonus_strength
        bonus_strength += 1
        return True, "Vos bonus aléatoires sont plus riches."

    return False, "Amélioration inconnue."


def get_building_upgrade_cost(building_name, upgrade_type):
    """Calcule le coût d'une amélioration spécifique à un bâtiment."""
    if upgrade_type == "production":
        return int(400 * (1.45 ** (building_prod_bonus[building_name] / 0.10)))
    if upgrade_type == "discount":
        return int(250 * (1.35 ** (building_price_reduction[building_name] / 0.05)))
    return 0


def buy_building_upgrade(building_name, upgrade_type):
    """Achete et applique une amélioration sur un bâtiment précis."""
    cost = get_building_upgrade_cost(building_name, upgrade_type)
    if not can_afford(cost):
        return False, f"Il vous faut {cost} diamants pour cette amélioration."

    global diamond
    diamond -= cost

    if upgrade_type == "production":
        building_prod_bonus[building_name] += 0.10
        return True, f"{building_name} gagne +10% de production."

    if upgrade_type == "discount":
        building_price_reduction[building_name] += 0.05
        return True, f"{building_name} est moins cher de 5%."

    return False, "Type d'amélioration inconnu."


def get_slot_cost(slot_index):
    """Retourne le coût du prochain niveau d'un slot permanent."""
    if slot_index >= len(permanent_slot_costs):
        return 999999

    current_level = permanent_slot_levels[slot_index]
    if current_level == 0:
        return permanent_slot_costs[slot_index]
    return build_upgrade_cost(current_level, permanent_slot_costs[slot_index])


def get_slot_label(slot_index):
    """Retourne le texte affiché pour un slot permanent."""
    if slot_index >= len(slot_effects):
        return "Slot vide"

    cost = get_slot_cost(slot_index)
    if permanent_slots[slot_index] is None:
        return f"Slot {slot_index + 1} - Débloquer ({cost} diamants)"

    level = permanent_slot_levels[slot_index]
    if slot_effects[slot_index] == "global_click":
        effect_text = f"Clic permanent +{level}"
    elif slot_effects[slot_index] == "global_production":
        effect_text = f"Production permanente +{level}"
    else:
        effect_text = f"Réduction globale prix {level * 5}%"

    return f"Slot {slot_index + 1} - {effect_text} (prix {cost})"


def apply_slot_delta(slot_index, delta):
    """Applique un delta d'effet sur un slot permanent."""
    global click_multiplier, diamond_prod

    effect = permanent_slots[slot_index]
    if effect == "global_click":
        click_multiplier += delta
    elif effect == "global_production":
        diamond_prod += delta
    elif effect == "global_price":
        for key in building_price_reduction:
            building_price_reduction[key] = min(0.5, building_price_reduction[key] + (delta * 0.05))


def apply_permanent_slots():
    """Applique tous les effets des slots permanents actifs."""
    global click_multiplier, diamond_prod

    click_multiplier = 1
    diamond_prod = 0

    for slot_index, effect in enumerate(permanent_slots):
        if effect is None:
            continue
        level = permanent_slot_levels[slot_index]
        apply_slot_delta(slot_index, level)


def buy_slot_upgrade(slot_index):
    """Débloque ou améliore un slot permanent."""
    if slot_index >= len(permanent_slots):
        return False, "Slot indisponible."

    current_level = permanent_slot_levels[slot_index]
    cost = get_slot_cost(slot_index)
    if not can_afford(cost):
        if current_level == 0:
            return False, f"Il vous faut {cost} diamants pour débloquer ce slot."
        return False, f"Il vous faut {cost} diamants pour améliorer ce slot."

    global diamond
    diamond -= cost

    if current_level == 0:
        permanent_slots[slot_index] = slot_effects[slot_index]
        permanent_slot_levels[slot_index] = 1
        apply_slot_delta(slot_index, 1)
        return True, f"Slot {slot_index + 1} activé."

    permanent_slot_levels[slot_index] += 1
    apply_slot_delta(slot_index, 1)
    return True, f"Slot {slot_index + 1} amélioré au niveau {permanent_slot_levels[slot_index]} !"


def reset_buildings():
    """Réinitialise les bâtiments à leur état de base."""
    global diamond_prod

    for building in building_stats.values():
        building.reset()

    for key in building_list:
        building_list[key] = 0

    diamond_prod = 0


def reset_game_state():
    """Réinitialise complètement l'état du jeu à son état initial."""
    global diamond, click_multiplier, diamond_prod, rebirth_count, rebirth_points
    global rebirth_bonus_pct, rebirth_cash_bonus, bonus_strength, bonus_click
    global bonus_production, bonus_click_timer, bonus_production_timer
    global total_clicks, total_diamonds_earned, achievement_unlocked, upgrade_levels, game_is_running

    diamond = 0
    click_multiplier = 1
    diamond_prod = 0
    rebirth_count = 0
    rebirth_points = 0
    rebirth_bonus_pct = 0.0
    rebirth_cash_bonus = 1.0
    bonus_strength = 1
    bonus_click = 0
    bonus_production = 0
    bonus_click_timer = 0
    bonus_production_timer = 0
    total_clicks = 0
    total_diamonds_earned = 0
    achievement_unlocked = {}
    upgrade_levels = {"click": 0, "production": 0, "fortune": 0}

    for key in building_prod_bonus:
        building_prod_bonus[key] = 0.0

    for key in building_price_reduction:
        building_price_reduction[key] = 0.0

    for key in building_list:
        building_list[key] = 0

    permanent_slots[:] = [None, None, None]
    permanent_slot_levels[:] = [0, 0, 0]

    for building in building_stats.values():
        building.reset()

    game_is_running = False
    apply_permanent_slots()


def reset_save():
    """Supprime la sauvegarde et réinitialise l'état du jeu."""
    if SAVE_PATH.exists():
        SAVE_PATH.unlink()

    reset_game_state()
    return True


def tick_buffs():
    """Décrémente les timers des bonus temporaires actifs."""
    global bonus_click_timer, bonus_production_timer, bonus_click, bonus_production

    if bonus_click_timer > 0:
        bonus_click_timer -= 1
        if bonus_click_timer == 0:
            bonus_click = 0

    if bonus_production_timer > 0:
        bonus_production_timer -= 1
        if bonus_production_timer == 0:
            bonus_production = 0


def effective_click_multiplier():
    """Calcule le multiplicateur de clic effectif."""
    return int(round((click_multiplier * (1 + rebirth_bonus_pct)) + bonus_click))


def building_effective_production(name):
    """Calcule la production effective d'un bâtiment."""
    building = building_stats[name]
    bonus = building_prod_bonus[name]
    return building.get_amount() * building.get_production() * (1 + bonus)


def effective_production():
    """Calcule la production totale effective du joueur."""
    total = diamond_prod
    for name in building_stats:
        total += building_effective_production(name)

    total += bonus_production
    return int(round(total * (1 + rebirth_bonus_pct)))


def get_save_data():
    """Construit l'état complet sauvegardable du jeu."""
    return {
        "diamond": diamond,
        "click_multiplier": click_multiplier,
        "diamond_prod": diamond_prod,
        "rebirth_count": rebirth_count,
        "rebirth_points": rebirth_points,
        "rebirth_bonus_pct": rebirth_bonus_pct,
        "rebirth_cash_bonus": rebirth_cash_bonus,
        "bonus_strength": bonus_strength,
        "bonus_click": bonus_click,
        "bonus_production": bonus_production,
        "bonus_click_timer": bonus_click_timer,
        "bonus_production_timer": bonus_production_timer,
        "total_clicks": total_clicks,
        "total_diamonds_earned": total_diamonds_earned,
        "achievement_unlocked": achievement_unlocked,
        "upgrade_levels": upgrade_levels,
        "building_list": building_list.copy(),
        "building_prod_bonus": building_prod_bonus.copy(),
        "building_price_reduction": building_price_reduction.copy(),
        "permanent_slots": permanent_slots.copy(),
        "permanent_slot_levels": permanent_slot_levels.copy(),
        "building_prices": {name: building_stats[name].price for name in building_stats},
        "building_amounts": {name: building_stats[name].amount for name in building_stats},
    }


def save_game():
    """Sauvegarde l'état actuel du jeu dans le fichier texte."""
    try:
        SAVE_PATH.write_text(json.dumps(get_save_data(), indent=2, sort_keys=True), encoding="utf-8")
        return True
    except Exception:
        return False


def load_game():
    """Recharge une partie sauvegardée si le fichier existe."""
    if not SAVE_PATH.exists():
        return False

    try:
        data = json.loads(SAVE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return False

    global diamond, click_multiplier, diamond_prod, rebirth_count, rebirth_points
    global rebirth_bonus_pct, rebirth_cash_bonus, bonus_strength, bonus_click
    global bonus_production, bonus_click_timer, bonus_production_timer
    global total_clicks, total_diamonds_earned, achievement_unlocked, upgrade_levels

    diamond = int(data.get("diamond", 0))
    click_multiplier = int(data.get("click_multiplier", 1))
    diamond_prod = int(data.get("diamond_prod", 0))
    rebirth_count = int(data.get("rebirth_count", 0))
    rebirth_points = int(data.get("rebirth_points", 0))
    rebirth_bonus_pct = float(data.get("rebirth_bonus_pct", 0.0))
    rebirth_cash_bonus = float(data.get("rebirth_cash_bonus", 1.0))
    bonus_strength = int(data.get("bonus_strength", 1))
    bonus_click = int(data.get("bonus_click", 0))
    bonus_production = int(data.get("bonus_production", 0))
    bonus_click_timer = int(data.get("bonus_click_timer", 0))
    bonus_production_timer = int(data.get("bonus_production_timer", 0))
    total_clicks = int(data.get("total_clicks", 0))
    total_diamonds_earned = int(data.get("total_diamonds_earned", 0))
    achievement_unlocked = data.get("achievement_unlocked", {}) or {}
    upgrade_levels = data.get("upgrade_levels", upgrade_levels) or upgrade_levels

    building_list.update(data.get("building_list", {}) or {})
    building_prod_bonus.update(data.get("building_prod_bonus", {}) or {})
    building_price_reduction.update(data.get("building_price_reduction", {}) or {})

    saved_slots = data.get("permanent_slots", []) or []
    for index, slot in enumerate(saved_slots):
        if index < len(permanent_slots):
            permanent_slots[index] = slot

    saved_levels = data.get("permanent_slot_levels", []) or []
    for index, level in enumerate(saved_levels):
        if index < len(permanent_slot_levels):
            permanent_slot_levels[index] = int(level)

    for index, slot in enumerate(permanent_slots):
        if slot is not None and permanent_slot_levels[index] == 0:
            permanent_slot_levels[index] = 1

    for name in building_stats:
        stats = building_stats[name]
        stats.amount = int((data.get("building_amounts", {}) or {}).get(name, 0))
        stats.price = int((data.get("building_prices", {}) or {}).get(name, stats.base_price))

    return True


def rebirth_threshold():
    """Calcule le seuil requis pour effectuer un rebirth."""
    return int(1000 * (1.75 ** rebirth_count))


def check_achievements():
    """Vérifie et débloque les succès selon l'état du jeu."""
    unlocked = []

    if total_diamonds_earned >= 1 and not achievement_unlocked.get("first_diamond"):
        achievement_unlocked["first_diamond"] = True
        unlocked.append("first_diamond")

    if total_clicks >= 25 and not achievement_unlocked.get("clicker"):
        achievement_unlocked["clicker"] = True
        unlocked.append("clicker")

    if total_diamonds_earned >= 100 and not achievement_unlocked.get("miner"):
        achievement_unlocked["miner"] = True
        unlocked.append("miner")

    if any(building.get_amount() > 0 for building in building_stats.values()) and not achievement_unlocked.get("builder"):
        achievement_unlocked["builder"] = True
        unlocked.append("builder")

    if effective_production() >= 20 and not achievement_unlocked.get("factory"):
        achievement_unlocked["factory"] = True
        unlocked.append("factory")

    if rebirth_count >= 1 and not achievement_unlocked.get("rebirth"):
        achievement_unlocked["rebirth"] = True
        unlocked.append("rebirth")

    return unlocked


def get_achievement_lines():
    """Retourne les lignes d'affichage des succès pour l'UI."""
    lines = []
    for key, data in achievement_data.items():
        status = "✓" if achievement_unlocked.get(key) else "○"
        lines.append(f"{status} {data['title']} - {data['description']}")
    return lines


def buy_building(name, quantity=1):
    """Achète un ou plusieurs bâtiments et met à jour l'état du joueur."""
    global diamond

    if isinstance(name, Building):
        name = name.name

    if quantity < 1:
        return False, "Quantité invalide."

    building = building_stats[name]
    total_cost = 0

    for _ in range(quantity):
        total_cost += building.get_price(building_price_reduction[name])

    if diamond < total_cost:
        return False, f"Vous n'avez pas assez de diamants. Il vous manque {total_cost - diamond}."

    diamond -= total_cost

    for _ in range(quantity):
        building.buy()

    building_list[name] += quantity
    check_achievements()
    return True, f"{building.get_name()} acheté{'s' if quantity > 1 else ''} !"


def rebirth_progress():
    """Réinitialise les bâtiments et augmente les bonus de renaissance."""
    global diamond, diamond_prod, click_multiplier, rebirth_count, rebirth_points, rebirth_bonus_pct, rebirth_cash_bonus, bonus_click, bonus_production, bonus_click_timer, bonus_production_timer, bonus_strength

    diamond = 0
    diamond_prod = 0
    click_multiplier = 1
    bonus_click = 0
    bonus_production = 0
    bonus_click_timer = 0
    bonus_production_timer = 0
    bonus_strength = 1

    for key in building_prod_bonus:
        building_prod_bonus[key] = 0.0

    for key in building_price_reduction:
        building_price_reduction[key] = 0.0

    global upgrade_levels
    upgrade_levels = {"click": 0, "production": 0, "fortune": 0}

    reset_buildings()
    rebirth_count += 1
    rebirth_points += 1
    rebirth_bonus_pct = rebirth_points * 0.01
    rebirth_cash_bonus = 1 + (rebirth_points * 0.1)
    apply_permanent_slots()
    check_achievements()



