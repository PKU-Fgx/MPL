import os
import json
import glob
import pandas as pd

from utils import *
from metric import *
from tqdm import tqdm
from fire import Fire

TASK2S = {
    "ner": [get_format_ner, EntityScorer(), 'string-ent-F1', ner_voter, ner_voter_2, 'string-ent-R'],
    "re": [get_format_re, RelationScorer(), 'string-rel-strict-F1', re_voter, re_voter_2, 'string-rel-strict-R'],
    "ee": [get_format_ee, EventScorer(), 'string-evt-trigger-F1', ee_voter, ee_voter_2, 'string-evt-trigger-R'],
    "eae": [get_format_eae, EventScorer(), 'string-evt-role-F1', eae_voter, eae_voter_2, 'string-evt-role-R'],
}
ROOT = "./generated"

def get_score(model_id, epoch_num, method, lan, tasks, zs=""):
    assert method in ["full", "qlora"]
    NUM_GEN_SENTENCE = 4

    score_dict = list()
    for T in tqdm(tasks):
        upper_task = T.split("_")[0].lower()

        path = os.path.join(ROOT, model_id, f"epoch_{epoch_num}", f"generated_{method}" + zs, T, "pred_*.json")
        output_list = sum([json.load(open(p, "r")) for p in glob.glob(path)], list())
        output_list = [[elem for elem in output_list if elem['language'] == l] for l in ['python', 'cpp', 'java']]

        items_test_list = [[list(
            map(lambda x: {**x, 'pred': x['pred'][i]}, output_list[j])
        ) for i in range(NUM_GEN_SENTENCE)] for j in range(3)]

        def return_score(L, enm):
            lan_map = {0: "python", 1: "cpp", 2: "java"}
            
            gold_list, pred_list = list(), list()
            for item in L:
                pred_list.append(TASK2S[upper_task][0](item['pred'].split('<|assistant|>')[-1], lan_map[enm]))
                gold_list.append(TASK2S[upper_task][0](item['prompt_ot'], lan_map[enm]))
            
            scorer = TASK2S[upper_task][1]

            gold_instance_list = scorer.load_gold_list(gold_list)
            pred_instance_list = scorer.load_gold_list(pred_list)

            return scorer.eval_instance_list(gold_instance_list, pred_instance_list)[TASK2S[upper_task][2]]
            
        def sorted_vote(score_list, items_test_list):
            items_test_list_new = list()
            for ls, sc in zip(items_test_list, score_list):
                temp_save = list()
                for idx, _ in sorted(enumerate(sc), key=lambda x: x[-1], reverse=True):
                    temp_save.append(ls[idx])
                items_test_list_new.append(ls)
            return items_test_list_new
            
        def return_vote_score(L, f=True):
            lan_map = {0: "python", 1: "cpp", 2: "java"}
            if f:
                task_voter = TASK2S[upper_task][3]
            else:
                task_voter = TASK2S[upper_task][4]

            L_0 = sorted(L[0], key=lambda x: int(x['idx']))
            L_1 = sorted(L[1], key=lambda x: int(x['idx']))
            L_2 = sorted(L[2], key=lambda x: int(x['idx']))
            L = [L_0, L_1, L_2]

            gold_list, pred_list = [list() for _ in range(3)], [list() for _ in range(3)]
            for enm, Ll in enumerate(L):
                for item in Ll:
                    pred_list[enm].append(TASK2S[upper_task][0](item['pred'].split('<|assistant|>')[-1], lan_map[enm]))
                    gold_list[enm].append(TASK2S[upper_task][0](item['prompt_ot'], lan_map[enm]))

            scorer = TASK2S[upper_task][1]
            voter_answer = task_voter(pred_list)

            gold_instance_list = scorer.load_gold_list(gold_list[0])
            pred_instance_list = scorer.load_gold_list(voter_answer)

            return scorer.eval_instance_list(gold_instance_list, pred_instance_list)[TASK2S[upper_task][2]]

        def return_union_score(L):
            lan_map = {0: "python", 1: "cpp", 2: "java"}

            L_0 = sorted(L[0], key=lambda x: int(x['idx']))
            L_1 = sorted(L[1], key=lambda x: int(x['idx']))
            L_2 = sorted(L[2], key=lambda x: int(x['idx']))
            L = list(zip(L_0, L_1, L_2))

            gold_list, pred_list = [], []
            for Ll in L:
                temp_pred_list = list()
                for enm, item in enumerate(Ll):
                    temp_pred_list.append(TASK2S[upper_task][0](item['pred'].split('<|assistant|>')[-1], lan_map[enm]))
                    
                    if enm == 0:
                        gold_list.append(TASK2S[upper_task][0](item['prompt_ot'], lan_map[enm]))
                pred_list.append(sum(temp_pred_list, list()))
            
            scorer = TASK2S[upper_task][1]

            gold_instance_list = scorer.load_gold_list(gold_list)
            pred_instance_list = scorer.load_gold_list(pred_list)

            cnt_right, cnt_total = 0, 0 
            for pred_item, gold_item in zip(pred_instance_list, gold_instance_list):
                if 'eae' in upper_task.lower():
                    pred_items = ['{}-{}'.format(item[-1], item[-2]) for item in pred_item['string_role']]
                    gold_items = ['{}-{}'.format(item[-1], item[-2]) for item in gold_item['string_role']]
                elif 'ee' in upper_task.lower():
                    pred_items = ['{}-{}'.format(item[-1], item[-2]) for item in pred_item['string_trigger']]
                    gold_items = ['{}-{}'.format(item[-1], item[-2]) for item in gold_item['string_trigger']]
                else:
                    pred_items = ['{}-{}'.format(item[0], item[1]) for item in pred_item['string']]
                    gold_items = ['{}-{}'.format(item[0], item[1]) for item in gold_item['string']]

                for g in gold_items:
                    if g in pred_items:
                        cnt_right += 1
                    cnt_total += 1

            # return scorer.eval_instance_list(gold_instance_list, pred_instance_list)[TASK2S[upper_task][5]]
            return 100 * cnt_right / cnt_total

        score_list = [[round(return_score(items_test_list[j][i], j), 2) for i in range(NUM_GEN_SENTENCE)] for j in range(3)]
        items_test_list_new = sorted_vote(score_list, items_test_list)
        vote_score_list = [round(return_vote_score([l[i] for l in items_test_list_new], True), 2) for i in range(NUM_GEN_SENTENCE)]
        vote_score_list = [round(return_vote_score([l[i] for l in items_test_list_new], False), 2) for i in range(NUM_GEN_SENTENCE)]
        # union_score_list = [round(return_union_score([l[i] for l in items_test_list_new]), 2) for i in range(NUM_GEN_SENTENCE)]
        
        score_dict.append({
            "task": T,
            "python": score_list[0], "c++": score_list[1], "java": score_list[2],
            "voted_1": vote_score_list, "voted_2": vote_score_list,
        })
        
    return score_dict

def main(i=0, task_name="main", model_id="mpl_ftq_llama3_8b", method = "qlora"):
    lan = "all"
    assert lan in ['cpp', 'python', 'java', 'all']

    epoch_num = i
    
    tasks = ['EAE_ACE05', 'EAE_RAMS', 'EE_ACE05', 'RE_ACE05', 'RE_CoNLL04',
                 'NER_ACE05', 'NER_BC5CDR', 'NER_CoNLL03', 'NER_DIANN', 'NER_NCBIDisease', 'NER_OntoNotes5', 'NER_WNUT2017']

    output = get_score(model_id, epoch_num, method, lan, tasks, "")
    for o in output:
        o.update({
            "py_max": max(o['python']),
            "cp_max": max(o['c++']),
            "ja_max": max(o['java']),
            "mean_score": round((sum(o['python'])/4 + sum(o['c++'])/4 + sum(o['java'])/4) / 3, 2)
        })
    
    df = pd.DataFrame(output)
    os.makedirs(f'./output/{model_id}', exist_ok=True)
    df.to_csv(f'./output/{model_id}/{method}_output_{task_name}_epoch_{i}.csv')

if __name__ == "__main__":
    Fire(main)
