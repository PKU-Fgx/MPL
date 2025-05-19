import re
from collections import Counter

def get_format_ner(input_text, lan):
    if lan == "python":
        pattern_sentence = r"entity_list.append(.+)"
        pattern_label = r"((.+)(\"(.+)\"))"
        pattern_entity = r"\"(.+)\""
    elif lan == "cpp":
        pattern_sentence = r"entityList.push_back(.+)"
        pattern_label = r"(new (.+)(\"(.+)\"))"
        pattern_entity = r"\"(.+)\""
    else:
        pattern_sentence = r"entityList.add(.+)"
        pattern_label = r"(new (.+)(\"(.+)\"))"
        pattern_entity = r"\"(.+)\""

    output_list = list()
    for line in input_text.split("\n"):
        if '>>>' in line:
            continue
        match = re.search(pattern_sentence, line)
        if match:
            try:
                label_text = match.group(1)
                label = re.search(pattern_label, label_text).group(2).strip('(').strip(')')
                entity = re.search(pattern_entity, label_text).group(1).strip('(').strip(')')
            except:
                continue

            output_list.append({'type': label, 'offset': [1], 'text': entity})
        else:
            continue
            
    return output_list

def get_format_re(input_text, lan):
    if lan == "python":
        pattern_sentence = r"relation_list.append(.+)" 
        # pattern_label = r"((.+)(head_entity=\"(.+)\", tail_entity=\"(.+)\"))"
        # pattern_entity = r"((.+)(head_entity=\"(.+)\", tail_entity=\"(.+)\"))"
        pattern_label = r"((.+)(\"(.+)\", \"(.+)\"))"
        pattern_entity = r"((.+)(\"(.+)\", \"(.+)\"))"
    elif lan == "cpp":
        pattern_sentence = r"relationList.push_back(.+)" 
        pattern_label  = r"(new (.+)(\"(.+)\", \"(.+)\"))"
        pattern_entity = pattern_label
    else:
        pattern_sentence = r"relationList.add(.+)" 
        pattern_label = r"(new (.+)(\"(.+)\", \"(.+)\"))"
        pattern_entity = pattern_label

    output_list = list()
    for line in input_text.split("\n"):
        if '>>>' in line:
            continue
        match = re.search(pattern_sentence, line)
        if match:
            try:
                label_text = re.search(pattern_sentence, line).group(1)
                label = re.search(pattern_label, label_text).group(2).strip('(').strip(')')
                entity_head = re.search(pattern_entity, label_text).group(4).strip('(').strip(')')
                entity_tail = re.search(pattern_entity, label_text).group(5).strip('(').strip(')')

                output_list.append({
                    'type': label,
                    'args': sorted([
                        {'type': 'Entity', 'offset': [1], 'text': entity_head},
                        {'type': 'Entity', 'offset': [1], 'text': entity_tail}
                    ], key=lambda x: x['text'])
                })
            except:
                continue
        else:
            continue
            
    return output_list

def get_format_re_2(input_text, lan):
    if lan == "python":
        pattern_sentence = r"relation_list.append(.+)" 
        pattern_label = r"((.+)(head_entity=\"(.+)\", tail_entity=\"(.+)\"))"
        pattern_entity = r"((.+)(head_entity=\"(.+)\", tail_entity=\"(.+)\"))"
        # pattern_label = r"((.+)(\"(.+)\", \"(.+)\"))"
        # pattern_entity = r"((.+)(\"(.+)\", \"(.+)\"))"
    elif lan == "cpp":
        pattern_sentence = r"relationList.push_back(.+)" 
        pattern_label  = r"(new (.+)(\"(.+)\", \"(.+)\"))"
        pattern_entity = pattern_label
    else:
        pattern_sentence = r"relationList.add(.+)" 
        pattern_label = r"(new (.+)(\"(.+)\", \"(.+)\"))"
        pattern_entity = pattern_label

    output_list = list()
    for line in input_text.split("\n"):
        match = re.search(pattern_sentence, line)
        if match:
            try:
                label_text = re.search(pattern_sentence, line).group(1)
                label = re.search(pattern_label, label_text).group(2).strip('(').strip(')')
                entity_head = re.search(pattern_entity, label_text).group(4).strip('(').strip(')')
                entity_tail = re.search(pattern_entity, label_text).group(5).strip('(').strip(')')
            except:
                continue

            output_list.append({
                'type': label,
                'args': sorted([
                    {'type': 'Entity', 'offset': [1], 'text': entity_head},
                    {'type': 'Entity', 'offset': [1], 'text': entity_tail}
                ], key=lambda x: x['text'])
            })
        else:
            continue
            
    return output_list

def get_format_eae(input_text, lan):
    if lan == "python":
        pattern_sentence = r"arguments_list.append(.+)" 
        pattern_content  = r"((.+)(\"(.+)\"))"
    elif lan == "cpp":
        pattern_sentence = r"argumentsList.push_back(.+)" 
        pattern_content = r"(new (.+)(\"(.+)\"))"
    else:
        pattern_sentence = r"argumentsList.add(.+)" 
        pattern_content = r"(new (.+)(\"(.+)\"))"

    args = list()
    for line in input_text.split("\n"):
        if '>>>' in line:
            continue
        match = re.search(pattern_sentence, line)
        if match:
            try:
                label_text = re.search(pattern_sentence, line).group(1)
                label = re.search(pattern_content, label_text).group(2).strip('(').strip(')')
                entity = re.search(pattern_content, label_text).group(4).strip('(').strip(')')

                args.append({'type': label, 'offset': [2], 'text': entity})
            except:
                continue
        else:
            continue

    return [{'type': 'EventType', 'offset': [1], 'text': 'EnvetTrigger', 'args': args}]

def get_format_ee(input_text, lan):
    if lan == "python":
        pattern_sentence = r"event_list.append(.+)" 
        pattern_content = r"((.+)\(\"(.+)\", \[(.*)\]\))"
    elif lan == "cpp":
        pattern_sentence = r"eventList.push_back(.+)" 
        pattern_content = r"(new (.+)\(\"(.+)\", \{(.*)\}\))"
    else:
        pattern_sentence = r"eventList.add(.+)" 
        pattern_content = r"(new (.+)\(\"(.+)\", List.of\((.*)\)\))"

    output_list = list()
    for line in input_text.split("\n"):
        if '>>>' in line:
            continue
        match = re.search(pattern_sentence, line)
        if match:
            try:
                label_text = re.search(pattern_sentence, line).group(1)
                label = re.search(pattern_content, label_text).group(2).strip('(').strip(')')
                entity = re.search(pattern_content, label_text).group(3).strip('(').strip(')')

                output_list.append({'type': label, 'offset': [1], 'text': entity, 'args': [{'type': 'TEMP', 'offset': [2], 'text': 'TEMP'}]})
            except:
                continue
        else:
            continue
            
    return output_list

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# 撰写投票的逻辑，不同的任务写一个函数
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def ner_voter(pred_list, n=1):
    return_list = list()
    for py, cp, ja in zip(*pred_list):
        temp_save = list()

        py_type = [f"{item['type']} | {item['text']}" for item in py] if len(py) != 0 else []
        cp_type = [f"{item['type']} | {item['text']}" for item in cp] if len(cp) != 0 else []
        ja_type = [f"{item['type']} | {item['text']}" for item in ja] if len(ja) != 0 else []

        total_pred = Counter(py_type + cp_type + ja_type)

        for k, v in total_pred.items():
            if v >= n:
                temp_save.append({'type': k.split(' | ')[0], 'offset': [1], 'text': k.split(' | ')[-1]})
                    
        return_list.append(temp_save)
        
    return return_list
    
def ner_voter_2(pred_list, n=1):
    return_list = list()
    for py, cp, ja in zip(*pred_list):
        temp_save = list()

        py_text = [f"{item['text']}" for item in py] if len(py) != 0 else []
        cp_text = [f"{item['text']}" for item in cp] if len(cp) != 0 else []
        ja_text = [f"{item['text']}" for item in ja] if len(ja) != 0 else []

        py_type = [f"{item['type']} | {item['text']}" for item in py] if len(py) != 0 else []
        cp_type = [f"{item['type']} | {item['text']}" for item in cp] if len(cp) != 0 else []
        ja_type = [f"{item['type']} | {item['text']}" for item in ja] if len(ja) != 0 else []

        type_dict = dict()
        for item in py_type + cp_type + ja_type:
            if " | ".join(item.split(" | ")[1:]) in type_dict.keys():
                type_dict[" | ".join(item.split(" | ")[1:])].append(item.split(" | ")[0])
            else:
                type_dict[" | ".join(item.split(" | ")[1:])] = [item.split(" | ")[0]]
                
        type_dict = {k: sorted(list(Counter(v).items()), key = lambda x: x[-1], reverse=True) for k, v in type_dict.items()}
        total_pred = Counter(py_text + cp_text + ja_text)

        for k, v in total_pred.items():
            if v >= n:
                temp_save.append({'type': type_dict[k][0][0], 'offset': [1], 'text': k})
                    
        return_list.append(temp_save)
        
    return return_list
    
def re_voter(pred_list, n=2):
    return_list = list()
    for py, cp, ja in zip(*pred_list):
        temp_save = list()
        py = [f"{item['type']} | {item['args'][0]['text']} | {item['args'][1]['text']}" for item in py]
        cp = [f"{item['type']} | {item['args'][0]['text']} | {item['args'][1]['text']}" for item in cp]
        ja = [f"{item['type']} | {item['args'][0]['text']} | {item['args'][1]['text']}" for item in ja]
        total_pred = Counter(py + cp + ja)
        
        for k, v in total_pred.items():
            if v >= n:
                temp_save.append({
                    'type': k.split(' | ')[0],
                    'args': [
                        {'type': 'Entity', 'offset': [1], 'text': k.split(' | ')[1]},
                        {'type': 'Entity', 'offset': [1], 'text': k.split(' | ')[2]}
                    ]
                })
        return_list.append(temp_save)
        
    return return_list

def re_voter_2(pred_list, n=3):
    return_list = list()
    for py, cp, ja in zip(*pred_list):
        temp_save = list()
        py = [f"{item['type']} | {item['args'][0]['text']} | {item['args'][1]['text']}" for item in py]
        cp = [f"{item['type']} | {item['args'][0]['text']} | {item['args'][1]['text']}" for item in cp]
        ja = [f"{item['type']} | {item['args'][0]['text']} | {item['args'][1]['text']}" for item in ja]
        total_pred = Counter(py + cp + ja)
        
        for k, v in total_pred.items():
            if v >= n:
                temp_save.append({
                    'type': k.split(' | ')[0],
                    'args': [
                        {'type': 'Entity', 'offset': [1], 'text': k.split(' | ')[1]},
                        {'type': 'Entity', 'offset': [1], 'text': k.split(' | ')[2]}
                    ]
                })
        return_list.append(temp_save)
        
    return return_list

def eae_voter(pred_list, n=2):
    return_list = list()
    for py, cp, ja in zip(*pred_list):
        temp_save = list()

        py_text = [f"{item['text']}" for item in py[0]['args']] if len(py) != 0 else []
        cp_text = [f"{item['text']}" for item in cp[0]['args']] if len(cp) != 0 else []
        ja_text = [f"{item['text']}" for item in ja[0]['args']] if len(ja) != 0 else []

        py_type = [f"{item['type']} | {item['text']}" for item in py[0]['args']] if len(py) != 0 else []
        cp_type = [f"{item['type']} | {item['text']}" for item in cp[0]['args']] if len(cp) != 0 else []
        ja_type = [f"{item['type']} | {item['text']}" for item in ja[0]['args']] if len(ja) != 0 else []

        type_dict = dict()
        for item in py_type + cp_type + ja_type:
            if " | ".join(item.split(" | ")[1:]) in type_dict.keys():
                type_dict[" | ".join(item.split(" | ")[1:])].append(item.split(" | ")[0])
            else:
                type_dict[" | ".join(item.split(" | ")[1:])] = [item.split(" | ")[0]]
                
        type_dict = {k: sorted(list(Counter(v).items()), key = lambda x: x[-1], reverse=True) for k, v in type_dict.items()}
        total_pred = Counter(py_text + cp_text + ja_text)

        for k, v in total_pred.items():
            if v >= n:
                temp_save.append({'type': type_dict[k][0][0], 'offset': [2], 'text': k})
                    
        return_list.append([{'type': 'EventType', 'offset': [1], 'text': 'EnvetTrigger', 'args': temp_save}])
        
    return return_list

def eae_voter_2(pred_list, n=2):
    return_list = list()
    for py, cp, ja in zip(*pred_list):
        temp_save = list()

        py_type = [f"{item['type']} | {item['text']}" for item in py[0]['args']] if len(py) != 0 else []
        cp_type = [f"{item['type']} | {item['text']}" for item in cp[0]['args']] if len(cp) != 0 else []
        ja_type = [f"{item['type']} | {item['text']}" for item in ja[0]['args']] if len(ja) != 0 else []
        total_pred = Counter(py_type + cp_type + ja_type)

        for k, v in total_pred.items():
            if v >= n:
                temp_save.append({'type': k.split(' | ')[0], 'offset': [2], 'text': k.split(' | ')[1]})
                    
        return_list.append([{'type': 'EventType', 'offset': [1], 'text': 'EnvetTrigger', 'args': temp_save}])
        
    return return_list

def ee_voter(pred_list, n=2):
    return_list = list()
    for py, cp, ja in zip(*pred_list):

        temp_save = list()
        temp_event_save = list()

        py_text = [f"{item['text']}" for item in py] if len(py) != 0 else []
        cp_text = [f"{item['text']}" for item in cp] if len(cp) != 0 else []
        ja_text = [f"{item['text']}" for item in ja] if len(ja) != 0 else []

        py_type = [f"{item['type']}|{item['text']}" for item in py] if len(py) != 0 else []
        cp_type = [f"{item['type']}|{item['text']}" for item in cp] if len(cp) != 0 else []
        ja_type = [f"{item['type']}|{item['text']}" for item in ja] if len(ja) != 0 else []

        type_dict = dict()
        for item in py_type + cp_type + ja_type:
            if "|".join(item.split("|")[1:]) in type_dict.keys():
                type_dict["|".join(item.split("|")[1:])].append(item.split("|")[0])
            else:
                type_dict["|".join(item.split("|")[1:])] = [item.split("|")[0]]
                
        type_dict = {k: sorted(list(Counter(v).items()), key = lambda x: x[-1], reverse=True) for k, v in type_dict.items()}
        total_pred = Counter(py_text + cp_text + ja_text)
        
        for k, v in total_pred.items():
            if v >= n:
                temp_event_save.append(f"{type_dict[k][0][0]}|{k}")

        event_args_map = dict()
        for item in py + cp + ja:
            if f"{item['type']}|{item['text']}" in temp_event_save:
                if f"{item['type']}|{item['text']}" not in event_args_map.keys():
                    event_args_map[f"{item['type']}|{item['text']}"] = [f"{e['type']}|{e['text']}" for e in item['args']]
                else:
                    event_args_map[f"{item['type']}|{item['text']}"] += [f"{e['type']}|{e['text']}" for e in item['args']]
                    
        event_args_map = {k: Counter(v) for k, v in event_args_map.items()}
        for k, v in event_args_map.items():
            temp_save.append({
                'type': k.split('|')[0], 'offset': [1], 'text': k.split('|')[1],
                'args': [{'type': e_k.split('|')[0], 'offset': [2], 'text': e_k.split('|')[1]} for e_k, e_v in v.items() if e_v >= 2]
            })

        return_list.append(temp_save)
        
    return return_list

def ee_voter_2(pred_list, n=2):
    return_list = list()
    for py, cp, ja in zip(*pred_list):
        temp_save = list()
        py_type = [f"{item['type']} | {item['text']}" for item in py] if len(py) != 0 else []
        cp_type = [f"{item['type']} | {item['text']}" for item in cp] if len(cp) != 0 else []
        ja_type = [f"{item['type']} | {item['text']}" for item in ja] if len(ja) != 0 else []
        total_pred = Counter(py_type + cp_type + ja_type)
        
        for k, v in total_pred.items():
            if v >= n:
                temp_save.append({
                    'type': k.split(' | ')[0], 'offset': [1], 'text': k.split(' | ')[1],
                    'args': []
                })
        return_list.append(temp_save)
        
    return return_list