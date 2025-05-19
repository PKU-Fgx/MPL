import json
from tqdm import tqdm

label_set = list(json.load(open("label_exp.json", "r"))[0].keys())

name = "train"

output_list = list()
with open(f"./{name}.json", "r", encoding="utf-8") as f:
    for line in tqdm(f.readlines()):
        line = json.loads(line)

        out_mention_list = list()
        for mention in line["entity_mentions"]:
            entity = mention["text"]
            type_name = mention["entity_type"]
            out_mention_list.append([entity, type_name])

        output_list.append({
            "sentence": line["sentence"],
            "mentions": out_mention_list,
        })

with open(f'./Formatted/{name}.json', 'w', encoding='utf-8') as f:
    json.dump(output_list, f, ensure_ascii=False, indent=4)

print(len(output_list))