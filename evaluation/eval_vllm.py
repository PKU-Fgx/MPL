import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3"

import json
import numpy as np

from fire import Fire
from tqdm import tqdm
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
from vllm.lora.request import LoRARequest

def main(
    batch_size = 64,
    task_name = "main",
    model_id = "mpl_ftq_llama3_8b_3E4",
    base_model_path = "meta-llama/Meta-Llama-3-8B",
    epoch_num = 2,
    lan = "python"
):
    concat_messages = lambda x: "<|user|>\n" + x["prompt_in"].strip() + "\n" + "<|assistant|>\n"
    
    tasks = ['EAE_ACE05', 'EAE_RAMS', 'EE_ACE05', 'RE_ACE05', 'RE_CoNLL04',
                'NER_ACE05', 'NER_BC5CDR', 'NER_CoNLL03', 'NER_DIANN', 'NER_NCBIDisease', 'NER_OntoNotes5', 'NER_WNUT2017']

    qlora_config_path = f"<SAVE_PATH>/{model_id}/epoch_{epoch_num}"

    test_data_root = "../dataPreparation/Formatted/{}/test.jsonl"
    data_path_list = sorted([test_data_root.format(t) for t in tasks])
    output_path_root = f"./generated/{model_id}/epoch_{epoch_num}/generated_qlora"

    tokenizer = AutoTokenizer.from_pretrained(base_model_path, padding_side='left')
    tokenizer.pad_token = tokenizer.eos_token

    sampling_params = SamplingParams(
        temperature=0.2, max_tokens=1024, n=4, best_of=4,
        stop_token_ids=[tokenizer.eos_token_id, tokenizer.pad_token_id]
    )
    
    llm = LLM(
        model=base_model_path, dtype="bfloat16", tensor_parallel_size=4,
        gpu_memory_utilization=0.98, trust_remote_code=True, enable_lora=True,
        max_lora_rank=128
    )

    for data_path in data_path_list:
        if lan in ['python', 'cpp', 'java']:
            input_data = [elem for elem in list(map(json.loads, open(data_path, "r").readlines())) if lan in elem['language']]
        else:
            input_data = [elem for elem in list(map(json.loads, open(data_path, "r").readlines())) if elem['language'] != 'nl' ]

        dataset_name = data_path.split("/")[-2]
        output_path = f"{output_path_root}/{dataset_name}/pred_0.json"
        os.makedirs("/".join(output_path.split("/")[:-1]), exist_ok=True)

        if os.path.exists(output_path):
            continue

        splitted_data_length = len(input_data)
        data_length_per_batch = splitted_data_length // batch_size
        data_batched = np.array_split(input_data, data_length_per_batch)

        output_list = list()
        for item in tqdm(data_batched, desc=f"Task: {dataset_name} | Epoch: {epoch_num}"):
            prompts = [concat_messages(one) for one in item]
            outputs = llm.generate(
                prompts, sampling_params, lora_request=LoRARequest("QLora", 1, qlora_config_path), use_tqdm=False
            )
            
            for i, output in enumerate(outputs):
                output_list.append({
                    "idx": item[i]["idx"],
                    "task": item[i]["task"],
                    "dataset": item[i]["dataset"],
                    "language": item[i]["language"],
                    "pred": [gen_output.text for gen_output in output.outputs],
                    "prompt_ot": item[i]["prompt_ot"],
                    "glod": item[i]['mentions']
                })
                
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_list, f, ensure_ascii=False)

def enter(
    start=4, model_id="mpl_ftq_llama3_8b_3E4",
    base_model_path="meta-llama/Meta-Llama-3-8B", lan="all"
):
    main(task_name="main", model_id=model_id, base_model_path=base_model_path, epoch_num=start, lan=lan)

if __name__ == "__main__":
    Fire(enter)