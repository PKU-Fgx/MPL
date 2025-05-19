# 数据预处理工具

这个工具用于处理和格式化多个信息抽取任务的数据集，包括命名实体识别(NER)、关系抽取(RE)、事件论元抽取(EAE)和事件抽取(EE)。

## 支持的任务和数据集

### 命名实体识别 (NER)
- ACE05
- CoNLL03
- OntoNotes5
- BC5CDR
- DIANN
- NCBIDisease
- WNUT2017

### 关系抽取 (RE)
- ACE05
- CoNLL04

### 事件论元抽取 (EAE)
- ACE05
- RAMS

### 事件抽取 (EE)
- ACE05

## 数据格式

### 输入数据格式
原始数据应存放在 `./Raw/` 目录下，按任务类型分类：
- `./Raw/NER/`
- `./Raw/RE/`
- `./Raw/EAE/`
- `./Raw/EE/`

每个任务目录下需要包含：
- `label_exp_new.json`: 标签定义和示例
- `label_map.json`: 标签映射关系
- `train.json`: 训练数据
- `test.json`: 测试数据

### 输出数据格式
处理后的数据将保存在 `./Formatted/` 目录下，按任务类型分类：
- `./Formatted/NER_*`
- `./Formatted/RE_*`
- `./Formatted/EAE_*`
- `./Formatted/EE_*`

输出文件为JSONL格式，每行包含：
- idx: 样本索引
- task: 任务类型
- dataset: 数据集名称
- language: 输出语言（python/cpp/java/nl）
- prompt_in: 输入提示
- prompt_ot: 输出提示
- mentions: 标注信息

## 使用方法

1. 准备原始数据，按照上述目录结构放置
2. 运行处理脚本：
```bash
python build.py
```

脚本将自动处理所有任务的数据，生成训练集和测试集。

## 数据集组合

使用 `generate_datasets.ipynb` 可以将所有处理后的数据集组合成一个统一的训练集。组合后的数据将保存在 `../dataTrain/` 目录下。

组合后的数据格式为JSONL，每行包含：
- dataset: 原始数据集名称
- id: 样本唯一标识符（格式：`{language}_{idx}`）
- messages: 对话格式的数据
  - role: 角色（user/assistant）
  - content: 内容（prompt_in/prompt_ot）

## 输出语言支持

支持四种输出格式：
- Python
- C++
- Java
- 自然语言描述

## 注意事项

- OntoNotes5数据集的训练集会被随机采样至30000条
- 每个样本会生成四种不同语言的输出格式
- 确保原始数据格式正确，包含必要的标签定义和映射文件
- 数据集组合过程会保留所有语言版本的样本
