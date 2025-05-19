import json

for task in ['ACE05', 'RAMS']:
    train_path = f"./{task}/train.json"
    valid_path = f"./{task}/dev.json"
    infer_path = f"./{task}/test.json"
    
    old_label_set = json.load(open(f"./{task}/label_exp.json", 'r'))[0].keys()
    new_label_set = json.load(open(f"./{task}/label_exp_new.json", 'r'))[0].keys()

    old2new = {k: v for k, v in zip(old_label_set, new_label_set)}
    
    train_new_data = [{**line, 'event_type': old2new[line['event_type']]} for line in json.load(open(train_path, 'r'))]
    valid_new_data = [{**line, 'event_type': old2new[line['event_type']]} for line in json.load(open(valid_path, 'r'))]
    infer_new_data = [{**line, 'event_type': old2new[line['event_type']]} for line in json.load(open(infer_path, 'r'))]

    json.dump(train_new_data, open(train_path, 'w'))
    json.dump(valid_new_data, open(valid_path, 'w'))
    json.dump(infer_new_data, open(infer_path, 'w'))