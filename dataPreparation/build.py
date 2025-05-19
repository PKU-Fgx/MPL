import re
import os
import glob
import json

from prompt import *
from tqdm.notebook import tqdm
from random import sample, choice, randint

def get_ner_formatted(mode="test"):
    
    LABEL_DEF_python = """        `{label_name}`: {defination}  # Examples: {exp}"""
    LABEL_DEF_cpp    = """        `{label_name}`: {defination}  // Examples: {exp}"""
    LABEL_DEF_java   = """        `{label_name}`: {defination}  // Examples: {exp}"""
    LABEL_DEF_nl     = """`{label_name}`: {defination} (Examples: {exp})"""

    ANSWER_FORMAT_python = """entity_list.append({}("{}"))"""
    ANSWER_FORMAT_cpp    = """    entityList.push_back(new {}("{}"));"""
    ANSWER_FORMAT_java   = """        entityList.add(new {}("{}"));"""
    ANSWER_FORMAT_nl   = """"{}": `{}`"""

    for task in ['ACE05', 'CoNLL03', 'OntoNotes5', 'BC5CDR', 'DIANN', 'NCBIDisease', 'WNUT2017']:
        label_raw_dict = json.load(open("./Raw/NER/{}/label_exp_new.json".format(task), 'r'))
        label_map_from_raw_to_target = json.load(open("./Raw/NER/{}/label_map.json".format(task), 'r'))
        data = json.load(open("./Raw/NER/{}/{}.json".format(task, mode), 'r'))

        if task == 'OntoNotes5' and mode=='train':
            data = sample(data, k=30000)
        
        output_path = "./Formatted/NER_{}".format(task)
        os.makedirs(output_path, exist_ok=True)
        fw = open(os.path.join(output_path, "{}.jsonl".format(mode)), 'w')
        
        for idx, s in enumerate(tqdm(data, desc="Mode: {} | Task: {}".format(mode, task))):
            for language in ['python', 'cpp', 'java', 'nl']:
                
                label_content_text = "\n".join([
                    eval(f"LABEL_DEF_{language}").format(label_name=k, defination=v) for k, v in choice(label_raw_dict).items()
                ])
                output_content = "\n".join([
                    eval(f"ANSWER_FORMAT_{language}").format(label_map_from_raw_to_target[m[1]], m[0]) for m in s['mentions']
                ])
                instance = eval(f"TEMPLATE_NER_{language}").format(
                    entities_defination=label_content_text, input_text=s['sentence'], output_text=output_content
                )
                
                fw.write(json.dumps({
                    "idx": idx,
                    "task": "NER",
                    "dataset": task,
                    "language": language,
                    "prompt_in": instance.split("<SPLIT>")[0].strip(),
                    "prompt_ot": instance.split("<SPLIT>")[1].strip('\n'),
                    "mentions": [[item[0], label_map_from_raw_to_target[item[1]]] for item in s['mentions']]
                }) + "\n")
                
        fw.close()

def get_re_formatted(mode="test"):

    LABEL_DEF_python = """        `{label_name}`: {defination}"""
    LABEL_DEF_cpp    = """        `{label_name}`: {defination}"""
    LABEL_DEF_java   = """        `{label_name}`: {defination}"""
    LABEL_DEF_nl     = """`{label_name}`: {defination} (Examples: {exp})"""

    ANSWER_FORMAT_python = """relation_list.append({}("{}", "{}"))"""
    ANSWER_FORMAT_cpp    = """    relationList.push_back(new {}("{}", "{}"));"""
    ANSWER_FORMAT_java   = """        relationList.add(new {}("{}", "{}"));"""
    ANSWER_FORMAT_nl   = """{}("{}", "{}")"""

    for task in ['ACE05', 'CoNLL04']:
        label_raw_dict = json.load(open("./Raw/RE/{}/label_exp_new.json".format(task), 'r'))
        label_map_from_raw_to_target = json.load(open("./Raw/RE/{}/label_map.json".format(task), 'r'))
        data = json.load(open("./Raw/RE/{}/{}.json".format(task, mode), 'r'))
        
        output_path = "./Formatted/RE_{}".format(task)
        os.makedirs(output_path, exist_ok=True)
        fw = open(os.path.join(output_path, "{}.jsonl".format(mode)), 'w')
        
        for idx, s in enumerate(tqdm(data, desc="Mode: {} | Task: {}".format(mode, task))):
            for language in ['python', 'cpp', 'java', 'nl']:
                
                label_content_text = "\n".join([
                    eval(f"LABEL_DEF_{language}").format(label_name=k, defination=v) for k, v in choice(label_raw_dict).items()
                ])
                entities = ', '.join([f'"{e}"' for e in set(s['entities'])])
                
                output_content = "\n".join([eval(f"ANSWER_FORMAT_{language}").format(
                    label_map_from_raw_to_target[m['realtion_type']], m['head_entity'], m['tail_entity']
                ) for m in s['relation_mentions']])
                instance = eval(f"TEMPLATE_RE_{language}").format(
                    entities=entities, relations_defination=label_content_text, input_text=s['sentence'], output_text=output_content
                )
    
                fw.write(json.dumps({
                    "idx": idx,
                    "task": "RE",
                    "dataset": task,
                    "language": language,
                    "prompt_in": instance.split("<SPLIT>")[0].strip(),
                    "prompt_ot": instance.split("<SPLIT>")[1].strip('\n'),
                    "mentions": [
                        [
                            item['head_entity'], item['tail_entity'], label_map_from_raw_to_target[item['realtion_type']]
                        ] for item in s['relation_mentions']
                    ]
                }) + "\n")
            
        fw.close()

def get_eae_formatted(mode="test"):

    LABEL_DEF_python = """        `{label_name}`: {defination}  # Examples: {exp}"""
    LABEL_DEF_cpp    = """        `{label_name}`: {defination}  // Examples: {exp}"""
    LABEL_DEF_java   = """        `{label_name}`: {defination}  // Examples: {exp}"""
    LABEL_DEF_nl     = """`{label_name}`: {defination} (Examples: {exp})"""

    ANSWER_FORMAT_python = """arguments_list.append({}("{}"))"""
    ANSWER_FORMAT_cpp    = """    argumentsList.push_back(new {}("{}"));"""
    ANSWER_FORMAT_java   = """        argumentsList.add(new {}("{}"));"""
    ANSWER_FORMAT_nl     = """"{}": `{}`"""

    for task in ['ACE05', 'RAMS']:
        label_raw_dict = json.load(open("./Raw/EAE/{}/label_exp_new.json".format(task), 'r'))
        label_map_from_raw_to_target = json.load(open("./Raw/EAE/{}/label_map.json".format(task), 'r'))
        data = json.load(open("./Raw/EAE/{}/{}.json".format(task, mode), 'r'))
        
        output_path = "./Formatted/EAE_{}".format(task)
        os.makedirs(output_path, exist_ok=True)
        fw = open(os.path.join(output_path, "{}.jsonl".format(mode)), 'w')

        for idx, s in enumerate(tqdm(data, desc="Mode: {} | Task: {}".format(mode, task))):
            for language in ['python', 'cpp', 'java', 'nl']:
                qn = lambda x: x.replace('1', '').replace('2', '')
                
                label_content_text = "\n".join([eval(f"LABEL_DEF_{language}").format(
                    label_name=qn(l), defination=choice(label_raw_dict)[qn(l)]
                ) for l in s['labels']])
                output_content = "\n".join([
                    eval(f"ANSWER_FORMAT_{language}").format(qn(m['role']), m['text']) for m in s['arguments']
                ])
                instance = eval(f"TEMPLATE_EAE_{language}").format(
                    trigger = s['trigger_word'], event_type = label_map_from_raw_to_target[s['event_type']],
                    arguments_defination=label_content_text, input_text=s['sentence'], output_text=output_content
                )
                
                fw.write(json.dumps({
                    "idx": idx,
                    "task": "EAE",
                    "dataset": task,
                    "language": language,
                    "prompt_in": instance.split("<SPLIT>")[0].strip(),
                    "prompt_ot": instance.split("<SPLIT>")[1].strip('\n'),
                    "mentions": [[item['role'], item['text']] for item in s['arguments']]
                }) + "\n")
            
        fw.close()

def get_ee_formatted(mode="test"):

    LABEL_DEF_python = """        `{label_name}`: {defination}"""
    LABEL_DEF_cpp    = """        `{label_name}`: {defination}"""
    LABEL_DEF_java   = """        `{label_name}`: {defination}"""
    LABEL_DEF_nl     = """`{label_name}`: {defination}"""

    ANSWER_FORMAT_python = """event_list.append({}("{}", [{}]))"""
    ANSWER_FORMAT_cpp    = """    eventList.push_back(new {}("{}", {{{}}}));"""
    ANSWER_FORMAT_java   = """        eventList.add(new {}("{}", List.of({})));"""
    ANSWER_FORMAT_nl   = """"{}": `{}` (Args: {})"""

    ARGUMENTS_TEMP_python = 'Arguments("{}", "{}")'
    ARGUMENTS_TEMP_cpp    = 'Arguments("{}", "{}")'
    ARGUMENTS_TEMP_java   = 'new Arguments("{}", "{}")'
    ARGUMENTS_TEMP_nl     = "{}('{}')"

    for task in ['ACE05']:
        label_raw_dict = json.load(open("./Raw/EE/{}/label_exp_new.json".format(task), 'r'))
        label_map_from_raw_to_target = json.load(open("./Raw/EE/{}/label_map.json".format(task), 'r'))
        data = json.load(open("./Raw/EE/{}/{}.json".format(task, mode), 'r'))

        output_path = "./Formatted/EE_{}".format(task)
        os.makedirs(output_path, exist_ok=True)
        fw = open(os.path.join(output_path, "{}.jsonl".format(mode)), 'w')

        for idx, s in enumerate(tqdm(data, desc="Mode: {} | Task: {}".format(mode, task))):
            for language in ['python', 'cpp', 'java', 'nl']:

                label_content_text = "\n".join([eval(f"LABEL_DEF_{language}").format(
                    label_name=k, defination=v
                ) for k, v in choice(label_raw_dict).items()])
    
                output_content = "\n".join([eval(f"ANSWER_FORMAT_{language}").format(
                    label_map_from_raw_to_target[m['event_type']],
                    m['trigger'], ", ".join([eval(f"ARGUMENTS_TEMP_{language}").format(a['text'], a['role']) for a in m['arguments']])
                ) for m in s['event_mentions']])
    
                instance = eval(f"TEMPLATE_EE_{language}").format(events_defination=label_content_text, input_text=s['sentence'], output_text=output_content)
    
                fw.write(json.dumps({
                    "idx": idx,
                    "task": "EE",
                    "dataset": task,
                    "language": language,
                    "prompt_in": instance.split("<SPLIT>")[0].strip(),
                    "prompt_ot": instance.split("<SPLIT>")[1].strip('\n'),
                    "mentions": [
                        [
                            label_map_from_raw_to_target[item['event_type']], item['trigger'], item['arguments']
                        ] for item in s['event_mentions']
                    ]
                }) + "\n")
            
        fw.close()

if __name__ == "__main__":
    get_ner_formatted(mode="train")
    get_ner_formatted(mode="test")

    get_re_formatted(mode="train")
    get_re_formatted(mode="test")

    get_eae_formatted(mode="train")
    get_eae_formatted(mode="test")

    get_ee_formatted(mode="train")
    get_ee_formatted(mode="test")