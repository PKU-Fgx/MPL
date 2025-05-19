import json

for task in ['ACE05', 'CoNLL03', 'OntoNotes5']:
    train_path = f"./{task}/train.json"
    valid_path = f"./{task}/dev.json"
    infer_path = f"./{task}/test.json"
    
    old_label_set = json.load(open(f"./{task}/label_exp.json", 'r'))[0].keys()
    new_label_set = json.load(open(f"./{task}/label_exp_new.json", 'r'))[0].keys()

    old2new = {k: v for k, v in zip(old_label_set, new_label_set)}
    
    train_new_data = [{
        **line, 'mentions': [[ment[0], old2new[ment[1]]] for ment in line['mentions']]
    } for line in json.load(open(train_path, 'r'))]
    valid_new_data = [{
        **line, 'mentions': [[ment[0], old2new[ment[1]]] for ment in line['mentions']]
    } for line in json.load(open(valid_path, 'r'))]
    infer_new_data = [{
        **line, 'mentions': [[ment[0], old2new[ment[1]]] for ment in line['mentions']]
    } for line in json.load(open(infer_path, 'r'))]

    print(train_new_data[0])

    json.dump(train_new_data, open(train_path, 'w'))
    json.dump(valid_new_data, open(valid_path, 'w'))
    json.dump(infer_new_data, open(infer_path, 'w'))