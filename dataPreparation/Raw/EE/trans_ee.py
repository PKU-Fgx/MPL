import json
from tqdm import tqdm

label_set = list(json.load(open("label_exp.json", "r"))[0].keys())

for name in ['train', 'dev', 'test']:

    n = 10
    output_list = list()
    with open(f"./{name}.json", "r") as f:
        for line in tqdm(list(map(json.loads, f.readlines()))):
            sentence = " ".join(line["tokens"])

            label_candi = list()
            event_mentions = list()
            for eve in line["event_mentions"]:
                label_candi.append(eve["event_type"])
                event_mentions.append({
                    "event_type": eve["event_type"],
                    "trigger": eve["trigger"]["text"],
                    "arguments": eve['arguments']
                })

            wrong_list = [i for i in label_set if i not in label_candi]

            output_list.append({
                "sentence": sentence,
                "arg_candi": [i["text"] for i in line["entity_mentions"]],
                "wrong_list": wrong_list,
                "event_mentions": event_mentions
            })

    print(len(output_list))

    with open(f'./Formatted/{name}.json', 'w', encoding='utf-8') as f:
        json.dump(output_list, f, ensure_ascii=False, indent=4)