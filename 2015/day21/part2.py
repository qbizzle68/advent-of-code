import sys
import re
import itertools
from dataclasses import dataclass


@dataclass
class EquipableItem:
    name: str
    cost: int
    damage: int
    armor: int


class PlayerLoadout:
    def __init__(self, items: list[EquipableItem]) -> None:
        self.items = items
        self.damage = sum(item.damage for item in items)
        self.armor = sum(item.armor for item in items)

    def __str__(self) -> str:
        return str(self.items)


def import_items(path: str) -> dict[str, list[EquipableItem]]:
    with open(path) as f:
        data = f.readlines()

    items = {'weapons': [], 'armor': [], 'rings': []}
    regex = re.compile(r'^(\S+(?: \+\d)?)\s+(\d+)\s+(\d+)\s+(\d+).*$')
    category = None
    for line in data:
        if line.startswith('Weapons: '):
            category = 'weapons'
            continue
        elif line.startswith('Armor: '):
            category = 'armor'
            continue
        elif line.startswith('Rings: '):
            category = 'rings'
            continue

        match = regex.match(line)
        if match is None:
            continue

        item = EquipableItem(match.group(1), *(int(match.group(i)) for i in range(2, 5)))
        items[category].append(item)

    return items


def import_initial_state(path: str) -> dict[str, int]:
    with open(path) as f:
        data = f.readlines()
    
    initial_state = {}
    for line in data:
        split = line.split(': ')
        initial_state[split[0].lower()] = int(split[1])

    return initial_state


def create_purchase_combinations(items: dict[str, list[EquipableItem]]) -> list[list[EquipableItem]]:
    valid_loadouts = []
    # Can only take 1 weapon at a time
    for weapon in items['weapons']:
        # Can have either 0 or 1 armor
        for i in range(2):
            armor_combos = itertools.combinations(items['armor'], i)
            for armor in armor_combos:
                for j in range(3):
                    ring_combos = itertools.combinations(items['rings'], j)
                    for combo in ring_combos:
                        loadout = PlayerLoadout((weapon,) + armor + combo)
                        valid_loadouts.append(loadout)

    return valid_loadouts


def play_battle(loadout: PlayerLoadout, initial_state: dict[str, int]) -> bool:
    """Returns True if the player wins the battle, False otherwise."""

    opponent_hp = initial_state['hit points']
    opponent_damage = initial_state['damage']
    opponent_armor = initial_state['armor']
    player_hp = 100
    player_damage = loadout.damage
    player_armor = loadout.armor
    players_turn = True

    player_net_damage = max((1, player_damage - opponent_armor))
    opponent_net_damage = max((1, opponent_damage - player_armor))

    while opponent_hp > 0 and player_hp > 0:
        if players_turn:
            opponent_hp -= player_net_damage
        else:
            player_hp -= opponent_net_damage
        players_turn = not players_turn

    return True if player_hp > 0 else False


def main(items: dict[str, list[EquipableItem]], initial_state: dict[str, int]) -> int:
    loadouts = create_purchase_combinations(items)
    winning_loadouts = [loadout for loadout in loadouts if play_battle(loadout, initial_state) is False]

    return max((sum(item.cost for item in loadout.items) for loadout in winning_loadouts))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} SHOP_FILE INPUT_FILE')
    shop_data_path = sys.argv[1]
    input_data_path = sys.argv[2]

    items = import_items(shop_data_path)
    initial_state = import_initial_state(input_data_path)
    
    value = main(items, initial_state)
    print(f'Value is {value}')
