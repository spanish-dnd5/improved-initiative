import re
import time
from typing import Dict


def construct_actions(array, subtype):
    result = []
    for element in array:
        name = element['name'].replace('espacio', 'slot')
        name = name.replace('día', 'Day')
        name = name.replace('Lanzamiento de conjuros innato',
                            'Innate Spellcasting')
        name = name.replace('Lanzamiento de conjuros', 'Spellcasting')
        description = element['description']
        if subtype in element:
            description += '\n'
            for subelement in element[subtype]:
                subname = subelement['name'].replace('espacio', 'slot')
                subname = subname.replace('Nivel 1', '1st level')
                subname = subname.replace('Nivel 2', '2nd level')
                subname = subname.replace('Nivel 3', '3rd level')
                subname = re.sub(r'Nivel (\d)', r'\1th level', subname)
                description += f"\n• **{subname}**: {subelement['description']}"
        result.append({'Name': name, 'Content': description, 'Usage': ''})
    return result


def format_monster(m: Dict):
    armor_class_notes_array = []
    armor_class_notes = ""

    if 'type' in m['armor_class'][0] and m['armor_class'][0]['type']:
        armor_class_notes_array.append(m['armor_class'][0]['type'])
    if len(m['armor_class']) > 1:
        for ac in m['armor_class'][1:]:
            ac_string = f"{ac['amount']} {ac['condition']}"
            if 'type' in ac and ac['type']:
                ac_string += f" ({ac['type']})"
            armor_class_notes_array.append(ac_string)
        armor_class_notes = f"({', '.join(armor_class_notes_array)})"

    tags = f" ({', '.join(m['tags'])})" if m['tags'] else ""
    _, link = m['source'].split(':', 1)
    return {
        f"Creatures.{m['index']}": {
            "Id":
            m['index'],
            "Name":
            m['name'],
            "Path":
            "Spanish SDR",
            "Source":
            "http://srd.nosolorol.com/DD5/",
            "Type":
            f"{m['type']} {m['size']}{tags}, {m['alignment']}",
            "HP": {
                "Value": m['hit_points'],
                "Notes": f"({m['hit_dice']})"
            },
            "AC": {
                "Value": m['armor_class'][0]['amount'],
                "Notes": armor_class_notes
            },
            "InitiativeModifier":
            m['initiative'],
            "InitiativeAdvantage":
            False,
            "Speed":
            [f"{type_} {amount} pies" for type_, amount in m['speed'].items()],
            "Abilities": {
                "Str": m['abilities']['strength'],
                "Dex": m['abilities']['dexterity'],
                "Con": m['abilities']['constitution'],
                "Int": m['abilities']['intelligence'],
                "Wis": m['abilities']['wisdom'],
                "Cha": m['abilities']['charisma']
            },
            "DamageVulnerabilities":
            m['damage_vulnerabilities'],
            "DamageResistances":
            m['damage_resistances'],
            "DamageImmunities":
            m['damage_immunities'],
            "ConditionImmunities":
            m['condition_immunities'],
            "Saves": [{
                "Name": save,
                "Modifier": value
            } for save, value in m['saving_throws'].items()],
            "Skills": [{
                "Name": skill,
                "Modifier": value
            } for skill, value in m['skills'].items()],
            "Senses":
            m['senses'],
            "Languages":
            m['languages'],
            "Challenge":
            m['challenge_rating'],
            "Traits":
            construct_actions(m['special_abilities'], 'spells'),
            "Actions":
            construct_actions(m['actions'], 'extra'),
            "Reactions":
            construct_actions(m['reactions'], 'extra'),
            "LegendaryActions":
            construct_actions(getattr(m['legendary_actions'], 'list', []),
                              'extra'),
            "Description":
            f"{m['description']}\n\n{link}",
            "Player":
            "",
            "Version":
            "2.16.0",
            "ImageURL":
            "",
            "LastUpdateMs":
            int(round(time.time() * 1000))
        }
    }
