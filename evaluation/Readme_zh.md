# 多语言信息抽取评估工具

这个文件夹下的代码用于评估多语言信息抽取模型的性能，包括命名实体识别(NER)、关系抽取(RE)、事件抽取(EE)和事件论元抽取(EAE)等任务。评估过程支持Python、C++和Java三种编程语言，并提供了多种评估指标和投票机制。

## 环境要求

- Python 3.8+
- CUDA 支持的 GPU
- vLLM
- transformers
- pandas
- tqdm
- fire

## 安装

```bash
pip install vllm transformers pandas tqdm fire
```

## 使用方法

### 1. 模型评估

使用 vLLM 进行模型评估：

```bash
python eval_vllm.py --model_id <model_id> --base_model_path <base_model_path> --lan <language>
```

参数说明：
- `model_id`: 模型ID
- `base_model_path`: 基础模型路径
- `lan`: 目标语言 (python/cpp/java/all)

### 2. 计算评估分数

```bash
python get_scores.py --model_id <model_id> --method <method>
```

参数说明：
- `model_id`: 模型ID
- `method`: 评估方法 (full/qlora)

### 3. 批量评估

使用提供的脚本进行批量评估：

```bash
bash eval_tf2.sh
```

## 评估指标

- NER: Entity F1 Score
- RE: Relation F1 Score
- EE: Event Trigger F1 Score
- EAE: Event Role F1 Score

## 输出结果

评估结果将保存在 `./output/<model_id>/` 目录下，包含以下信息：
- 各任务的评估分数
- 不同编程语言的性能对比
- 投票后的综合性能

## 注意事项

1. 确保有足够的 GPU 内存运行 vLLM
2. 评估前请确保数据格式正确
3. 建议使用 bfloat16 精度进行推理以节省显存

## 结果分析

可以使用 `Mean.ipynb` 进行结果分析和可视化，该文件提供了：
- 各任务的平均性能
- 不同 epoch 的性能对比
- 任务间的性能对比
