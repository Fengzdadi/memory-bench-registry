# 待复核条目（阶段 4 第二批，暂停于 2026-10-10）

这里的条目**还没有经过独立复核**，不在 `benchmarks/` 中，也不进入 README。复核通过后再移入 `benchmarks/`。

## 现状

阶段 4 候选共 210 个（见 [docs/coverage-gaps.md](../docs/coverage-gaps.md) 候选清单）：

- **第一批 P0 + P1（106 个）**：已完成“填写 → 独立复核 → 分歧裁决”。其中 101 个已入库；5 个经复核不是新 benchmark，没有入库，
  放在 `flagged/`：OmniMemEval、Agent Memory Leaderboard、MemoryData、Harness the Memory、Benchmarking and Rethinking Knowledge Editing。
- **第二批 P2（104 个）**，按计划暂停：
  - 71 个已由 agent 填写（打开过论文和仓库，每个字段写了 `sources`），但**尚未独立复核**，即本目录下的 `*.yaml`，均能通过 `validate.py`。
  - 2 个填写时被标记为可能不应单独入库，放在 `flagged/`：agent-memory-integrity-benchmark（已并入 RAMR 仓库，没有论文）、
    locomo-refined（LoCoMo 的修订再发布，技术报告尚未发布）。
- 复核中新增的 flagged（2026-10-11）：
  - bad-memory：论文描述的是安全评测框架，作者没有称其为 benchmark，也没有题目条目。
  - eccbench：核心任务是判断一个片段是否出现在单次输入的长流中，属于 docs/fields.md 排除的单次长输入测试（阶段 1 也标为 long_context_single_input）。
  - 31 个还没有填写：mobilemem statemembench utilmem apm-bench capmem cicm comembench cpb cue-mem dolphinbench icm-bench
    impact-is-not-invalidation lapse locomo-conv lsrep memcalib memoreason memprobe-2 memriskbench memtransfer pairpref pragma
    simlife-bp twist video2skill what-should-an-agent-remember cmsc-e dyadmem ember-bench knowing-the-store realcompanion

## 下一步

1. 对本目录的 71 个条目做独立复核；有分歧的字段再交给第三个 agent 裁决。
2. 对上面 31 个候选做“填写 → 复核”。
3. 复核通过的移入 `benchmarks/`，运行 `python scripts/validate.py` 与 `python scripts/build_readme.py`。

`tools/` 里是本次使用的流水线：`phase4_workflow.js`（Claude Code workflow 脚本）、`journal_to_yaml.py`（从 workflow 日志生成 YAML），
以及 `leads/`（每个候选的线索：列表中的链接、阶段 1 的分类与核实证据）。
