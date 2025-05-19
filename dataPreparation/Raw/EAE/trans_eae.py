import json
from tqdm import tqdm

label_set = json.load(open("label_exp.json", "r"))[0]

for name in ['train', 'dev', 'test']:

    output_list = list()
    with open(f"./{name}.json", "r") as f:
        for line in tqdm(list(map(json.loads, f.readlines()))):
            sentence = " ".join(line["tokens"])
            for eve in line["event_mentions"]:
                output_list.append({
                    "sentence": sentence,
                    "trigger_word": eve["trigger"]["text"],
                    "event_type": eve["event_type"],
                    "labels": label_set[eve["event_type"]]["Role Types"],
                    "arguments": eve['arguments']
                })

    print(len(output_list))

    with open(f'./Formatted/{name}.json', 'w', encoding='utf-8') as f:
        json.dump(output_list, f, ensure_ascii=False, indent=4)