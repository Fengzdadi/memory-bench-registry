# 未收录的候选

这些候选经过“填写 → 复核”后，由仓库所有者决定不单独收录（2026-10-11）。如果再有人提议收录，先看这里的理由。
收录标准见 [fields.md](fields.md)。

## 单次长输入测试

`fields.md` 排除只考察单次长输入的测试：被测系统一次拿到全部材料，不需要跨交互保留记忆。

| 名称 | 论文 | 理由 |
| --- | --- | --- |
| ECCBench | [arXiv 2609.00103](https://arxiv.org/abs/2609.00103) | 判断一个短片段是否出现在单次输入的长流中；阶段 1 已标为 long_context_single_input |
| RECON | [arXiv 2607.16716](https://arxiv.org/abs/2607.16716) | 系统只看一次提供的 50K–100K token 案例文件并据此答题（§3.1） |
| SCALE-QA | [arXiv 2608.25655](https://arxiv.org/abs/2608.25655) | 官方协议自称 single-session 长上下文评测，把条目和噪声打包成单个长线程 |
| CapMem | [arXiv 2609.17688](https://arxiv.org/abs/2609.17688) | 每题只依据一段视频生成的字幕作答 |
| EMBER-Bench | [arXiv 2610.05013](https://arxiv.org/abs/2610.05013) | 每个任务给一段预录视频，离线做多选题；不在环境中行动，也不跨交互保留记忆 |
| SimLife-BP | [arXiv 2609.19610](https://arxiv.org/abs/2609.19610) | 一次提供一整段超长模拟生活 episode，离线做规律问答 |

## 不是新的 benchmark

| 名称 | 论文 / 仓库 | 理由 |
| --- | --- | --- |
| Bad Memory | [arXiv 2607.14611](https://arxiv.org/abs/2607.14611) | 安全评测框架加沙盒工作区；作者没有称其为 benchmark，也没有题目条目 |
| OmniMemEval | [MemTensor/OmniMemEval](https://github.com/MemTensor/OmniMemEval) | 评测工具，在已有 benchmark 上跑多个记忆后端；没有论文，也没有新数据 |
| Agent Memory Leaderboard | [AML-memory/agent-memory-leaderboard](https://github.com/AML-memory/agent-memory-leaderboard) | 提交制排行榜，使用 LoCoMo、LongMemEval 等已有数据；没有论文 |
| MemoryData | [arXiv 2606.24775](https://arxiv.org/abs/2606.24775) | 在已有 benchmark 上比较 12 个记忆系统的评测研究，没有新数据 |
| Harness the Memory | [arXiv 2608.15008](https://arxiv.org/abs/2608.15008) | 在已有 benchmark 上比较 11 种记忆载体的评测研究，没有新数据 |
| Benchmarking and Rethinking Knowledge Editing for LLMs | [arXiv 2505.18690](https://arxiv.org/abs/2505.18690) | 知识编辑的评测研究，数据来自 KnowEdit、ELKEN 等已有数据集 |

## 重复或修订版

| 名称 | 仓库 | 理由 |
| --- | --- | --- |
| Agent-Memory Integrity Benchmark | [DanceNitra/agent-memory-integrity](https://github.com/DanceNitra/agent-memory-integrity) | 没有论文；仓库已归档，并入 RAMR 仓库 |
| LoCoMo-Refined | [mem-eval-suite/LoCoMo_refined](https://github.com/mem-eval-suite/LoCoMo_refined) | LoCoMo 的修订再发布，沿用同样的 10 段对话；技术报告未发布。已在 [LoCoMo 条目](../benchmarks/locomo.yaml)的 notes 中提及 |

## 暂不收录：没有合适的记忆类型

| 名称 | 论文 | 理由 |
| --- | --- | --- |
| What Should an Agent Remember? | [arXiv 2610.00366](https://arxiv.org/abs/2610.00366) | 考的是在线流式记忆里该保留还是丢弃什么。它是记忆 benchmark，但 11 个 `memory_types` 都不合适。为单个条目新增类型不划算，等同类 benchmark 多了再考虑新增“记忆取舍”类型 |
