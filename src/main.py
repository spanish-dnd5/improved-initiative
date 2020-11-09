import json
import os

from creature_formatter import format_monster

if __name__ == "__main__":

    dirpath = os.path.dirname(os.path.realpath(__file__))
    output_folder = f'{dirpath}/../output'
    crawler_repo = '../../spanish-srd5.1-crawl/output/monsters.json'
    with open(f'{dirpath}/{crawler_repo}', 'r') as file:
        monsters = json.load(file)

    result = {}
    for monster in monsters:
        result.update(format_monster(monster))

    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    with open(f'{output_folder}/spanish_srd_creatures.json',
              'w',
              encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
