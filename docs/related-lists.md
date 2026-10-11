# 现有汇总列表及其核实状态

核对日期：2026-10-10。“最后更新”取默认分支最新一次提交（GitHub API `commits?per_page=1`）；网页取页面元数据。
“实际打开”指这次核对中取回了原文件全文并逐条解析，而不是只看过标题或摘要。

| 列表 | 链接 | 最后更新 | 实际打开 | 本次核对的范围 |
| --- | --- | --- | --- | --- |
| WEN6Lev57q4/awesome-agent-memory-benchmark | <https://github.com/WEN6Lev57q4/awesome-agent-memory-benchmark> | 2026-07-08（`5885019`） | 是：`README.md`、`README.zh-CN.md` | `## Benchmarks` 下全部 12 条 |
| zwq2018/awesome-agent-memory-benchmark（上面的 fork） | <https://github.com/zwq2018/awesome-agent-memory-benchmark> | `main` 与上游相同（`5885019`，ahead 0 / behind 0）；分支 `add/embodiedmemory-bench` 2026-09-29（`fdab623`） | 是：`main` 与 `add/embodiedmemory-bench` 两个分支的 `README.md` | 与上游的差异只有该分支新增的 1 条（EmbodiedMemory-Bench），尚未合入 `main` |
| TsinghuaC3I/Awesome-Memory-for-Agents | <https://github.com/TsinghuaC3I/Awesome-Memory-for-Agents> | 2026-09-28（`568b63a`） | 是：`README.md` | `### Benchmark` 表 18 条；另外扫描了全文其他小节中名称或标题含 bench/benchmark/dataset/evaluat 等词的条目（2 条） |
| TeleAI-UAGI/Awesome-Agent-Memory | <https://github.com/TeleAI-UAGI/Awesome-Agent-Memory> | 2026-10-09（`8cd94d3`） | 是：`README.md` | `## 📏 Benchmarks` 下三个小节（纯文本、多模态、动态环境）全部 49 条；另外扫描了其他小节中标题含 benchmark 等词的条目（6 条） |
| IAAR-Shanghai/Awesome-AI-Memory | <https://github.com/IAAR-Shanghai/Awesome-AI-Memory> | 2026-10-09（`5dc85bb`） | 是：`README_en.md`（1.43 MB）与 `README.md`（中文，1.35 MB） | `Resources / Benchmarks and Tasks` 表（44 个链接）+ 论文列表 `Datasets & Benchmark` 分组（178 条）；另外扫描了论文列表其他分组中标题或标签含 benchmark/dataset/evaluation 的条目（33 条） |
| topoteretes/awesome-ai-memory | <https://github.com/topoteretes/awesome-ai-memory> | 2026-08-24（`fa13101`） | 是：`README.md` | `## Benchmarks & evaluation` 表 3 条，另加正文顺带提到、没有链接的 2 个名称（ConvoMem、BEAM） |
| Cognee《AI Memory Benchmarks: The Complete Guide (2026)》 | <https://www.cognee.ai/ai-memory-benchmarks> | 发布 2026-09-01，`dateModified` 2026-09-03（页面 JSON-LD） | 是：取回整页 HTML 并转成文本 | 各个 benchmark 小节及 “More haystack variants”“Long-context suites”“Future directions” 中点名的全部 31 个 benchmark；“What is an AI benchmark” 一节里作为一般 AI benchmark 举例的 MMLU / GSM8K / SWE-bench 不计 |

## 收录规模（去重后）

去重规则：先按 arXiv ID，再按论文 URL，最后按简称合并；跨列表的重复只算一次。七个来源合计 379 条记录，去重后 279 条。
分类口径见 [coverage-gaps.md](coverage-gaps.md)。

| 来源 | 记录数 | 去重后 | memory benchmark | 通用 benchmark（被列为记忆评测资源） | 不是 benchmark |
| --- | ---: | ---: | ---: | ---: | ---: |
| WEN6Lev57q4 | 12 | 12 | 12 | 0 | 0 |
| zwq2018 fork（分支） | 1 | 1 | 1 | 0 | 0 |
| TsinghuaC3I | 20 | 20 | 16 | 2 | 2 |
| TeleAI-UAGI | 55 | 54 | 33 | 16 | 5 |
| IAAR-Shanghai | 255 | 223 | 136 | 28 | 59 |
| topoteretes | 5 | 5 | 5 | 0 | 0 |
| Cognee 指南 | 31 | 31 | 15 | 16 | 0 |

## 各列表的注意事项

- **WEN6Lev57q4** 的 12 条正是本库阶段 2 的 12 个样例。它的中英文 README 收录的条目相同。
- **zwq2018 fork** 的默认分支没有自己的提交；GitHub 显示的 `pushed_at`（2026-09-29）来自分支 `add/embodiedmemory-bench`。
- **IAAR-Shanghai** 的仓库首页 `README.md` 是中文版，`README_en.md` 是英文版（`README_cn.md` 只是一句跳转说明）。本次以英文版为准；
  两版的 arXiv 链接集合只差一篇（arXiv 2606.27499 只出现在英文版）。其 `Datasets & Benchmark` 分组里有相当一部分是方法、攻击或分析论文，
  不是 benchmark（59 条被判为“不是 benchmark”，多数来自这个分组）。该分组里有一条 OpenReview 链接（`forum?id=aLLuYpn83y`）
  与同一论文的 arXiv 条目（2406.09179）重复，且该 OpenReview ID 实际指向另一篇论文。
- **TeleAI-UAGI** 的条目格式不完全统一（有的标题没有链接、有的不加粗），解析时逐条核对过行号，49 条全部取到。
  它把 2023 年的视频生成 benchmark “StoryBench（NeurIPS 2023）”放在纯文本记忆 benchmark 下；它与 TsinghuaC3I / IAAR 收录的
  “StoryBench（arXiv 2506.13356，长期记忆）”是两个不同的工作，本库没有合并。
- **topoteretes** 列表的重点是记忆工具，benchmark 部分只有 3 条，另外顺带提到 ConvoMem、BEAM。
- **Cognee 指南** 是厂商博客，近一半篇幅讲通用的多跳问答和长上下文 benchmark（HotPotQA、RULER、NIAH 等），并不是专门为记忆设计的评测。
  它点名的 STATE-Bench、MemTrack、LongMemEval-V2 等不在任何一个 GitHub 列表里。

列表内容会持续变化；以上数字只对应表中记录的提交与日期。
