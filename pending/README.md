# 阶段 4 记录（2026-10-11 完成）

阶段 4 的 210 个候选全部处理完毕：每个候选都走了“填写 → 独立复核”流程。通过的条目已移入 `benchmarks/`；
决定不收录的 15 个连同理由记在 [docs/excluded.md](../docs/excluded.md)。本目录不再有待处理条目。

`tools/` 保留本次流水线，供以后新增候选时参考：

- `phase4_workflow.js`：Claude Code workflow 脚本，包含填写、复核、裁决三步的提示词
- `journal_to_yaml.py`：从 workflow 日志生成 YAML
- `leads/`：每个候选的线索（列表中的链接、阶段 1 的分类与核实证据）

后来的复核由 Codex 按 [AGENTS.md](../AGENTS.md) 的流程完成，每批一个提交（git log 中的 "Review batch N" 和 "Fill batch N"）。
