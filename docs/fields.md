# 字段说明

每个 benchmark 一个文件 `benchmarks/<slug>.yaml`，结构由 [`schema/benchmark.schema.json`](../schema/benchmark.schema.json) 约束，
`scripts/validate.py` 另外检查下文列出的跨字段规则。

## 核心原则

- **所有字段都要有出处**：值必须能在论文或官方仓库 / 数据页里找到。每个非空字段都要在 `sources` 里写明出处
  （论文章节或表格、README 路径、dataset card），validate.py 会检查这一点。
- **找不到就填 `null`，不要猜。** 也可以在 `sources` 里说明为什么是 `null`（例如“论文只用 F1，没有 LLM judge”）。
- **可复现等级只填实际核对过的档位。** 没打开过仓库的一律 `unverified`。

## 字段

| 字段 | 含义 |
| --- | --- |
| `name` | 作者使用的 benchmark 名称 |
| `slug` | 文件名（不含 `.yaml`），小写字母、数字、连字符 |
| `release_date` | `YYYY-MM`，论文首次公开时间：有 arXiv 用 v1 日期，否则用会议/期刊发表时间 |
| `venue` | 发表会议/期刊及年份，如 `ACL 2024`；只有预印本则写 `arXiv preprint` |
| `memory_types` | 评测所针对的记忆类型（见下），至少一个 |
| `links.paper` / `links.code` / `links.data` | 论文、官方代码、官方数据。只收官方链接；找不到填 `null` |
| `scale.conversations` | 对话 / 交互历史 / episode 数量，按原文 |
| `scale.questions` | 评测题目 / probe / 任务数量，按原文 |
| `scale.avg_context_length` | 平均上下文长度，原文表述加单位，如 `~115k tokens`、`~600 turns` |
| `scale.notes` | 说明上面数字具体指什么（例如有多个版本或子集） |
| `metrics` | 原论文使用的评测指标 |
| `judge_model` | 原论文使用的 LLM judge；论文不用 LLM judge 则为 `null` |
| `repro_level` | 可复现等级（见下） |
| `repro_checked_at` | 核对 `repro_level` 的日期 `YYYY-MM-DD`；仅在 `unverified` 时为 `null` |
| `run_records` | 我们自己的运行记录，每条含 `date, model, sample_size, tokens, cost, notes`；当前阶段为空 |
| `notes` | 其他需要说明的事项 |
| `sources` | 字段路径 → 出处。键只能取 schema 中列出的字段路径 |

## 可复现等级 `repro_level`

从低到高。只填实际核对过的最高档位，并在 `sources.repro_level` 写明核对了什么。

| 等级 | 含义 | validate.py 额外要求 |
| --- | --- | --- |
| `unverified` | 还没有人打开论文和仓库核对 | `repro_checked_at` 为 `null` |
| `paper_only` | 核对过论文；找不到公开数据或代码 | 需要 `links.paper` |
| `data_public` | 数据可公开获取（打开过下载页/仓库，确认数据在），但没有官方评测脚本 | 需要 `links.data` 或 `links.code` |
| `official_script` | 官方仓库里有可直接对该 benchmark 跑评测的脚本 / 入口，且数据可获取 | 需要 `links.code` |
| `smoke_tested` | 我们用官方脚本在小样本上跑通过 | 需要 `links.code` 和至少一条 `run_records` |
| `full_run` | 我们跑过完整评测 | 需要 `links.code` 和至少一条 `run_records` |

当前阶段不运行任何 benchmark，所以最高只会到 `official_script`。

## 记忆类型 `memory_types`

一个 benchmark 可以有多个类型；只选评测**实际考察**的类型。

| 类型 | 判定标准 |
| --- | --- |
| `conversational_longterm` | 在长的多会话对话 / 聊天历史上做回忆或推理（如 LoCoMo、LongMemEval、MSC） |
| `personalization` | 利用用户特定的偏好 / 人设 / 画像信息来定制回答（如 PersonaMem、PrefEval） |
| `episodic` | 回忆带有时间、地点或顺序的具体事件与经历（“什么时候发生了什么”） |
| `semantic_knowledge_update` | 记忆存放在权重之外（上下文 / 外部存储）的事实知识，并在事实变化时正确更新、覆盖 |
| `procedural_workflow` | 记住“怎么做”：从早先任务中提炼技能、流程、工具用法或经验，并在之后**不同的**任务中复用；用任务流或留出任务上的表现变化来评测。仅从轨迹里回忆事实的问答属于 `episodic` |
| `coding_cross_session` | 面向软件工程 / 编码 agent，信息必须跨**独立的**会话或任务保留（仓库约定、先前修复、用户编码偏好等）。单会话长上下文的代码任务不算 |
| `parametric` | 记忆存放在**模型权重**中：评测知识编辑、通过微调或持续训练注入知识、test-time training、记忆化或遗忘，或在同一协议下比较参数化和非参数化记忆。只是用到预训练知识的普通知识问答不算 |
| `multi_agent_group` | 多个 agent 共享记忆，或多方 / 群组对话 |
| `multimodal` | 需要记住和回忆的内容包含非文本输入（图像、视频、音频），被测系统必须直接处理这些输入 |
| `embodied` | agent 在模拟或真实环境中行动（导航、操作等），记忆通过环境中的动作或任务成败来评测 |
| `memory_security` | 评测针对记忆的攻击或保护：记忆投毒 / 注入、隐私泄露、不应保留的信息被保留、删除或遗忘请求是否生效 |

后三个类型是阶段 1 核对后加入的，依据见 [coverage-gaps.md](coverage-gaps.md)。
只考察单次长输入的长上下文测试（如 RULER、NIAH、LongBench）不算记忆 benchmark，不为它们设类型，也不收录。
经过复核但决定不收录的候选及理由见 [excluded.md](excluded.md)。

`parametric` 的收录范围：只收明确把自己定位为评测“记忆”的知识编辑 / 遗忘 benchmark，
不追求覆盖整个知识编辑领域（阶段 1 找到 132 个相关 benchmark，按此标准收录 17 个；2026-10-11 由仓库所有者确认）。
