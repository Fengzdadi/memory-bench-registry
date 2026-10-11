# 待复核条目（阶段 4 第二批，更新于 2026-10-11）

这里的条目**还没有经过独立复核**，不在 `benchmarks/` 中，也不进入 README。复核通过后再移入 `benchmarks/`。

## 现状

阶段 4 候选共 210 个（见 [docs/coverage-gaps.md](../docs/coverage-gaps.md) 候选清单）：

- **第一批 P0 + P1（106 个）**：已完成“填写 → 独立复核 → 分歧裁决”。其中 101 个已入库；5 个经复核不是新 benchmark，没有入库，
  放在 `flagged/`：OmniMemEval、Agent Memory Leaderboard、MemoryData、Harness the Memory、Benchmarking and Rethinking Knowledge Editing。
- **第二批 P2（104 个）**：
  - 先前填写的 71 个已走完独立复核流程；通过的已移入 `benchmarks/`，未通过的留在 `flagged/`。
  - 2 个填写时被标记为可能不应单独入库，放在 `flagged/`：agent-memory-integrity-benchmark（已并入 RAMR 仓库，没有论文）、
    locomo-refined（LoCoMo 的修订再发布，技术报告尚未发布）。
  - 原先未填写的 31 个现已完成填写：25 个在本目录等待独立复核，6 个新增到 `flagged/` 等仓库所有者裁决。
- 复核中新增的 flagged（2026-10-11）：
  - bad-memory：论文描述的是安全评测框架，作者没有称其为 benchmark，也没有题目条目。
  - eccbench：核心任务是判断一个片段是否出现在单次输入的长流中，属于 docs/fields.md 排除的单次长输入测试（阶段 1 也标为 long_context_single_input）。
  - recon：论文 §3.1 规定系统只看到一次提供的 50K–100K token 案例文件并据此答题，属于 docs/fields.md 排除的单次长输入测试。
  - scale-qa：官方 benchmark_protocol.md 明确称为 Single-session Cross-domain Agentic Long-context Evaluation，运行时把条目和噪声打包成单个长线程，属于 docs/fields.md 排除的单次长输入测试。

本次填写新增的待裁决条目（不要直接入库）：

- `flagged/impact-is-not-invalidation.yaml`：输入是仓库断言与提交差异，判断断言是否失效；论文没有让编码 agent 在独立会话或任务间保留信息，不符合 `coding_cross_session` 的收录标准。
- `flagged/lsrep.yaml`：论文明确把 LSREP 定义为评测协议；实例化所用的四段私人对话及 219 个 probe 未公开，不构成可单独登记的公开 benchmark 数据集。
- `flagged/capmem.yaml`：每题只从一段预生成的长视频字幕作答，属于 `docs/fields.md` 排除的单次长输入测试。
- `flagged/simlife-bp.yaml`：已报告的任务把一整段超长模拟生活 episode 作为输入做离线规则问答，没有跨独立交互保存记忆。
- `flagged/what-should-an-agent-remember.yaml`：每个 episode 只有 10 条 slot-value 陈述和两次查询，主要检验保留/选择规则；不符合现有任一记忆类型的具体判定标准。
- `flagged/ember-bench.yaml`：模型从单段预录家庭任务视频做离线多选问答，没有环境中的动作评测，也没有跨独立交互的记忆保留。

## 下一步

1. 对本目录的 25 个新填条目在新的独立会话做复核；有分歧的字段再交给第三个 agent 裁决。
2. `flagged/` 条目的去留由仓库所有者决定。
3. 复核通过的移入 `benchmarks/`，运行 `python scripts/validate.py` 与 `python scripts/build_readme.py`。

`tools/` 里是本次使用的流水线：`phase4_workflow.js`（Claude Code workflow 脚本）、`journal_to_yaml.py`（从 workflow 日志生成 YAML），
以及 `leads/`（每个候选的线索：列表中的链接、阶段 1 的分类与核实证据）。
