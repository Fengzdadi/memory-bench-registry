# 阶段 4 第二批复核记录（更新于 2026-10-11）

本批 25 个新填条目已独立复核；通过的条目已移入 `benchmarks/`。

## 现状

阶段 4 候选共 210 个（见 [docs/coverage-gaps.md](../docs/coverage-gaps.md) 候选清单）：

- **第一批 P0 + P1（106 个）**：已完成“填写 → 独立复核 → 分歧裁决”。其中 101 个已入库；5 个经复核不是新 benchmark，没有入库，
  放在 `flagged/`：OmniMemEval、Agent Memory Leaderboard、MemoryData、Harness the Memory、Benchmarking and Rethinking Knowledge Editing。
- **第二批 P2（104 个）**：
  - 先前填写的 71 个已走完独立复核流程；通过的已移入 `benchmarks/`，未通过的留在 `flagged/`。
  - 2 个填写时被标记为可能不应单独入库，放在 `flagged/`：agent-memory-integrity-benchmark（已并入 RAMR 仓库，没有论文）、
    locomo-refined（LoCoMo 的修订再发布，技术报告尚未发布）。
  - 原先未填写的 31 个现已完成填写并复核：25 个从本目录入库，6 个新增 flag 中 3 个维持、3 个取消并入库。
- 复核中新增的 flagged（2026-10-11）：
  - bad-memory：论文描述的是安全评测框架，作者没有称其为 benchmark，也没有题目条目。
  - eccbench：核心任务是判断一个片段是否出现在单次输入的长流中，属于 docs/fields.md 排除的单次长输入测试（阶段 1 也标为 long_context_single_input）。
  - recon：论文 §3.1 规定系统只看到一次提供的 50K–100K token 案例文件并据此答题，属于 docs/fields.md 排除的单次长输入测试。
  - scale-qa：官方 benchmark_protocol.md 明确称为 Single-session Cross-domain Agentic Long-context Evaluation，运行时把条目和噪声打包成单个长线程，属于 docs/fields.md 排除的单次长输入测试。

本次填写新增 flag 的复核结论：

- `benchmarks/impact-is-not-invalidation.yaml`：取消 flag。虽不符合 `coding_cross_session`，但它独立评测仓库事实变化后的记忆断言失效，归为 `semantic_knowledge_update`。
- `benchmarks/lsrep.yaml`：取消 flag。四段私人历史与 219 个 probe 构成已实例化的记忆评测；数据未公开影响 `repro_level`，不影响收录。
- `flagged/capmem.yaml`：每题只从一段预生成的长视频字幕作答，属于 `docs/fields.md` 排除的单次长输入测试。复核同意。
- `flagged/simlife-bp.yaml`：已报告的任务把一整段超长模拟生活 episode 作为输入做离线规则问答，没有跨独立交互保存记忆。复核同意。
- `flagged/what-should-an-agent-remember.yaml`：复核认为它是记忆 benchmark（300 个 episode 的在线流式保留，不是单次长输入），但现有 11 个 `memory_types` 都不合适：条目填的是 `semantic_knowledge_update`，自己的 notes 却写明没有事实更新。是否新增类型（如“保留/取舍”）或归入现有类型，由仓库所有者决定，暂不入库。
- `flagged/ember-bench.yaml`：模型从单段预录家庭任务视频做离线多选问答，没有环境中的动作评测，也没有跨独立交互的记忆保留。复核同意。

## 下一步

1. 对 `what-should-an-agent-remember` 的 `memory_types` 精确归类若有分歧，可另行裁决。
2. 其他 `flagged/` 历史条目的去留由仓库所有者决定。

`tools/` 里是本次使用的流水线：`phase4_workflow.js`（Claude Code workflow 脚本）、`journal_to_yaml.py`（从 workflow 日志生成 YAML），
以及 `leads/`（每个候选的线索：列表中的链接、阶段 1 的分类与核实证据）。
