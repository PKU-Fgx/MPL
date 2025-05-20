<p align="center">
    <br>
    <img src="assets/MPL-Logo.png" style="height: 250px;">
    <br>
    <h2 align="center">MPL: Multiple Programming Languages with Large Language Models for Information Extraction</h2>
    <hr>

<p align="center">
    <a href=""><img alt="GitHub license" src="https://img.shields.io/github/license/PKU-Fgx/transformers"></a>
    <a href="https://huggingface.co/collections/pku-fanggx/mpl-682c3bc6135458f10802720b"><img alt="Pretrained Models" src="https://img.shields.io/badge/🤗HuggingFace-Pretrained Models-green"></a>
    <a href=""><img alt="Paper" src="https://img.shields.io/badge/📖-Paper-orange"></a>
    <br>
</p>

<p align="justify">
We present<i> MPL: Multiple Programming Languages with Large Language Models for Information Extraction</i>. Recent advances in information extraction (IE) have explored the use of code-style prompts to improve structured output generation. This approach leverages the inherent structure of programming languages (PLs), which are often more precise and organized than natural language. While most existing work focuses on Python as the primary PL for simulation and fine-tuning, our framework MPL extends this paradigm by incorporating multiple widely-used programming languages , such as C++, Java, and Python, into the supervised fine-tuning (SFT) process. This allows the model to learn cross-language structural patterns that enhance IE performance. To further improve the code-style simulation, we introduce a novel function-prompt with virtual running , enabling more effective and efficient generation of structured outputs. This repository contains the implementation, training scripts, and evaluation tools for MPL. Please refer to the supplementary materials for more details and trained models.

- 📖 Paper: [MPL: Multiple Programming Languages with Large Language Models for Information Extraction]()
</p>

<p align="center">
<img src="assets/main.png">
</p>

## 🏗️ Repo Structure

```text
project/
├── dataPreparation/          # 数据预处理模块
│   ├── Formatted/            # 格式化后数据输出
│   ├── Raw/                  # 原始数据与相关处理
│   │   ├── EAE/
│   │   ├── EE/
│   │   ├── NER/
│   │   └── RE/
│   ├── build.py              # 将原始构建成格式化后的数据
│   ├── prompt.py             # IE 数据转换成 Code 形式的 Format Prompt
│   └── generate_datasets.ipynb  # 生成用于训练的完整数据集
├── train/                    # 训练相关代码
│   ├── scripts/              # 训练脚本
│   ├── open_instruct/        # 训练核心代码
│   └── run_mpl.sh            # 入口脚本
├── evaluation/               # 评估模块
└── dataTrain/                # 训练数据存储
```

## 📥 Installation

1. 克隆仓库：
```bash
git clone [repository_url]
cd [repository_name]
```

2. 安装依赖：
```bash
# Environment setup
conda create -n MPL python=3.12 -y
conda activate MPL

# install dependencies
pip install -r requirements.txt
```

## 🏋️ 训练步骤

### 1. 数据预处理

1. 获取原始数据集

    | Task | Dataset | Link | Label Explanations | Domain |
    |------|---------|------|--------------------|--------|
    | NER | ACE05 | [ACE 2005](https://catalog.ldc.upenn.edu/LDC2006T06 ) | ✅ | News |
    | NER | BC5CDR | [tner/bc5cdr](https://huggingface.co/datasets/tner/bc5cdr) | ❌ | Biomedical |
    | NER | CoNLL03 | [conll2003](https://www.clips.uantwerpen.be/conll2003/ner/) | ❌ | News |
    | NER | DIANN | [diann-sentences-english](https://huggingface.co/datasets/ferrazzipietro/diann-sentences-english) | ❌ | Biomedical |
    | NER | NCBID | [ncbi-disease](https://huggingface.co/datasets/nr2n23/ncbi-disease-sequence-classification) | ❌ | Biomedical |
    | NER | OntoNotes5* | [OntoNotes 5.0](https://www.ldc.upenn.edu/) | ❌ | News |
    | NER | WNUT2017 | [tner/wnut2017](https://huggingface.co/datasets/tner/wnut2017) | ❌ | News |
    | RE | ACE05 | [ACE 2005](https://catalog.ldc.upenn.edu/LDC2006T06) | ✅ | News |
    | RE | CoNLL04 | [DFKI-SLT/conll04](DFKI-SLT/conll04) | ❌ | News |
    | EAE | ACE05 | [ACE 2005](https://catalog.ldc.upenn.edu/LDC2006T06 ) | ✅ | News |
    | EAE | RAMS | [RAMS](https://nlp.jhu.edu/rams/) | ❌ | News |
    | EE | ACE05 | [ACE 2005](https://catalog.ldc.upenn.edu/LDC2006T06) | ✅ | News |

    - 其中，部分数据集如 ACE05 会自带标签解释，但是其余数据集不包含标签解释，需要通过 AI 自动生成，我们在 Repo 的 `dataPreparation/Raw/<TASK>` 中提供了一个解释的版本。

    - 另外，为了保持可比较性以及增加训练效率，OntoNotes5 数据集我们从中采样了 30k 条目数据用于训练。

    - 原始数据存放在 `dataPreparation/Raw/<TASK>` 目录下，每个任务目录需包含：
        - `label_exp.json`: 标签定义与解释
        - `label_map.json`: 标签映射
        - `train.json`: 训练数据
        - `dev.json`: 验证集数据
        - `test.json`: 测试数据

2. 将原始数据集处理到中间格式

    - 由于原始数据的格式多种多样，我们在 `dataPreparation/Raw/<TASK>/trans_<TASK>.py` 中提供了将原始格式数据转换成中间格式的参考代码，然后为了将标签格式改为统一，我们在 `dataPreparation/Raw/<TASK>/reformat.py` 中提供了将标签进行格式化统一的参考代码。

    - 为了顺利进行上述工作，我们需要为每个数据集准备 `label_exp.json` 文件，用来表示 `{"label": "Explanation"}`。

    - 具体地，每种数据集的中间格式参考 `dataPreparation/README.md`。

3. 将中间格式的数据集转换成 CodeIE 的形式

    - 经过上述步骤之后，中间格式数据被放置在 `dataPreparation/Raw/<TASK>/<DATASET>/<SPLIT>.json` 之中，可以通过 `dataPreparation/build.py` 生成 CodeIE 形式的数据集，生成后的数据放置于 `dataPreparation/Formatted` 之中。

4. 生成用于训练的训练数据

    - 最后通过 `dataPreparation/generate_datasets.ipynb` 脚本将训练数据按照 open-instruct 的格式进行整合放置于 `dataTrain` 文件夹之中。

### 2. 模型训练

我们使用 [allenai/open-instruct](https://github.com/allenai/open-instruct) 进行微调，详细内容请参考 `train/run_mpl.sh`、`train/scripts/MPL_qlora.sh` 以及 `train/scripts/run.sh` 脚本以获得更多信息。

```bash
# 使用 MPL 训练脚本
bash train/run_mpl.sh
```

#### 2.1 Pretrained models
Meanwhile, we release MPL models based on [CodeLLaMa](https://huggingface.co/codellama) (7B, 13B). The models are available in the 🤗HuggingFace Hub.

| Model |                     🤗 HuggingFace Hub                     |
|-------|:---------------------------------------------------------:|
| MPL-7B |  [pku-fanggx/MPL-7B-Qlora](https://huggingface.co/pku-fanggx/MPL-7B-Qlora)  |
| MPL-13B | [pku-fanggx/MPL-13B-Qlora](https://huggingface.co/pku-fanggx/MPL-13B-Qlora) |

### 3. 模型评估

我们使用 [vllm-project/vllm](https://github.com/vllm-project/vllm) 进行推理评估，请参考 `evaluation/README.md` 以获得更多信息。

```bash
# 使用 vLLM 进行评估
python evaluation/eval_vllm.py --model_id <model_id> --base_model_path <base_model_path> --lan <language>

# 计算评估分数
python evaluation/get_scores.py --model_id <model_id> --method <method>
```

## 📝 Citation
```bibtex
```