# TODO:
# Add initial gold/gem cost, plus unlock cost, when optimizing
# Suggest only affordable checkbox
# Current gold input/label
# Current gems input/label
# disclaimer that magic damage is currently only calculated for single target and is thus a little better than described
# clicks/s label/input (defaults to 5)
# enable click damage for suggestions checkbox
# reset button for when the game restarts
# save upon closing the program and load upon starting
# Figure out how to handle non-updated costs. No idea how to handle it tbh. Might just let the user handle it
# Figure out how to handle optimization with gem costs. Perhaps we should have an input where the user defines the weight of it compared to gold cost
# Move things into widgets and move things out of the main.py file.

import tkinter
from tkinter import ttk
from idlelib.tooltip import Hovertip
import json
from dataclasses import dataclass
import copy

root = tkinter.Tk()


@dataclass
class PrestigeCard:
    name: str
    description: str


@dataclass
class PrestigeCardCount:
    magical_familiar: int = 0
    ronin: int = 0
    sharpening: int = 0
    collection: int = 0
    anvil: int = 0
    dojo: int = 0
    magic_book: int = 0


@dataclass
class Card:
    name: str
    description: str
    initial_gold_cost: int
    initial_gem_cost: int
    unlock_gem_cost: int


@dataclass
class CardCount:
    klink_kick: int = 0
    draw_the_sword: int = 0
    sharpen_the_blade: int = 0
    spellcasting: int = 0
    swing_the_sword: int = 0
    magic_wand: int = 0
    goldmine: int = 0
    magic_blade: int = 0
    the_forge: int = 0
    summon_a_wizard: int = 0
    bronze_akinak: int = 0
    arcenal: int = 0


class CardWidget(ttk.Frame):
    def __init__(self, parent: ttk.Frame, card: Card):
        super().__init__(master=parent)

        self.rowconfigure((0, 1, 2, 3), weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.card_label = ttk.Label(self, text=card.name)
        self.card_count_spinbox = ttk.Spinbox(self, from_=0, to=100, width=10)
        gold_cost_label = ttk.Label(self, text="Gold")
        self.gold_cost_value = tkinter.StringVar(
            value=str(card.initial_gold_cost))
        gold_cost_entry = ttk.Entry(
            self, width=10, textvariable=self.gold_cost_value)
        gem_cost_label = ttk.Label(self, text="Gems")
        self.gem_cost_value = tkinter.StringVar(
            value=str(card.initial_gem_cost))
        gem_cost_entry = ttk.Entry(
            self, width=10, textvariable=self.gem_cost_value)
        unlock_gem_cost_label = ttk.Label(self, text="Unlock")
        unlock_gem_cost_value_label = ttk.Label(
            self, text=card.unlock_gem_cost)

        Hovertip(self.card_label, card.description, hover_delay=100)

        self.card_label.grid(column=0, row=0, columnspan=2, padx="0 5")
        self.card_count_spinbox.grid(
            column=0, row=1, columnspan=2, sticky="we", padx="0 5")
        gold_cost_label.grid(column=0, row=2, sticky="w")
        gold_cost_entry.grid(column=1, row=2, sticky="e", padx="0 5")
        gem_cost_label.grid(column=0, row=3, sticky="w")
        gem_cost_entry.grid(column=1, row=3, sticky="e", padx="0 5")
        unlock_gem_cost_label.grid(column=0, row=4, sticky="w")
        unlock_gem_cost_value_label.grid(
            column=1, row=4, sticky="e", padx="0 5")

        self.card_count_spinbox.set(0)


class PrestigeCardWidget(ttk.Frame):
    def __init__(self, parent: ttk.Frame, card: PrestigeCard):
        super().__init__(master=parent)

        self.rowconfigure((0, 1, 2, 3), weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.card_label = ttk.Label(self, text=card.name)
        self.card_count_spinbox = ttk.Spinbox(self, from_=0, to=100, width=10)

        # In case we need it, \n for newline to make it a multiline tooltip
        Hovertip(self.card_label, card.description, hover_delay=100)

        self.card_label.grid(column=0, row=0, columnspan=2, padx="0 5")
        self.card_count_spinbox.grid(
            column=0, row=1, columnspan=2, sticky="we", padx="0 5")

        self.card_count_spinbox.set(0)


def load_cards() -> list[Card]:
    with (open("cards.json")) as read_file:
        json_data = json.load(read_file)
    # Keep in mind that the order of the cards in the file is important and match the order in the game.
    # It goes from upper left to upper right and then repeats for each row
    json_cards = json_data["cards"]
    cards: list[Card] = list[Card]()
    for json_card in json_cards:
        cards.append(Card(**json_card))

    return cards


def load_prestige_cards() -> list[PrestigeCard]:
    with (open("cards.json")) as read_file:
        json_data = json.load(read_file)
    # Keep in mind that the order of the cards in the file is important and match the order in the game.
    # It goes from upper left to upper right and then repeats for each row
    json_cards = json_data["prestige_cards"]
    cards: list[PrestigeCard] = list[PrestigeCard]()
    for json_card in json_cards:
        cards.append(PrestigeCard(**json_card))

    return cards


def setup_cards(frame: ttk.Frame) -> list[CardWidget]:
    cards = load_cards()
    card_widgets = []
    card_columns = len(cards) % 13

    ttk.Label(frame, text="Cards").grid(
        column=0, row=0, columnspan=card_columns)

    # Card Widgets fill column/row from (0, 1) to (11, 3)
    for index, card in enumerate(cards):
        card_widget = CardWidget(frame, card)
        card_column = index % 12
        card_row = 1
        if 12 <= index < 24:
            card_row = 2
        elif index >= 24:
            card_row = 3

        card_widget.grid(column=card_column, row=card_row)

        if card.name == "KLINK KICK":
            # The very first card is free so we set the count to 1
            card_widget.card_count_spinbox.set(1)
        elif card.name == "GOLDMINE":
            # For this card there is a limit of 5 cards
            card_widget.card_count_spinbox.configure(to=5)

        card_widgets.append(card_widget)

    return card_widgets


def setup_prestige_cards(frame: ttk.Frame) -> list[PrestigeCardWidget]:
    cards = load_prestige_cards()
    card_widgets = []
    card_columns = len(cards)

    ttk.Label(frame, text="Prestige Cards").grid(
        column=0, row=0, columnspan=card_columns)

    for index, card in enumerate(cards):
        card_widget = PrestigeCardWidget(frame, card)
        card_widget.grid(column=index, row=1)
        card_widgets.append(card_widget)

    return card_widgets


def setup_tk(root: tkinter.Tk):
    root.title("Card Storm Idle Optimizer")
    root.geometry("1600x900")
    root.columnconfigure(0, weight=1)
    root.rowconfigure((1, 2, 3), weight=1)


# TODO: Add automatic testing of this.
def calculate_total_dps(card_count: CardCount, prestige_card_count: PrestigeCardCount, include_click_damage: bool = False, clicks_per_second: int = 5) -> int:
    click_damage_value = calculate_click_damage(
        card_count, prestige_card_count) * clicks_per_second
    dps_value = calculate_dps(card_count, prestige_card_count)
    magic_damage_value = calculate_magic_damage(
        card_count, prestige_card_count)
    total_dps_value = dps_value + magic_damage_value + \
        click_damage_value if include_click_damage else dps_value + magic_damage_value

    return total_dps_value


def calculate_click_damage(card_count: CardCount, prestige_card_count: PrestigeCardCount) -> int:
    total_damage = (prestige_card_count.sharpening * 2 + (card_count.klink_kick + card_count.klink_kick * card_count.arcenal * 10) *
                    (1 + card_count.sharpen_the_blade * 2) + card_count.bronze_akinak * 5000) * (1 + card_count.magic_blade) * (1 + prestige_card_count.dojo)

    return total_damage


def calculate_dps(card_count: CardCount, prestige_card_count: PrestigeCardCount) -> int:
    total_damage = (prestige_card_count.ronin * 50 + ((card_count.draw_the_sword * 5 + card_count.draw_the_sword * card_count.arcenal * 10)
                    * (1 + card_count.the_forge * 10)) + card_count.swing_the_sword * 500) * (1 + prestige_card_count.anvil)

    return total_damage


def calculate_magic_damage(card_count: CardCount, prestige_card_count: PrestigeCardCount) -> int:
    total_damage = (prestige_card_count.magical_familiar * 3 + ((card_count.spellcasting * 10 + card_count.spellcasting * card_count.arcenal * 10)
                    * (1 + card_count.summon_a_wizard)) + card_count.magic_wand * 100) * (1 + card_count.magic_blade) * (1 + prestige_card_count.magic_book)

    return total_damage


def get_card_count(cards: list[CardWidget]) -> CardCount:
    result = CardCount()
    for card in cards:
        name = card.card_label.cget("text")
        # TODO: Figure out a way to do this better
        match name:
            case "KLINK KICK":
                result.klink_kick = int(card.card_count_spinbox.get())
            case "DRAW THE SWORD":
                result.draw_the_sword = int(card.card_count_spinbox.get())
            case "SHARPEN THE BLADE":
                result.sharpen_the_blade = int(card.card_count_spinbox.get())
            case "SPELLCASTING":
                result.spellcasting = int(card.card_count_spinbox.get())
            case "SWING THE SWORD":
                result.swing_the_sword = int(card.card_count_spinbox.get())
            case "MAGIC WAND":
                result.magic_wand = int(card.card_count_spinbox.get())
            case "GOLDMINE":
                result.goldmine = int(card.card_count_spinbox.get())
            case "MAGIC BLADE":
                result.magic_blade = int(card.card_count_spinbox.get())
            case "THE FORGE":
                result.the_forge = int(card.card_count_spinbox.get())
            case "SUMMON A WIZARD":
                result.summon_a_wizard = int(card.card_count_spinbox.get())
            case "BRONZE AKINAK":
                result.bronze_akinak = int(card.card_count_spinbox.get())
            case "ARCENAL":
                result.arcenal = int(card.card_count_spinbox.get())
    return result


def get_prestige_card_count(cards: list[PrestigeCardWidget]) -> PrestigeCardCount:
    result = PrestigeCardCount()
    for card in cards:
        name = card.card_label.cget("text")
        match name:
            case "MAGICAL FAMILIAR":
                result.magical_familiar = int(card.card_count_spinbox.get())
            case "RONIN":
                result.ronin = int(card.card_count_spinbox.get())
            case "SHARPENING":
                result.sharpening = int(card.card_count_spinbox.get())
            case "COLLECTION":
                result.collection = int(card.card_count_spinbox.get())
            case "ANVIL":
                result.anvil = int(card.card_count_spinbox.get())
            case "DOJO":
                result.dojo = int(card.card_count_spinbox.get())
            case "MAGIC BOOK":
                result.magic_book = int(card.card_count_spinbox.get())

    return result


# TODO: Add automatic testing of this
def optimize(current_card_count: CardCount, prestige_card_count: PrestigeCardCount) -> str:
    # TODO: Calculate a comparison value depending on cost and dps increase. Currently we only calculate based on dps increase
    highest_dps_field = ""
    higest_dps_value = 0

    for field in current_card_count.__dataclass_fields__:
        new_card_count = copy.copy(current_card_count)
        new_card_count.__dict__[field] += 1
        new_dps = calculate_total_dps(new_card_count, prestige_card_count)
        if higest_dps_value < new_dps:
            higest_dps_value = new_dps
            highest_dps_field = field

    # Transform field into a human readable format. I am unsure if this is a hack or not.
    return highest_dps_field.upper().replace("_", " ")


# Note that this uses global variables since we cannot return values. TODO: Move into classes so we can use "self." and getters instead
def calculate():
    card_count = get_card_count(cards)
    prestige_card_count = get_prestige_card_count(prestige_cards)

    click_damage_value = calculate_click_damage(
        card_count, prestige_card_count)
    dps_value = calculate_dps(card_count, prestige_card_count)
    magic_damage_value = calculate_magic_damage(
        card_count, prestige_card_count)
    total_dps_value = dps_value + magic_damage_value

    click_damage.set(str(click_damage_value))
    dps.set(str(dps_value))
    magic_damage.set(str(magic_damage_value))
    total_dps.set(str(total_dps_value))

    next_card_value = optimize(card_count, prestige_card_count)
    next_card.set(next_card_value)


setup_tk(root)

# Because there's so many card widgets they get their own frame so they don't mess with the column width of the other widgets
cardframe = ttk.Frame(root, padding="3 3 12 12")
cardframe.grid(column=0, row=0, sticky="nwe")

cards = setup_cards(cardframe)

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=1, sticky="nswe")

# This button calculates current damage and suggests the next card to upgrade
# TODO: Do calculations automatically upon changing any input
calculate_current_damage = ttk.Button(
    mainframe, text="Calculate", command=calculate)
calculate_current_damage.grid(column=0, row=0, columnspan=2)

# TODO: There are a lot of widgets here. They should be moved into a custom widget rather than be global.
click_damage_text_label = ttk.Label(mainframe, text="Click Damage:")
click_damage = tkinter.StringVar(value="1")
click_damage_value_label = ttk.Label(mainframe, textvariable=click_damage)

click_damage_text_label.grid(column=0, row=1, sticky="e")
click_damage_value_label.grid(column=1, row=1, sticky="w")

dps_text_label = ttk.Label(mainframe, text="DPS:")
dps = tkinter.StringVar(value="0")
dps_value_label = ttk.Label(mainframe, textvariable=dps)

dps_text_label.grid(column=0, row=2, sticky="e")
dps_value_label.grid(column=1, row=2, sticky="w")

magic_damage_text_label = ttk.Label(mainframe, text="Magic Damage:")
magic_damage = tkinter.StringVar(value="0")
magic_damage_value_label = ttk.Label(mainframe, textvariable=magic_damage)

magic_damage_text_label.grid(column=0, row=3, sticky="e")
magic_damage_value_label.grid(column=1, row=3, sticky="w")

total_dps_text_label = ttk.Label(mainframe, text="Total DPS:")
total_dps = tkinter.StringVar(value="0")
total_dps_value_label = ttk.Label(mainframe, textvariable=total_dps)

total_dps_text_label.grid(column=0, row=4, sticky="e")
total_dps_value_label.grid(column=1, row=4, sticky="w")

next_card_text_label = ttk.Label(mainframe, text="Next Card:")
next_card = tkinter.StringVar(value="N/A")
next_card_value_label = ttk.Label(mainframe, textvariable=next_card)

next_card_text_label.grid(column=0, row=5, sticky="e")
next_card_value_label.grid(column=1, row=5, sticky="w")

# Because there's so many card widgets they get their own frame so they don't mess with the column width of the other widgets
prestige_card_frame = ttk.Frame(root, padding="3 3 12 12")
prestige_card_frame.grid(column=0, row=2, sticky="nwe")

prestige_cards = setup_prestige_cards(prestige_card_frame)

root.mainloop()
