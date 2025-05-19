import json
from tqdm import tqdm

label_map = json.load(open("ACE05_label_exp.json", "r"))[0]

for name in ['dev']:

    output_list = list()
    with open(f"./{name}.json", "r") as f:
        for line in tqdm(list(map(json.loads, f.readlines()))):
            sentence = " ".join(line["tokens"])

            relation_mentions = list()
            for rel in line["relation_mentions"]:
                relation_mentions.append({
                    "head_entity": rel["arguments"][0]["text"],
                    "tail_entity": rel["arguments"][1]["text"],
                    "realtion_type": rel["relation_type"]
                })

            output_list.append({
                "entities": [e['text'] for e in line["entity_mentions"]],
                "sentence": sentence,
                "relation_mentions": [{**m, 'realtion_type': label_map[m['realtion_type']]} for m in relation_mentions]
            })

    print(len(output_list))

    with open(f'./Formatted/{name}.json', 'w', encoding='utf-8') as f:
        json.dump(output_list, f, ensure_ascii=False, indent=4)