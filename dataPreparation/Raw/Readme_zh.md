# 信息抽取数据预处理工具

这个项目提供了用于信息抽取(Information Extraction)任务的数据预处理工具，支持多个子任务：命名实体识别(NER)、关系抽取(RE)、事件抽取(EE)和事件论元抽取(EAE)。支持ACE05、CoNLL04和RAMS等数据集的处理和格式转换。

注意：这些代码主要用于参考，您可以根据相关的信息将自己的数据集处理成这种格式方便后续进一步进行处理。

## 项目结构

```
dataPreparation/
├── Raw/
│   ├── NER/                # 命名实体识别
│   │   ├── trans_ner.py    # NER 数据转换脚本
│   │   └── reformat.py     # NER 标签重映射脚本
│   ├── RE/                 # 关系抽取
│   │   ├── trans_re.py     # RE 数据转换脚本
│   │   └── reformat.py     # RE 标签重映射脚本
│   ├── EE/                 # 事件抽取
│   │   ├── trans_ee.py     # EE 数据转换脚本
│   │   └── reformat.py     # EE 标签重映射脚本
│   └── EAE/                # 事件论元抽取
│       ├── trans_eae.py    # EAE 数据转换脚本
│       └── reformat.py     # EAE 标签重映射脚本
```

## 支持的任务和数据集

### 命名实体识别 (NER)
- 数据集：ACE05、BC5CDR、CoNLL03、DIANN、NCBIDisease、OntoNotes5

### 关系抽取 (RE)
- 数据集：ACE05, CoNLL04

### 事件抽取 (EE)
- 数据集：ACE05

### 事件论元抽取 (EAE)
- 数据集：ACE05, RAMS

## 数据格式

#### NER输出格式
```json
{
    "sentence": "完整句子",
    "mentions": [
        ["实体文本", "实体类型"],
        ...
    ]
}
```

#### RE输出格式
```json
{
    "sentence": "完整句子",
    "entities": ["实体1", "实体2", ...],
    "relation_mentions": [
        {
            "head_entity": "头实体",
            "tail_entity": "尾实体",
            "relation_type": "关系类型"
        }
    ]
}
```

#### EE输出格式
```json
{
    "sentence": "完整句子",
    "arg_candi": ["候选实体1", "候选实体2", ...],
    "wrong_list": ["非事件类型1", "非事件类型2", ...],
    "event_mentions": [
        {
            "event_type": "事件类型",
            "trigger": "触发词",
            "arguments": [...]
        }
    ]
}
```

#### EAE输出格式
```json
{
    "sentence": "完整句子",
    "trigger_word": "触发词",
    "event_type": "事件类型",
    "labels": ["论元角色1", "论元角色2", ...],
    "arguments": [...]
}
```

## 使用方法

```bash
# 数据转换
python dataPreparation/Raw/<TASK>/trans_<TASK>.py
# 标签重映射
python dataPreparation/Raw/<TASK>/reformat.py
```

## 依赖项

- Python 3.x
- json
- tqdm

## 注意事项

- 所有输入数据必须符合指定的JSON格式
- 每个任务都需要相应的标签映射文件(label_exp.json)
- 处理后的数据将保存在各任务目录下的Formatted文件夹中
- 确保在运行脚本前准备好所需的标签映射文件

## 标签映射说明

- 每个任务目录下都需要准备label_exp.json文件
- 部分任务支持新旧标签映射(label_exp_new.json)
- 标签映射文件格式为JSON，包含标签的对应关系

## 输出目录

所有处理后的数据将保存在对应任务目录下的Formatted文件夹中，保持原始数据集的划分（train/dev/test）。