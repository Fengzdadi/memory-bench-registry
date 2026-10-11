# 缺口核对：现有列表对三类记忆的覆盖

核对日期：2026-10-10。来源列表及其版本见 [related-lists.md](related-lists.md)，类型定义见 [fields.md](fields.md)。

## 结论

| 类型 | 现有列表是否覆盖 | 列表内经确认 | 各列表分布 | 列表外另有（经确认） |
| --- | --- | ---: | --- | ---: |
| `procedural_workflow` | **有，但不全** | 19 | IAAR 12 · TeleAI 6 · Cognee 3 · Tsinghua 2 · WEN6 0 · topoteretes 0 | 34 |
| `coding_cross_session` | **有，但很少** | 7 | TeleAI 4 · IAAR 3 · 其余 0 | 11 |
| `parametric` | **有，但只有一个列表** | 8 | IAAR 8 · 其余 0 | 18（抽样核实；另有 114 个未核实） |

（一个 benchmark 可能被多个列表收录，所以各列表分布之和可以大于列表内总数。）

- **`procedural_workflow`：有。** 证据：LifelongAgentBench 被 Tsinghua、TeleAI、IAAR 三个列表收录，论文 §3 写明它评测
  “leverage past experience to improve current task performance”，并在任务序列中回放先前轨迹；Evo-Memory（TeleAI、Cognee）把数据集
  改造成任务流，让早先任务的策略服务于后续任务；StuLife、StreamBench、MemoryBench 等同样经过两轮独立核实。
  但覆盖不全：SWE-Bench-CL、SkillCraft、EvoMemBench、AgentCL、ContinualSkillBench 等 34 个经确认的 benchmark 不在任何列表里，
  按经确认的总数算，列表只覆盖了约 36%（19 / 53）。WEN6 与 topoteretes 两个列表一个也没有。
- **`coding_cross_session`：有，但很少。** 有论文的只有 3 个，全部只在 IAAR：DreamBench-SWE（摘要：“multi-session benchmark …
  later software tasks depend on non-inferable evidence from earlier sessions”）、VibeMemBench、MetaKernelBench。另外 4 个只在 TeleAI，
  都是没有论文的 GitHub 评测框架或排行榜：agent-memory-bench、Agent Memory Benchmark（AMB 的 sde-bench 数据集）、
  Agent Memory Leaderboard 的 coding-memory 赛道、OmniMemEval 的 agent_memory 设置。MemoryCode、SWE-Bench-CL、SWE-ContextBench、
  ChainSWE 等 11 个经确认的 benchmark 不在任何列表里（检索还找到 sde-bench，但它是 TeleAI 所收 AMB 中的一个数据集，不算列表外）。
- **`parametric`：有，但只有 IAAR 一个列表收录，且偏向边缘。** IAAR 收录的 8 个中，5 个是把参数化记忆（微调 / LoRA）当作
  对比条件的记忆 benchmark（Episodic Memory Benchmark、LOCCO、MPR、MemOps、Harness the Memory），3 个是遗忘（unlearning）评测
  （OpenUnlearning、IDUnlearn-Bench、Cross-Lingual Unlearning Tensor）。参数化记忆的主流 benchmark，即知识编辑
  （MQuAKE、RippleEdits、KnowEdit、WikiBigEdit 等）、持续知识学习（TiC-LM、EvoWiki、WikiDYK）、遗忘（TOFU、MUSE、WMDP）等，
  不在任何列表里。TeleAI 虽然有 “Papers - Parametric Memory” 一节，但收录的都是方法论文，它的 Benchmarks 部分没有参数化记忆 benchmark。
  外部检索为这一类找到 132 个候选，这是一个独立的大领域；本次只抽样核实了 18 个（全部确认），其余 114 个列在下文，尚未逐条核实。

### 阶段 4 复核后的修正

阶段 4 逐条入库时，复核发现 5 个阶段 1 计入的条目不是新 benchmark：它们只是重跑已有 benchmark 的评测框架、排行榜或复评研究，
没有自己的新数据。这 5 个条目未入库，结论的方向不变：

- `coding_cross_session` 列表内：TeleAI 的 4 个中，Agent Memory Leaderboard（coding 赛道数据未公开）与 OmniMemEval（重跑
  EvoAgentBench 等已有 benchmark）不算，**有自己数据的只剩 5 个**（IAAR 3、TeleAI 2）。
- `procedural_workflow` 列表内：同样去掉上面两个，**19 → 17**。
- `parametric` 列表内：Harness the Memory 不算（在已有 benchmark 上比较记忆方式，代码未发布），**8 → 7**；
  列表外：“Benchmarking and Rethinking Knowledge Editing” 不算（没有发布新数据集），**18 → 17**。
- P1 候选 MemoryData 同理未入库。

## 方法

1. **收集。** 七个来源（六个列表加一个 fork 分支）用脚本逐条解析原文件，链接按原样保留，共 379 条记录；按 arXiv ID、论文 URL、
   简称三级去重后为 279 条。Cognee 页面按小节人工整理。去重复查又找到 1 组重复（IAAR 中同一篇 unlearning 论文以 arXiv 与
   OpenReview 两个链接出现），已合并。
2. **分类。** 279 条分 14 批，由 agent 结合 arXiv 摘要（必要时打开论文）判断：是否为记忆 benchmark、属于哪些记忆类型、
   是否属于三类缺口。结果：记忆 benchmark 164 个，被列为记忆评测资源的通用 benchmark 51 个，不是 benchmark 的 63 个。
3. **补漏。** 每个缺口类型另派一个扫描 agent 通读全部 279 条，宽松地找出可能属于该类型的条目，避免分类时漏判。
4. **列表外检索。** 每个缺口类型用两种方式检索文献：arXiv 和网络关键词检索；从已知 benchmark 出发沿引用、GitHub、Hugging Face 追溯。
   每个结果都用脚本与 279 条比对，判断是否已被列表收录。检索只做了一轮。仅这一轮就返回约 200 个不重复的候选（参数化一类 132 个），
   已足以回答“有没有缺口”。
5. **核实。** 分类、扫描、检索得到的每一条“X 属于该类型”的主张，都由两个独立 agent 分别核实：一个按定义逐字挑错，一个打开论文和
   仓库找原文证据。两者一致则采纳；不一致（16 次）由第三个 agent 重新阅读论文裁决。共核实 185 条主张：列表内的主张全部核实；
   列表外的程序性与编码类候选全部核实；列表外的参数化候选按“两种检索方式都找到”优先，抽样核实 18 个。

局限：分类与核实由 LLM agent 完成，每条都要求引用原文，但没有人工复核；列表外检索不保证穷尽。

## 记忆类型的调整

阶段 1 后在原有 8 个类型之外新增 3 个（定义见 [fields.md](fields.md)）：

- `multimodal`：约 30 个列表内的记忆 benchmark 以视频、图像或音频为记忆内容（如 TeleEgo、Persona-MME、VoxMem）。
- `embodied`：10 个记忆 benchmark 在模拟或真实环境中评测（如 RoboMemArena、RMBench、EmbodiedMemory-Bench）。
- `memory_security`：12 个记忆 benchmark 评测记忆投毒、隐私泄露或删除是否生效（如 MemSecBench、HUSH-Bench、MPBench）。

164 个记忆 benchmark 中只有 9 个无法归入原有 8 个类型，其中 7 个落在这三个新类型里。
只考察单次长输入的长上下文测试（RULER、NIAH、LongBench 等；分类时有 28 个条目带这个标签）不设类型；其中被判为通用 benchmark 的不作为候选。

## 三类缺口详情

### `procedural_workflow`

核实了 95 条主张：列表内确认 19 个，列表外确认 34 个，否定 42 个，未定 0 个。

**列表内、经确认属于该类型的 benchmark**

| Benchmark | 收录它的列表 | 证据（核实者引用） |
| --- | --- | --- |
| [Agent Memory Leaderboard (AML)](https://github.com/AML-memory/agent-memory-leaderboard) | TeleAI | Official AML HF leaderboard page: "Coding Memory ranks by Task Solve (%)"; README 'Coding memory capabilities': "Retrieves past diagnostic data, repair strategies, and validation workflows to accelerate the resolution of similar issues." |
| [AgenticSTS](https://arxiv.org/abs/2607.02255) | IAAR | Sec 4.2: "L5 skill library stores triggered strategic guides distilled from logs"; Sec 6.3: "Runs with postrun-active memory attempt A6–A8, while no-postrun streams stop at A2–A4" |
| [ConsolidationBench](https://arxiv.org/abs/2609.33013) | IAAR | Sec. 4.2: clusters include "recurring parametric sub-tasks (which warrant skills)"; axis "Reuse (transfer to novel composite tasks)"; Sec. 5.4: reuse "credits skill- and rule-artifact transfer". |
| [DreamBench-SWE](https://arxiv.org/abs/2608.20664) | IAAR | Table 21 construct taxonomy: "C8 Procedural / source-of-truth memory: Remember how this repository expects a change to be made, such as editing a generator rather than a generated artifact." Generated-files family: "S2 exposes source-of-truth plus regeneration |
| [EconSkills](https://arxiv.org/abs/2609.19523) | IAAR | Sec 3.3: 'Each of the 50 source skills is paired with two held-out task variants'. BASE vs MATCH1. Table 3: success 41.0% to 49.3%. Table 4: full-library RETR5/ALL50 on 360 tasks. |
| [Evo-Memory](https://arxiv.org/abs/2511.20857) | TeleAI, Cognee | Sec.3.1: restructures datasets "into streaming task sequences" so that "earlier tasks provide essential information or strategies for later ones"; ExpRAG/ReMem retrieve and write experience memory each step. |
| [EvoArena](https://arxiv.org/abs/2606.13681) | IAAR | App.F.1: "Earlier tasks in the same chain provide internal evidence for synthesizing reusable procedural memory"; Sec.5.2: "EvoMem improves Terminal-Bench-Evo by 2.4%, SWE-Chain-Evo by 0.5%". |
| [LifelongAgentBench](https://arxiv.org/abs/2505.11942) | Tsinghua, TeleAI, IAAR | Sec.3: "evaluates agents on their ability to leverage past experience to improve current task performance"; Sec.5.3: "enforces strict sequential execution to preserve the integrity of experience accumulation"; Tables 2-5 vary Exp=0..64. |
| [LongMemEval-V2](https://arxiv.org/abs/2605.12493) | Cognee | Sec.3.1: "Workflow Knowledge. An experienced colleague knows the steps needed to perform common tasks in the customized environment." This is one of five scored question abilities. |
| [MemoryBench](https://arxiv.org/abs/2510.17281) | TeleAI, IAAR | Sec.2.1: "procedural memory focuses on non-factual knowledge related to the execution of tasks"; Sec.3.2: train/test split "with ratio 4:1"; A.3.3: "training dialogues are first loaded into the memory". |
| [MetaKernelBench](https://arxiv.org/abs/2610.05014) | IAAR | Abstract: "instructed to distill what it learns into a natural-language skill ... The skill is the only extra input to a skill-conditioned attempt"; Sec 3.3 Eq.3 paired lift/help/harm rates |
| [MLE-InsightBench](https://arxiv.org/abs/2610.04927) | IAAR | §3 (held-out split): "an agentic MLE system facing a new task can draw on prior experience, but not on experience derived from the new task itself"; insights injected "as on-demand skills" (Abstract). |
| [OmniMemEval](https://github.com/MemTensor/OmniMemEval) | TeleAI | docs/agent_memory/README.md: "Run train split ... Back up domain memory. Restore the domain backup before every test run. Run test split" |
| [SEAGym](https://arxiv.org/abs/2606.17546) | TeleAI | Sec.3.3: "Train batches produce update evidence, while validation and test views are reserved for frozen assessment"; App.C.1: "ACE mainly stores process-level skills, TF-GRPO stores task-family experiences". |
| [SLVMBench](https://arxiv.org/abs/2607.11312) | IAAR | Sec 3.4: "SLVMBench evaluates true knowledge transfer instead of simple visual pattern matching"; Sec 4.1: "apply learned procedural knowledge"; Table 2 Procedural Mastery: Next Step Prediction, Step Ordering, Tool Configuration |
| [STATE-Bench](https://github.com/microsoft/STATE-Bench) | Cognee | docs/AGENT_LEARNING_TRACK.md: "100 task trajectories per domain ... 50 held-out test tasks per domain ... The score asks whether learnings extracted from past trajectories improve agent performance." |
| [StreamBench](https://arxiv.org/abs/2406.08747) | IAAR | Sec.1: "with the goal to maximize the accuracy for the whole sequence of the agent's predictions"; Sec.3.1: "evaluate an agent by its aggregate metric at the final time step (T)"; Sec.4.1.2 MemPrompt/Self-StreamICL keep past feedback in external memory. |
| [StuLife](https://arxiv.org/abs/2508.19005) | Tsinghua | Sec.4.3: "agents must abstract experiences into reusable skills and transfer them across evolving challenges"; Sec.5.2: AWM gives "a robust improvement, lifting StuGPA to 17.81 and Total Success to 10.12%". |
| [VibeMemBench](https://arxiv.org/abs/2609.23570) | IAAR | Sec 3.2: history 'admits only earlier instances from the same repository'. 'Each experience records a bug class, root cause, fix pattern, and reusable lesson.' Tables 1–2 score Resolved vs memory-off. |

**列表外、经确认属于该类型的 benchmark（六个来源都没有收录）**

| Benchmark | 证据（核实者引用） |
| --- | --- |
| [AFTER](https://arxiv.org/abs/2606.23127) | Abstract: 'controlled evaluation settings for local improvement, cross-task transfer, cross-role transfer' (plus cross-model). Sec 3.2: Evolution 'Collect–Diagnose–Revise–Promote cycle'. App. D.1: the test split checks 'genuine generalization'. |
| [AgentCL](https://arxiv.org/abs/2606.02461) | Sec 3.3 Metrics: "Plasticity Gain (PG) measures whether experience accumulated from preceding tasks helps the agent solve the current task." Generalization Gain uses held-out independent tasks with frozen memory. |
| [AgentStream](https://arxiv.org/abs/2608.00155) | Sec. 3: "an agent processes a stream of tasks and, after each attempt, distills the interaction trajectory into persistent experience (e.g., refined context, memory entries, reusable skills". Eq. 1 defines the evolution gain. |
| [AhaBench](https://arxiv.org/abs/2609.05435) | Sec 3.1: "The learning opportunity is the questioning strategy demonstrated by a solved episode"; Sec 4 'Procedure gap' quantifies "dependence on procedural teaching"; endpoint gain compares post-curriculum vs cold on same targets. |
| [BELA](https://arxiv.org/abs/2511.22130) | Intro: agents should "refine their strategy from inferring the shared uncertainty structure in observed tasks"; Sec 4.1 tracks regret across episodes and reports "no models exhibit episode-over-episode improvements" |
| [BenchTrace](https://arxiv.org/abs/2605.29225) | Sec 3.3.2: "agents evolve through evolution snapshots and are evaluated on a test snapshot"; Type 3: "s0 is from a different subtask of the same task" |
| [CL-Bench (Continual Learning Bench)](https://arxiv.org/abs/2606.05661) | Sec 3.1: "a system that identifies recurring patterns can exploit them in future instances"; Sec 4.2: gain = stateful reward minus the same system's stateless reward per instance. |
| [ContinualSkillBench](https://arxiv.org/abs/2608.03874) | Sec 3: "After completing each subtask, the agent receives feedback and may create or modify skills ... the updated repository is then available for subsequent tasks." Sequential compared against Independent baselines. |
| [EngramBench](https://arxiv.org/abs/2609.39284) | Sec 4.3: "Phase 1: Skill Generation & Freezing. During the learning phase, the harness distills historical trajectories into a reusable Skill Bank"; Phase 2 runs 13 transfer tasks with the frozen bank. |
| [EvaLearn](https://arxiv.org/abs/2506.02672) | Repo README Overview: 'EvaLearn requires models to solve problems sequentially, allowing them to leverage experience from previous solutions.' Paper compares feedback/demonstration learning with a zero-shot baseline. |
| [EvoAgentBench](https://arxiv.org/abs/2607.05202) | Sec 3: "An Ability is ... a reusable operation such as a search strategy, debugging procedure, or validation workflow"; primary metric is average transfer gain on test tasks vs no-evolution baseline. |
| [EvoHarnessBench](https://arxiv.org/abs/2609.04280) | Sec. 3.4 (self-evolving adaptation evaluation): "measures whether experience accumulated under earlier harnesses continues to support effective adaptation as new capabilities are introduced". Evaluation uses a held-out split. |
| [EvoMemBench](https://arxiv.org/abs/2605.18421) | Sec 4.4: "Cross-episode execution evolution evaluates whether an agent can learn reusable execution experience from previous episodes and apply it to future tasks." Sec 5.1: memory updated after each episode and reused. |
| [EvoPathBench](https://arxiv.org/abs/2609.24663) | Sec 1: "At fixed checkpoints, it freezes these artifacts and reevaluates the same target capability on held-out episodes excluded from subsequent updates." Artifacts are memories, skills or workflows. |
| [FinEvo-Bench](https://arxiv.org/abs/2608.06144) | Sec 3.1: "Each scene contains six substantively distinct cases governed by the same professional procedure. The shared procedure creates a basis for transferring experience"; paired state-reset controls (abstract). |
| [FinEvolveBench](https://arxiv.org/abs/2606.06960) | Sec 3.2: "The agent then uses this feedback to update or generate experience, which becomes available for subsequent tasks." App A.5: "Every experience store is empty before the first evaluation date." |
| [GDPevo](https://arxiv.org/abs/2608.03764) | Abstract/Sec 1: rule hybridization "distributes subsets of these rules across training tasks, and recombines them in held-out test tasks, so that test-time gains are attributable"; skill-based evolution vs no-evolution base. |
| [Learn2Play Bench](https://arxiv.org/abs/2610.08215) | Sec 4.1 Metrics: "Learning Gain (LG) and Learning Slope (LS) measure improvement across episodes"; RQ4: re-shuffled games change "the visible instance but preserves the underlying rule". |
| [MedEvoEval](https://arxiv.org/abs/2606.28900) | Sec 3.4: manager writes "IF ... THEN" / "IF ... AVOID" cards to memory banks; Table 3: held-out transfer H0→H3 total 0.338→0.413; maturation E0 0.246→E3 0.430 |
| [OmniGameArena](https://arxiv.org/abs/2606.09826) | Abstract: IDC exposes "how the score evolves across reflection rounds, and how the learned skill behaves on held-out task variants". Sec. 5.3.2 and Table 5 report gains on held-out variants. |
| [PAST-Bench](https://arxiv.org/abs/2608.04003) | Sec 1/3.1: four capabilities incl. "procedural reuse (8/64)"; task families share "a reusable artifact (procedural reuse)"; later episodes test reuse vs matched no-persistence controls. |
| [PATH-Bench](https://arxiv.org/abs/2608.01149) | Sec 3.3: "Only the intervening tasks update the agent's external learning state; repeated occurrences of [the probe] serve exclusively as evaluation probes." FWT/BWT/FGT are read from the probe trajectory. |
| [S3Gym](https://arxiv.org/abs/2608.31100) | Sec. 4.4: "Exploration provides diverse experience for judgment and consolidation, whereas evaluation verifies whether the resulting improvement transfers to stricter conditions". The phases use disjoint seeds. |
| [SEA-Eval](https://arxiv.org/abs/2604.08988) | Paper: 92 sequences (correlated/orthogonal/implicit-intent) of length 5 from 32 atomic tasks; agents keep procedural/episodic/declarative memory; metrics SR, token cost, Keff(Evo), Keff(Stab), Keff(Ret). |
| [SeqMem-Eval](https://arxiv.org/abs/2605.15384) | Sec. 3.3: "we measure hold-out generalization on a fixed set of unseen tasks under different memory states". Sec. 3.1 says the memory holds workflows and reflections. Table 6 fixes the sequential and hold-out splits. |
| [ServeLearnBench](https://arxiv.org/abs/2610.07792) | Sec 3.1 (arXiv HTML): "Serving and test tasks cover the same behavioral components ... using disjoint task instances"; tests "transfer to new instances under the same active policy rather than memorization"; harnesses include SkillOpt, Continual Harness, Prime |
| [SkillCraft](https://arxiv.org/abs/2603.00718) | Sec 5.2: 'We implement Cross-Task Mode using a two-phase static transfer approach' (Easy→Hard, Hard→Easy, Hard→Hard). Table 3: 'Base: No skill library. Skill: With skill library.' |
| [SkillEvolBench](https://arxiv.org/abs/2605.24117) | Paper protocol: 'Each environment in SkillEvolBench is evaluated as an independent lifelong episode'. Library frozen after acquisition. ESR = 'frozen deployment success on held-out context-shift, adversarial, and composition tasks'. |
| [SkillFlow](https://arxiv.org/abs/2604.17308) | Sec 1/2.4: agents "begin without skills, evolve an external skill library through trajectory- and rubric-driven skill patches, and ... are evaluated under a fixed task order within each family". |
| [SkillLearnBench](https://arxiv.org/abs/2604.20087) | Sec 3.1: "the skill is generated once per task and then tested on all instances"; Sec 5.2 compares seed-instance vs held-out-instance accuracy; Level 3 compares against no-skill baseline. |
| [SWE-Bench-CL](https://arxiv.org/abs/2507.00014) | Paper: memory stores 'summaries of problem, solution, rationale; tool usage; success status'. Metrics include forward/backward transfer and forgetting, comparing memory-enabled vs memory-disabled. Full agentic results are 'ongoing'. |
| [SWE-ContextBench](https://arxiv.org/abs/2602.08316) | Sec. 2.2.5: "1,100 experience tasks, whose solution trajectories form a reusable context pool, and 376 related tasks". Tables 3-4 compare No-Context against Free/Oracle Context and Summary Learning, plus Mem0, LangMem and others. |
| [The Agent's First Day (EvoEnv)](https://arxiv.org/abs/2601.08173) | Sec 3.3: "While the sequence, quantity, and types of tasks remain invariant across both days, the specific input parameters for task instantiation vary"; insights "guide task execution on Day 2" (Table 6) |
| [Trust-Memevo](https://arxiv.org/abs/2602.03224) | Sec. 5.1: "After each evolution stage, we freeze the evolved memory bank and conduct static evaluation on the corresponding trustworthiness set, without adding or updating any memory." |

<details><summary>被否定的主张</summary>

| 条目 | 来源 | 否定理由（核实者引用） |
| --- | --- | --- |
| After the Fix | IAAR | Paper contributions: "Our empirical contribution evaluates accepted experience as a memory update, against both its predecessor and independence." Pairs are built from the existing ThinkingBox and APEX-Agents benchmarks, and no benchmark release is stated. |
| agent-memory-bench | TeleAI | README 'Task suite': '30 ts-* tasks \| retrieve a governing fact from prior sessions'; 'Scope and limits': 'Most tasks state one governing fact in one document.' |
| AMA-Bench | IAAR | Sec. 6.1: each trajectory is ingested once and each QA pair is answered independently; Limitations: the work focuses on "in-episode memory" and leaves cross-task lifelong learning to future work. |
| AndroidIntent (PersonalAlign) | IAAR | Sec. 3: "latent routines, requiring agents to incorporate current user state to provide proactive suggestions"; Appendix D defines Routine Intent as a recurring user intent inferred from time and scenario. |
| AppWorld | TeleAI | Abstract: 'a suite of 750 natural, diverse, and challenging autonomous agent tasks ... robust programmatic evaluation with state-based unit tests'. |
| CL-bench | TeleAI | Sec. 3.2 has a 'Procedural Task Execution' category, but the procedures are supplied in the given context; Sec. 6.3 says evaluation covers only 'single-turn tasks and short sequences of tasks'. |
| CoMemBench | IAAR | Appendix E: "Each external store is empty at workflow start; only the memory policy changes across rows." |
| DolphinBench | IAAR | Sec. 3.1 Test Construction: each selected history fact (decisions, preferences, project developments) must affect the work; Limitations: longer multi-step workflows are not tested. |
| DyadMem | IAAR | Sec. 2 says experience-based agent memory such as AWM and Memp extracts workflows that 'transfer across tasks', then 'DyadMem differs by representing both the user and how a p[articular agent works with them]'. Sec. 4.5 scores agent_method only by Capture F1. |
| Ego2World | IAAR | Sec. 6.4: "persistent belief resets once per episode, whereas the comparison resets belief at each group"; "the controller can reuse retained locations when deciding whether to query again." |
| Evaluating Long-Term Memory for Long-Context QA | TeleAI | Sec. 3.1/3.2: uses LoCoMo with QMSum validation, and 'We use the optimized prompt for the next sets of questions'. The metric is answer F1, and no new benchmark is introduced. |
| FAME | IAAR | Sec. 5.1: "Our main evaluation is AUROC, representing the effectiveness of identifying false memory, which is computed between predicted labels and false memory ground truths." |
| Harness the Memory | IAAR | Intro contributions: "The first holistic harness evaluation of agent memory"; "A controlled evaluation isolating the memory substrate across 11 methods". Abstract: "Code will be made available upon acceptance." |
| ImplicitMemBench | 列表外 | Sec 3.2.1 Learning-Interference-Test: "minimal specification (rule + 1-3 examples), extensive interference (15 misleading turns), then novel test probes requiring first-attempt success." |
| J-TTL (Jericho Test-Time Learning, from EvoTest) | 列表外 | Sec 3: "After each episode concludes, the game environment is reset to its identical initial state". App. limitations: "The J-TTL benchmark and our method are designed for rapid improvement on a single task." |
| LegalWorld / LongJud-Bench | IAAR | Sec. 4.4: LongJud-Bench "scores the target lawyer agent... through eight legal capabilities". Sec. 3.2: Skills are pre-authored manuals that "specify steps, constraints, and outputs". |
| LifeBench | IAAR | Sec. 3.2.5: ND category 'Evaluates system understanding of user habits, skills, emotion and preferences' (e.g. the user's gym routine). It is scored by accuracy with an LLM judge using the LoCoMo prompt. |
| Mem2ActBench | WEN6, IAAR, Cognee | Sec. 3.3: memory consists of facts extracted as (attribute, fact, source ID) triples merged into a 'memory evolution chain' (e.g., dietary preferences, travel plans); scored by Tool Accuracy / parameter F1 (Sec. 4.1). |
| MEMENTO | IAAR | Sec. 3.2: memory categories are object semantics and user patterns (routines, arrangement preferences); Sec. 4.1: the LLM "selects appropriate skills from a predefined skill library". |
| MemGUI-Bench | 列表外 | App. A.5.2: "long-term memory evaluation through the pass@k protocol, where agents are allowed up to attempts per task". A.4.5 says mirror pairs mean agents "can potentially transfer knowledge"; no metric isolates this. |
| MemoryAgentBench | WEN6, Tsinghua, TeleAI, IAAR, Cognee | Sec. 3.1 TTL datasets: agent must 'map sentences to class labels, leveraging previously seen labeled examples in context' (BANKING77, CLINC150, TREC, NLU) plus movie recommendation from dialogue history. |
| MemoryArena | IAAR, Cognee | Paper §3.1 (Bundled Web Shopping): "Later purchases depend on recalling attributes of earlier items to ensure compatibility and preference consistency." Formal reasoning requires "reuse of previously established conclusions." |
| MemoryData | TeleAI, IAAR | Sec. 4.1: DB-Bench tests whether 'memory supports procedural execution across database operations' (EM / Task Success Rate). Neither the paper nor the repo says experience accumulates across tasks, and the paper claims no new benchmark. |
| MemTrack | Cognee | Sec. 4.2: "Correctness: For each of the questions, our benchmark provides a set of respective expected answers... Using a LLM-judge (gpt-4o), we output a Correctness score". |
| MemTransfer | IAAR | Sec. III-B: "The four demonstrations are used to construct memory"; the test is the same task case from a different start or with a blocked route. Memory is framed as spatial/episodic, and 'procedural' never describes it. |
| MemTrapBench | IAAR | Sec. 2.2: "MemTrapBench serves as a diagnostic stress test of harmful memory influence rather than a general evaluation of memory utility." |
| MERIT | IAAR | Sec. 3.3 domains store only facts, e.g. "Facts: diagnosed config fixes, safe rollback versions"; probe episodes require a remembered fact absent from the episode's inputs. |
| Mining Agent Skills from Production Traces | IAAR | Listed contributions are only: "Controlled comparisons of skill form and mining evidence", "Quantifying the effect of outcome-label access", "Characterizing task-dependent gains and regressions". It evaluates on existing ThinkingBox-Bench and APEX-Agents. |
| MIRIX | IAAR | Abstract/experiments: evaluated only on ScreenshotVQA (overall accuracy and storage) and LOCOMO (single-hop, multi-hop, open-domain, temporal); no experiment or ablation isolates the Procedural memory component. |
| Momento | IAAR | Sec. 2.3: tasks include "evolving preferences, implicit references, contradictory updates, and temporally distributed information"; there is no procedural or workflow-reuse category. |
| OdysseyBench | TeleAI | Sec. 3: each task requires the agent to "extract essential information from long-horizon dialogue histories between the user and agent"; metric is the pass rate (Evaluation Metrics). Nothing tests procedures reused across tasks. |
| PM-Bench | IAAR | Abstract: evaluates how agents "maintain user intentions, execute delayed intentions, and monitor latent environment changes". Sec. on metrics: "The primary metric is set-level F1" over prospective action selections. |
| Proced_mem_bench (Procedural Memory Retrieval Benchmark) | 列表外 | arXiv HTML abstract: benchmark 'isolates procedural memory retrieval from task execution'; README: scored with 'Standard IR metrics (P@k, R@k, F1@k, NDCG@k, MAP)' against an LLM judge. No downstream task-success experiment. |
| ReMe | IAAR | Sec. 1 claims a framework and 'release reme.library, a fine-grained procedural memory dataset'. That is a memory resource. Evaluation uses the existing BFCL-V3 (50/150 split) and AppWorld (90 train / 168 test-normal). |
| ReplayLens | IAAR | Abstract: 'a black-box audit that changes one relationship in the stored history at a time'. Sec. 3.1: memory holds (task, action, outcome) records, and queries come from the same task families. |
| SCLATE | IAAR | Paper: SCLATE is "an open execution substrate where arbitrary continual-learning agents can be evaluated and trained"; held-out MetaClaw gains come from post-training Qwen3.5-4B. |
| Sequential EQA | IAAR | Sec. 1: "Agents that retain only traversability information... remember where the robot has explored but not the visual-semantic evidence needed for later questions". What is reused is scene memory, not procedures. |
| SimLife-BP | IAAR | Abstract/Task Design: SimLife-BP tests whether a model can infer hidden behavioral rules from weeks of observations; scored by All-Correct Rate and accuracy on binary multiple-choice questions. |
| StreamMemBench | TeleAI, IAAR | Sec. 3.2: FUR passes only if the follow-up response 'uses the anchor evidence appropriately'. Correction feedback 'supplies the missing or corrected evidence', so the reused experience is facts, not procedures. |
| Video2Skill | IAAR | Limitations: "Our skill schemas describe observed physical transformations; their utility for downstream planning and executable control requires further evaluation." |
| WebArena | IAAR | Abstract: 'we release a set of benchmark tasks focusing on evaluating the functional correctness of task completions'; reports end-to-end task success rate (14.41% best agent). |
| WebShop | IAAR | Abstract: 'Given a text instruction specifying a product requirement, an agent needs to navigate multiple types of webpages ... to find, customize, and purchase an item.' |

</details>

### `coding_cross_session`

核实了 41 条主张：列表内确认 7 个，列表外确认 12 个（其中 sde-bench 实为列表内 AMB 的一个数据集，故真正列表外为 11 个），否定 22 个，未定 0 个。

**列表内、经确认属于该类型的 benchmark**

| Benchmark | 收录它的列表 | 证据（核实者引用） |
| --- | --- | --- |
| [Agent Memory Leaderboard (AML)](https://github.com/AML-memory/agent-memory-leaderboard) | TeleAI | README.md 'Evaluation at a glance' table, Coding Memory row: 'Whether an agent can retrieve, filter, and reuse relevant engineering experience from earlier work in the same repository' (12 repos, 1,290 historical tasks). |
| [agent-memory-bench](https://github.com/GiulioDER/agent-memory-bench) | TeleAI | README: "evaluates Claude Code on real repository tasks whose solutions depend on information from earlier sessions"; tasks "retrieve a governing fact from prior sessions" (README, Task suite). |
| [AMB (Agent Memory Benchmark)](https://github.com/vectorize-io/agent-memory-benchmark) | TeleAI | src/memory_bench/dataset/sdebench.py: "the decision — a past developer chat or a documented git commit"; sde-bench README: decision "made in a past developer chat and never written into the repo". |
| [DreamBench-SWE](https://arxiv.org/abs/2608.20664) | IAAR | Abstract: "multi-session benchmark for software-agent memory hygiene in which later software tasks depend on non-inferable evidence from earlier sessions". Sec. 5.1: S3 info "recoverable only from earlier-session memory". |
| [MetaKernelBench](https://arxiv.org/abs/2610.05014) | IAAR | Abstract: agents "retain what they learn in knowledge bases or as distilled skills"; benchmarks "leave the reuse value of retained experience unmeasured." §2.2: "fresh execution"; skill is "the only additional task input". |
| [OmniMemEval](https://github.com/MemTensor/OmniMemEval) | TeleAI | docs/agent_memory/README.md, memory_train_backup_test: 'Clear memory. Run train split... Back up domain memory. Restore the domain backup before every test run. Run test split'. The software_engineering domain is SWE-Bench, 101 train / 26 test. |
| [VibeMemBench](https://arxiv.org/abs/2609.23570) | IAAR | Sec. 3.2: screen "admits only earlier instances from the same repository and excludes every target identifier". Sec. 3.5: memory systems "ingest the full eligible prior-work history available to a target". |

**列表外、经确认属于该类型的 benchmark（六个来源都没有收录）**

| Benchmark | 证据（核实者引用） |
| --- | --- |
| [AgentCL (coding streams)](https://arxiv.org/abs/2606.02461) | Sec. 4.1: "Each task pair, from subtask to complex task, is guaranteed to exhibit a function reuse relation"; Sec. 3.3: "The second pass is read-only with frozen memory." |
| [CAPA](https://arxiv.org/abs/2607.26611) | Benchmark Task section: 'CAPA evaluates whether a coding assistant can use a recurring user's prior multi-turn coding sessions'. Main Results: same-user history improves ES for 11 of 12 models. |
| [ChainSWE](https://arxiv.org/abs/2607.02606) | Sec. 4.3, Seq+Mem mode: 'The agent enters bug k+1 with the transcript from bug k, including intermediate observations and dead ends.' The HF card describes 100 time-ordered chains (304 bug-fix tasks). |
| [Continual Learning Bench (CL-Bench, software-engineering domain)](https://arxiv.org/abs/2606.05661) | App. A.2 (Codebase Adaptation): "Each issue is presented in a fresh Docker container at the issue's base commit"; an agent that records repo knowledge means "its stateful version outperforms the stateless one". |
| [EngramBench](https://arxiv.org/abs/2609.39284) | Sec. 4.3 Phase 2: agent gets "the current task's README, a clean workspace scaffold, and the frozen Skill Bank"; it is "restricted from ... accessing the raw workspaces, interaction histories, or codebases from the learning phase." |
| [EvoAgentBench (software-engineering domain)](https://arxiv.org/abs/2607.05202) | Sec. 3.2.5: "every test task must share at least one edge-eligible Ability with a training task in its own community"; Sec. 4.1: SWE-Bench Verified "uses hidden repository test suites and resolve rate". |
| [Insecure Coding Preferences in Long-Term Memory (dataset)](https://arxiv.org/abs/2607.17619) | Sec. 5.3: "we construct a corresponding long-term memory entry in the target LLM system for each code prompt"; Sec. 1: "three independent code-generation runs in separate sessions". |
| [MemoryCode](https://arxiv.org/abs/2502.13791) | Title: 'Evaluating LLMs in Multi-Session Coding Interactions'. Sec. 4: the HISTORY setting 'evaluates the ability to recall information from previous sessions'. Sec. 1: instructions can be 'updated multiple times throughout the dialogue history'. |
| [sde-bench (Vectorize)](https://hindsight.vectorize.io/blog/2026/08/06/hindsight-0-9-0) | sde-bench README: "The only way to get it right first-try is to know the decision: from the project's git history, or from a past developer conversation." Sources: 28 history / 27 conversation / 6 amended. |
| [Stateful SWE-bench (from TOM-SWE)](https://arxiv.org/abs/2510.21903) | Sec. 4: "agents have access to previous conversation histories with the same user profile, requiring them to derive user preferences from past interactions"; "we randomly sample 20 sessions from the same developer". |
| [SWE-Bench-CL](https://arxiv.org/abs/2507.00014) | Sec. 3.2: '8 sequences from distinct repositories, totaling 273 tasks'. Sec. 6.3: per-task summaries are stored in FAISS and retrieved for later tasks, prioritizing 'experiences from the same task sequence'. |
| [SWE-ContextBench](https://arxiv.org/abs/2602.08316) | Sec. 1: 'The benchmark enables direct evaluation of how effectively agents can learn from previous context when solving new tasks.' Sec. 3.1: related tasks run 'in a fresh environment'. |

<details><summary>被否定的主张</summary>

| 条目 | 来源 | 否定理由（核实者引用） |
| --- | --- | --- |
| Agent Memory Techniques | Tsinghua | README: "30 runnable Jupyter notebooks covering every major memory pattern". The coding-agent 'before/after' card is a course promo (5 questions per repo after a docs layer), not a benchmark protocol. |
| AMA-Bench | IAAR | Sec 6.1: 'For each trajectory, the memory system first ingests the full trajectory once to construct its memory state.' Sec 7: 'A limitation of this study is its focus on in-episode memory.' |
| AppWorld | TeleAI | README: 'for task_id in load_task_ids("test_challenge"): with AppWorld(task_id=task_id, ...)'. Each task runs in its own world instance and is evaluated independently, with no cross-session memory. |
| Bad Memory | IAAR | Workspace "represents the working directory of 'Jordan Kim', a software engineer"; metrics are attack success rate and persistence rate of planted payloads (arXiv HTML 2607.14611, Sec. 3.2-3.3). |
| CoMemBench | IAAR | arXiv HTML Appendix F: "Each external store is empty at workflow start; only the memory policy changes across rows." Code tasks use issue-specific Docker environments. |
| DolphinBench | IAAR | Sec 3.1: personas are a startup CEO, 'Alex, an infrastructure engineer who handles deploys, incidents, on-call rotations, and runbooks', and a product manager. No tasks are shown to involve coding or repo editing. |
| EvoArena | IAAR | Sec. 3.2: "the benchmark tests whether agents can solve each localized requirement under the current accumulated codebase; memory-based agents may additionally use prior interaction context" |
| FAME | IAAR | Abstract (arXiv:2609.39473): FAME is a training-free framework detecting false memory via hidden-state 'concept drift' under counterfactuals. GitChameleon is used only as a code-generation testbed, with no persistence across coding sessions. |
| Impact Is Not Invalidation (claim-invalidation benchmark) | IAAR | arXiv HTML: the model receives a claim (a test function) and a diff, then answers {"verdict": "held"\|"flipped"}. Also: "No memory system was modified to use any of these arms." |
| LifelongAgentBench | Tsinghua, TeleAI, IAAR | Paper names environments only as 'Database, Operating System, and Knowledge Graph' and uses 'LLM agents'/'interactive environments'. There is no software-engineering, repository or coding-agent framing (Sec 3, 4.2, App. A). |
| LoCoBench | 列表外 | locobench/evaluation/evaluator.py, _generate_solution: "# Multi-session development scenario - combine all sessions". The session prompts are joined into one solution_prompt that ends "Generate your response now:". Paper §3.3 claims cross-session scope for onl |
| LoCoBench-Agent | Tsinghua | arXiv HTML Sec 3.1: "Multi-Session Memory Retention. Evaluates context retention across conversation turns through reference consistency." Sec 4.2: each session has at most 50 turns per scenario. |
| Measure Before You Manage | IAAR | Title/abstract: 'Evaluating Agent Working Memory in Coding Agents' over '55 archived coding-agent trajectories', comparing compression and retrieval policies. This is within-run context management, not persistence across sessions. |
| MemTrack | Cognee | arXiv HTML: questions "are introduced strictly sequentially to remove the possibility of preemptive solution planning" within one instance. Memory (none, Mem0 or Zep) operates within a single episode. |
| MLE-InsightBench | IAAR | arXiv HTML: insights come from "the descriptions, datasets, solution notebooks, and writeups of the source competitions" and are assembled offline before target tasks. The evaluated system accumulates no memory across tasks. |
| PATH-Bench | 列表外 | Sec. 3.2: BigCodeBench is "a single-turn benchmark that evaluates practical program synthesis under complex instructions and diverse function calls". Nothing mentions repos, coding-agent sessions or project conventions. |
| ReMe | IAAR | Sec.4.1: "we use 90 training tasks for the initial experience acquisition stage and evaluate agents on 168 test-normal tasks" (AppWorld); BFCL-V3 function calling. The paper describes no repo or software-engineering sessions. |
| ReplayLens | IAAR | Abstract: ReplayLens is 'a black-box audit that changes one relationship in the stored history at a time'. In the code case (Sec 4.7), a four-entry patch history is supplied per task, not carried across sessions. |
| SCLATE | IAAR | Section 4.3 heading 'Single-session post-training on SWE-Gym'; SWE-bench Verified is only a transfer check ('The trained models transfer to SWE-bench Verified'). Multi-session recall (Sec 4.2) uses LongMemEval/PersonaMem, not code. |
| SEAGym | TeleAI | arXiv HTML Sec 3.1: the mutable harness includes "prompts, memories, skills, experience libraries, tools, middleware, project files, runtime configuration". Train tasks mix Terminal-Bench 2.0 with HLE Math/Physics. |
| Self-Propagating Misalignment in LLM Agents | IAAR | Sec III-D: 'Each scenario defines a specific tool call with specific arguments as a deterministic condition' for the misaligned action. Only about 4 of 20 scenarios (H06, H07, U04, U05) are code or repo settings. |
| StreamBench | IAAR | Text-to-SQL: "the agent has to convert users' natural language queries into SQL code"; DS-1000 is "Python programming questions from StackOverflow" (arXiv HTML 2406.08747, task section). Instances are independent, with no repo or session history. |

</details>

### `parametric`

核实了 49 条主张：列表内确认 8 个，列表外确认 18 个，否定 23 个，未定 0 个。

**列表内、经确认属于该类型的 benchmark**

| Benchmark | 收录它的列表 | 证据（核实者引用） |
| --- | --- | --- |
| [Cross-Lingual Unlearning Tensor](https://arxiv.org/abs/2609.40286) | IAAR | Repo README: models are "fine-tuned on fictional biography facts (TOFU) in one language, unlearned with SimNPO, GradDiff or RMU, and then asked about those facts in 174 languages". Paper §2 Evaluation protocol scores oracle-normalized residual access (R=0 matc |
| [Episodic Memory Benchmark](https://arxiv.org/abs/2501.13121) | IAAR | Sec. 5.1: '(3) Parametric Memory via Fine-Tuning, where memory is stored within the model's parameters'. Table 3 scores fine-tuned GPT-4o-mini against in-context and RAG on the same questions (F1 0.83 vs 0.54/0.60 on single-event questions). |
| [Harness the Memory](https://arxiv.org/abs/2608.15008) | IAAR | App. B.2, M9 Adapter Tuning: 'A LoRA adapter (r=8) is then fine-tuned on these pairs ... no explicit retrieval step occurs'. Sec. 3 uses a 'shared harness, backbone, prompting'; Tables 1-2 list M9 with the non-parametric substrates. |
| [IDUnlearn-Bench](https://arxiv.org/abs/2609.33481) | IAAR | Sec. 4.1: 'We fine-tune each Base model on the profile supervision set to obtain Vanilla and initialize every unlearning method from the same checkpoint'. Sec. 3.1: 'The supervision set contains 10,050 direct profile QAs.' |
| [LOCCO](https://aclanthology.org/2025.findings-acl.1014) | IAAR | §2.2: "We adjust model parameters through supervised fine-tuning, enabling models to internalize key information from long-term dialogues". §4.3: models are trained sequentially over six periods and tested on D1 using Q1 after each phase. |
| [MemOps](https://arxiv.org/abs/2607.12893) | IAAR | Sec. 4.1: 'we test the parameter-update baseline Temp-LoRA'. Sec. 1: 'Parametric memory, which folds interaction history directly into model parameters' is 'markedly unreliable'. Tables 3-5 score Temp-LoRA beside RAG, MemOS, Mem0 and long-context models. |
| [MPR](https://arxiv.org/abs/2508.13250) | IAAR | Sec. 1: 'Implicit memory refers to storing users' personalized information within model parameters'. Sec. 3.4.2/5.1: LoRA-based MaskSFT/AskSFT are run against explicit RAG memory, all scored by Exact Match on the same 2-10 hop QA. |
| [OpenUnlearning](https://arxiv.org/abs/2506.12618) | IAAR | Repo README: 'An easily extensible framework unifying LLM unlearning evaluation benchmarks' (TOFU, MUSE, WMDP). It releases 'TOFU Models w & w/o Knowledge' and unlearned models for meta-evaluating forgetting metrics. |

**列表外、经确认属于该类型的 benchmark（六个来源都没有收录）**

| Benchmark | 证据（核实者引用） |
| --- | --- |
| [AToKe](https://arxiv.org/abs/2312.05497) | Paper, AToKe section: 'AToKe-ME, includes temporal knowledge Multiple Edits'. Methods section: 'All of the above model editing methods make changes to the parameters of the model' (CFT, MEND, ROME, MEMIT). |
| [Benchmarking and Rethinking Knowledge Editing (event-based & general-purpose datasets)](https://arxiv.org/abs/2505.18690) | Paper (arXiv HTML, related-work note): "This work extends [63] by providing a comprehensive benchmark"; abstract: "we introduce more complex event-based datasets and general-purpose datasets drawn from other tasks". Repo name: Knowledge-Editing-Benchmark. |
| [CodeUpdateArena](https://arxiv.org/abs/2407.06249) | README: goal is to 'update an LLM about code API update' and solve tasks 'without providing documentation of the update at inference time'. FT(U) runs continued pretraining on the update docstring (LoRA). Prepending is the in-context baseline. |
| [ConflictEdit / RoundEdit (Pitfalls of Knowledge Editing)](https://arxiv.org/abs/2310.02129) | Paper Sec. 3-4: 'we construct ConflictEdit by sampling ... Reverse Edit and Composite Edit' and 'construct a dataset RoundEdit from WikiData'. FT updates 'the model's parameters by gradient descent'. Metrics: Conflict Score and Distortion. |
| [EvoWiki](https://arxiv.org/abs/2412.13582) | Sec.4.1: "We integrate new knowledge into the model using continual pre-training (CPT) and supervised fine-tuning (SFT)"; Sec.4.4 Continual Learning and 4.5 Combination of RAG and CL. |
| [ForgetBench](https://arxiv.org/abs/2607.26455) | Sec 1: "our work focuses on intrinsic parametric memory, where knowledge is encoded into model parameters and forgetting emerges from ... subsequent model updates." Sec 5.1 evaluates MEMIT, WISE, AlphaEdit and UltraEdit sequentially (T=500). |
| [HalluEditBench](https://arxiv.org/abs/2410.16251) | Paper Sec. 2.3 'chose 7 representative techniques': ROME, MEMIT, FT-L, FT-M, LoRA (weight editing) plus ICE and GRACE. Abstract: five dimensions, Efficacy, Generalization, Portability, Locality and Robustness. |
| [KnowEdit](https://arxiv.org/abs/2401.01286) | Sec.3.4 New Benchmark: KnowEdit: "six selected datasets for the evaluation of knowledge editing methods ... insertion, modification, and erasure settings"; metrics edit success, portability, locality, fluency. |
| [KUP (Knowledge Update Playground)](https://arxiv.org/abs/2504.12523) | Intro: "we focus on continued pre-training (CPT) methods that directly update model parameters to memorize updated facts"; test set of 6260 direct/indirect probing questions (Sec.4.1 KUPEval). |
| [LIFESTATE-BENCH](https://arxiv.org/abs/2503.23514) | Evaluation section: "The evaluation methods fall into two broad categories: (i) parametric and (ii) non-parametric"; parametric = Knowledge Editing-GRACE and LoRA Fine-Tuning on prior episodes. |
| [MMEdit](https://arxiv.org/abs/2310.08475) | Sec 3.1: "Assuming we have a multimodal LLM f parameterized by θ ... what we need is an updated θ_e with f(i_e, x_e; θ_e) = y_e." Table 1 lists E-VQA and E-IC splits. |
| [MQuAKE](https://arxiv.org/abs/2305.14795) | Sec.2: "For the methods we assess in Section 4, [the editor] modifies the weights of [the model] in an attempt to incorporate [edits]"; MeLLo keeps model frozen with external store. |
| [QAEdit (with WILD evaluation)](https://arxiv.org/abs/2502.11177) | Paper: 'QAEdit contains 19,249 samples across ten categories'. Sequential editing 'with a batch size of 1, i.e., updating knowledge incrementally'. FT-M 'directly optimizes model parameters at each step'. |
| [RippleEdits](https://arxiv.org/abs/2307.12976) | Abstract: "We evaluate prominent editing methods on RippleEdits, showing that they fail to introduce consistent changes in the model's knowledge"; in-context baseline vs "explicit parametric updates". |
| [TiC-LM](https://arxiv.org/abs/2504.02107) | Sec.4.2: TiC-Wiki aims to "isolate changed/unchanged factual knowledge"; metrics: "Backward transfer ... capturing how well continual checkpoints do on older months" (forgetting). |
| [UniEdit](https://arxiv.org/abs/2505.12345) | Paper Sec. 5.1: 'We evaluate various types of editors, spanning methods that modify model parameters or use external modules: Fine-Tuning (FT), ROME, AlphaEdit, SERAC, T-Patcher, and GRACE'. Table 2 reports Rel./Gen./Loc. |
| [WikiBigEdit](https://arxiv.org/abs/2503.05683) | README (ExplainableML/WikiBigEdit): 'over 500K question-answer pairs for knowledge editing'; paper Sec. 4 compares ROME/R-ROME/MEMIT/WISE and LoRA 'trained for 10 epochs on each timestep' against a RAG memory. |
| [WikiDYK](https://arxiv.org/abs/2505.12306) | Sec.4: "we focus on comparing approaches that can internalize new knowledge into model parameters"; Fig.1: "We inject the knowledge ... via continued pre-training" then evaluate injected model. |

<details><summary>被否定的主张</summary>

| 条目 | 来源 | 否定理由（核实者引用） |
| --- | --- | --- |
| Cross-Lingual Transferability of TDE Attacks | IAAR | arXiv HTML: "We do not release the underlying dataset itself". The paper uses "memory" only once ("extractable memory") and is framed as a training-data-extraction security attack. |
| Delayed Supervision for Test-Time LMs | IAAR | arXiv HTML: memory is "sequence-specific fast weights or associative state updated from the current input during inference"; evaluation uses "shared BABILong and RULER evaluation panels". No new benchmark. |
| Evo-Memory | TeleAI, Cognee | Appendix E: "The evaluated LLMs are used solely for inference ... without modifying their pre-trained parameters. Memory modules operate externally and do not alter the underlying model weights" |
| GemmaSV (Auditable Deletion) | IAAR | arXiv HTML, Appendix B: "Only global layers are replaced; all pretrained parameters remain fixed." Memory is stored as key/value rows plus an SVM gate, and "Raw benchmark histories... are not redistributed". |
| LaMP | IAAR | arXiv 2304.11406 Sec. 3: two strategies are "(1) fine-tuning the LM for each user and (2) prompting a shared LM with user specific input". The paper then focuses on (2) because (1) is too costly. |
| MemoReason | IAAR | Sec. 3: nine existing models evaluated; interventions only replace entities in input documents. No weight editing, fine-tuning, injection or unlearning; parametric memory influence inferred from factual-vs-fictitious accuracy gaps. |
| Memory vs. Context replication | IAAR | Abstract: a reproducibility study of Yu et al. (2023) for the BlackboxNLP 2026 Reproducibility Challenge. It probes pretrained memorized facts against in-context statements and does no writing, editing or injection of knowledge into weights. |
| MemoryBench | TeleAI, IAAR | §3.1: "we also implemented a supervised fine-tuning baselines (SFT) and reported its performance in A.3.9". A.3.9 says of the SFT data: "these dialogues are different from the training dialogues used above". The repo README lists "8 memory-system baselines", n |
| MemoryData | TeleAI, IAAR | README: "unifies four benchmark families (MemoryAgentBench, LoCoMo, LongBench, MemBench)"; evaluated systems are Mem0, Zep, Letta, MemOS, A-MEM and others. No fine-tuning, LoRA or editing arm was found in the paper or repo. |
| MemToC | IAAR | Sec. 1: 'LLM memory correctness is measured independently for each model by comparing its closed-book answer'; SFT/DPO is a mitigation experiment (Sec. 4.3), not writing/editing knowledge. |
| MT fine-tuning forgetting mitigation study | IAAR | arXiv abstract: the paper compares mitigation methods "anchored to auxiliary data, to model outputs, and to base model parameters" during MT fine-tuning of Llama 3.x. No new benchmark or dataset is mentioned. |
| No Hindsight for LLM Fact-Checkers | IAAR | arXiv abstract: the authors measure leakage "on AVeriTeC and QuanTemp++ by reconstructing point-in-time evidence conditions and probing model representations". They use existing datasets and introduce no new benchmark. |
| Panini | IAAR | Sec. 3.4 Baselines: "We compare Panini against non-parametric memory systems spanning (i) chunk-based retrieval, (ii) structure-augmented memories, and (iii) agentic multi-step retrieval." Abstract: "the base model remains fixed". |
| PersonaMem | TeleAI, IAAR, Cognee | Appendix A.2: "Our current exploration of retrieval-augmented methods, such as RAG and Mem0, is intended as a proof of concept". The evaluated arms are only long-context prompting and RAG/Mem0. |
| PersonaMem-v2 | Tsinghua, IAAR, Cognee | Sec. 4.2: "The training dataset contains 18,000 samples with no persona overlap with the benchmark set." RFT trains general long-context reasoning; user facts are not stored in the weights. |
| PrefEval | IAAR | Sec. 3.7: "We fine-tuned the Mistral-7B model using SFT on 80% of the topics in PrefEval and evaluated it on the remaining unseen 20% topics". This trains a general skill; preferences are not stored in the weights. |
| ProTTT | IAAR | arXiv HTML: "We evaluate ProTTT on CMV, LaMP-3, and PersonaMem"; the paper only promises to "release the source code upon acceptance" and introduces no new benchmark. |
| REALTALK | Tsinghua | §6.1.1: '(2) w/ fine-tuning: An LLM fine-tuned on C_a and tested on C_b'. The scores measure emulation of a speaker's style (EI attributes), not recall of knowledge. Memory probing (Table 3) has no fine-tuning condition. |
| SCLATE | IAAR | arXiv HTML: configurations are Claude Code, Hermes and Codex harnesses with Native, Mem0, Hindsight or GBrain memory, saved as "a directory snapshot or a sidecar export". No parametric-memory configuration was found. |
| StuLife | Tsinghua | Sec. 5 RQ III / Table 4: "For training-based evolution, we employ an on-policy Rejection Sampling Fine-Tuning (RFT) ... on the Qwen3-8B model". This is one demo run, on a different model than the 235B inference-time arm. |
| TRIAGE | IAAR | Abstract and §5 Conclusion: "a benchmark-agnostic evaluation framework that complements behavioral unlearning evaluation". §4.1 says the forget and adjacent partitions "follow the corresponding forget/retain construction". §5 leaves "carefully designed tripart |
| Unlearning with Control (UWC) | IAAR | Ethics Statement: "Rather than developing new methods, we focus on ensuring effective evaluations and fair comparisons"; §6: "main evaluations were based on the well-established benchmarks of TOFU". README: "If you find our metrics beneficial". |
| UWC (LLM unlearning evaluation) |  | arXiv 2406.09179v2 §1: the authors refer to "our evaluation framework as 'unlearning with control' (UWC)"; the only data is existing TOFU (locuslab/TOFU in the repo README), and no new dataset is introduced. |

</details>

外部检索另找到 114 个未逐条核实的候选（只抽样核实了一部分，见上）：TOFU；WMDP；RWKU；KnowUnDo；MLLMU-Bench；LUME；K-Bench；MUDAPIBench；EvolvingQA；OCKL benchmark (Online Continual Knowledge Learning)；PhoneBook & PaperQA (LoRA as Knowledge Memory)；TTT deployment-memory behavioral evaluation framework (Beyond Perplexity)；NanoKnow；ParallelEvents；Continuous Knowledge Drift benchmark (RAG or Learning? / Chronos)；Wikipedia-2024 multi-hop novel-knowledge dataset (Fine-Tuning vs. RAG)；Current Events task (Fine-Tuning or Retrieval?)；Entity Inferences / ECBD knowledge-propagation benchmark；DeepKnowledge；Hubble；MMEVOKE；MMKU-Bench；Wiki-Newpages-2023-QA；SE-Bench；Concept-1K；Wiki2023；Fictional Knowledge dataset；P-RAG new-knowledge QA benchmark；DyKnow；V-DyKnow；CopyBench；WikiMem；CopyShield；MRLF-Bench；CounterFact+；DUnE；RaKE；BAKE；ReCoE；LEME；EvEdit；ELKEN；AKEW；MLaKE；TAXI；TKEMQA；CROLIN-MQUAKE；EVOKE (Editing Overfit)；CLMEEval；ScEdit；COMPKE；MedEditBench；DocTER；CLM-Bench；Logical-rules knowledge editing benchmark；EditRisk-Bench；CKnowEdit；UnKEBench；UltraEditBench；EditEverything；ChronoEdit；Wikidata belief-revision testbed for model editing；EDAPIBench；UPQA；SA-MCQ (Surface Compliance diagnostic)；MIKE；VLKEB；MC-MKE；MMKE-Bench；ComprehendEdit；MedMKEB；MultiMedEdit；UniKE；M3Bench；ConceptVectors；PISTOL；Eval-DU (deep unlearning)；CLEAR；DUSK；R-TOFU；BLUR；PULSE；UnLOK-VQA；Behemoth；AMNESIA；PPU-Bench；LACUNA；ConceptGuard；Leak-Resistant Unlearning；UNLINK-VL；mu^2-Bench；CLLPU；Trajectory unlearning benchmarks (ALFWorld/WebShop)；Unlearning Mirage dynamic evaluation framework；FAME；WaterDrum；WMDP++；PROD source-code unlearning benchmark；Pre-trained LLM unlearning benchmark (arXiv/books/GitHub)；PEBench；SafeEraser；OFFSIDE；PRMU；HANKER；UnifiedMemBench (UMB)；FictionalQA；CounterFact；MUSE (Machine Unlearning Six-Way Evaluation)；CKL (Continual Knowledge Learning benchmark)；TemporalWiki；StreamingQA；PopQA；PEFT-U；ConflictBank

## 候选清单（阶段 4 按此添加）

已入库的 12 个样例不再列出。通用 benchmark 与“不是 benchmark”的条目不作为候选。外部检索找到但尚未核实的参数化候选（见上）在核实前不作为候选。

### P0：三类缺口中经确认的 benchmark（86 个）

| Benchmark | 类型 | 是否已在某个列表中 |
| --- | --- | --- |
| [AFTER](https://arxiv.org/abs/2606.23127) | `procedural_workflow` | 否 |
| [Agent Memory Leaderboard (AML)](https://github.com/AML-memory/agent-memory-leaderboard) | `procedural_workflow`, `coding_cross_session` | 是 |
| [agent-memory-bench](https://github.com/GiulioDER/agent-memory-bench) | `coding_cross_session` | 是 |
| [AgentCL](https://arxiv.org/abs/2606.02461) | `procedural_workflow`, `coding_cross_session` | 否 |
| [AgenticSTS](https://arxiv.org/abs/2607.02255) | `procedural_workflow` | 是 |
| [AgentStream](https://arxiv.org/abs/2608.00155) | `procedural_workflow` | 否 |
| [AhaBench](https://arxiv.org/abs/2609.05435) | `procedural_workflow` | 否 |
| [AMB (Agent Memory Benchmark)](https://github.com/vectorize-io/agent-memory-benchmark) | `coding_cross_session` | 是 |
| [AToKe](https://arxiv.org/abs/2312.05497) | `parametric` | 否 |
| [BELA](https://arxiv.org/abs/2511.22130) | `procedural_workflow` | 否 |
| [Benchmarking and Rethinking Knowledge Editing (event-based & general-purpose datasets)](https://arxiv.org/abs/2505.18690) | `parametric` | 否 |
| [BenchTrace](https://arxiv.org/abs/2605.29225) | `procedural_workflow` | 否 |
| [CAPA](https://arxiv.org/abs/2607.26611) | `coding_cross_session` | 否 |
| [ChainSWE](https://arxiv.org/abs/2607.02606) | `coding_cross_session` | 否 |
| [CL-Bench (Continual Learning Bench)](https://arxiv.org/abs/2606.05661) | `procedural_workflow`, `coding_cross_session` | 否 |
| [CodeUpdateArena](https://arxiv.org/abs/2407.06249) | `parametric` | 否 |
| [ConflictEdit / RoundEdit (Pitfalls of Knowledge Editing)](https://arxiv.org/abs/2310.02129) | `parametric` | 否 |
| [ConsolidationBench](https://arxiv.org/abs/2609.33013) | `procedural_workflow` | 是 |
| [ContinualSkillBench](https://arxiv.org/abs/2608.03874) | `procedural_workflow` | 否 |
| [Cross-Lingual Unlearning Tensor](https://arxiv.org/abs/2609.40286) | `parametric` | 是 |
| [DreamBench-SWE](https://arxiv.org/abs/2608.20664) | `procedural_workflow`, `coding_cross_session` | 是 |
| [EconSkills](https://arxiv.org/abs/2609.19523) | `procedural_workflow` | 是 |
| [EngramBench](https://arxiv.org/abs/2609.39284) | `procedural_workflow`, `coding_cross_session` | 否 |
| [Episodic Memory Benchmark](https://arxiv.org/abs/2501.13121) | `parametric` | 是 |
| [EvaLearn](https://arxiv.org/abs/2506.02672) | `procedural_workflow` | 否 |
| [Evo-Memory](https://arxiv.org/abs/2511.20857) | `procedural_workflow` | 是 |
| [EvoAgentBench](https://arxiv.org/abs/2607.05202) | `procedural_workflow`, `coding_cross_session` | 否 |
| [EvoArena](https://arxiv.org/abs/2606.13681) | `procedural_workflow` | 是 |
| [EvoHarnessBench](https://arxiv.org/abs/2609.04280) | `procedural_workflow` | 否 |
| [EvoMemBench](https://arxiv.org/abs/2605.18421) | `procedural_workflow` | 否 |
| [EvoPathBench](https://arxiv.org/abs/2609.24663) | `procedural_workflow` | 否 |
| [EvoWiki](https://arxiv.org/abs/2412.13582) | `parametric` | 否 |
| [FinEvo-Bench](https://arxiv.org/abs/2608.06144) | `procedural_workflow` | 否 |
| [FinEvolveBench](https://arxiv.org/abs/2606.06960) | `procedural_workflow` | 否 |
| [ForgetBench](https://arxiv.org/abs/2607.26455) | `parametric` | 否 |
| [GDPevo](https://arxiv.org/abs/2608.03764) | `procedural_workflow` | 否 |
| [HalluEditBench](https://arxiv.org/abs/2410.16251) | `parametric` | 否 |
| [Harness the Memory](https://arxiv.org/abs/2608.15008) | `parametric` | 是 |
| [IDUnlearn-Bench](https://arxiv.org/abs/2609.33481) | `parametric` | 是 |
| [Insecure Coding Preferences in Long-Term Memory (dataset)](https://arxiv.org/abs/2607.17619) | `coding_cross_session` | 否 |
| [KnowEdit](https://arxiv.org/abs/2401.01286) | `parametric` | 否 |
| [KUP (Knowledge Update Playground)](https://arxiv.org/abs/2504.12523) | `parametric` | 否 |
| [Learn2Play Bench](https://arxiv.org/abs/2610.08215) | `procedural_workflow` | 否 |
| [LifelongAgentBench](https://arxiv.org/abs/2505.11942) | `procedural_workflow` | 是 |
| [LIFESTATE-BENCH](https://arxiv.org/abs/2503.23514) | `parametric` | 否 |
| [LOCCO](https://aclanthology.org/2025.findings-acl.1014) | `parametric` | 是 |
| [LongMemEval-V2](https://arxiv.org/abs/2605.12493) | `procedural_workflow` | 是 |
| [MedEvoEval](https://arxiv.org/abs/2606.28900) | `procedural_workflow` | 否 |
| [MemOps](https://arxiv.org/abs/2607.12893) | `parametric` | 是 |
| [MemoryBench](https://arxiv.org/abs/2510.17281) | `procedural_workflow` | 是 |
| [MemoryCode](https://arxiv.org/abs/2502.13791) | `coding_cross_session` | 否 |
| [MetaKernelBench](https://arxiv.org/abs/2610.05014) | `procedural_workflow`, `coding_cross_session` | 是 |
| [MLE-InsightBench](https://arxiv.org/abs/2610.04927) | `procedural_workflow` | 是 |
| [MMEdit](https://arxiv.org/abs/2310.08475) | `parametric` | 否 |
| [MPR](https://arxiv.org/abs/2508.13250) | `parametric` | 是 |
| [MQuAKE](https://arxiv.org/abs/2305.14795) | `parametric` | 否 |
| [OmniGameArena](https://arxiv.org/abs/2606.09826) | `procedural_workflow` | 否 |
| [OmniMemEval](https://github.com/MemTensor/OmniMemEval) | `procedural_workflow`, `coding_cross_session` | 是 |
| [OpenUnlearning](https://arxiv.org/abs/2506.12618) | `parametric` | 是 |
| [PAST-Bench](https://arxiv.org/abs/2608.04003) | `procedural_workflow` | 否 |
| [PATH-Bench](https://arxiv.org/abs/2608.01149) | `procedural_workflow` | 否 |
| [QAEdit (with WILD evaluation)](https://arxiv.org/abs/2502.11177) | `parametric` | 否 |
| [RippleEdits](https://arxiv.org/abs/2307.12976) | `parametric` | 否 |
| [S3Gym](https://arxiv.org/abs/2608.31100) | `procedural_workflow` | 否 |
| [SEA-Eval](https://arxiv.org/abs/2604.08988) | `procedural_workflow` | 否 |
| [SEAGym](https://arxiv.org/abs/2606.17546) | `procedural_workflow` | 是 |
| [SeqMem-Eval](https://arxiv.org/abs/2605.15384) | `procedural_workflow` | 否 |
| [ServeLearnBench](https://arxiv.org/abs/2610.07792) | `procedural_workflow` | 否 |
| [SkillCraft](https://arxiv.org/abs/2603.00718) | `procedural_workflow` | 否 |
| [SkillEvolBench](https://arxiv.org/abs/2605.24117) | `procedural_workflow` | 否 |
| [SkillFlow](https://arxiv.org/abs/2604.17308) | `procedural_workflow` | 否 |
| [SkillLearnBench](https://arxiv.org/abs/2604.20087) | `procedural_workflow` | 否 |
| [SLVMBench](https://arxiv.org/abs/2607.11312) | `procedural_workflow` | 是 |
| [STATE-Bench](https://github.com/microsoft/STATE-Bench) | `procedural_workflow` | 是 |
| [Stateful SWE-bench (from TOM-SWE)](https://arxiv.org/abs/2510.21903) | `coding_cross_session` | 否 |
| [StreamBench](https://arxiv.org/abs/2406.08747) | `procedural_workflow` | 是 |
| [StuLife](https://arxiv.org/abs/2508.19005) | `procedural_workflow` | 是 |
| [SWE-Bench-CL](https://arxiv.org/abs/2507.00014) | `procedural_workflow`, `coding_cross_session` | 否 |
| [SWE-ContextBench](https://arxiv.org/abs/2602.08316) | `procedural_workflow`, `coding_cross_session` | 否 |
| [The Agent's First Day (EvoEnv)](https://arxiv.org/abs/2601.08173) | `procedural_workflow` | 否 |
| [TiC-LM](https://arxiv.org/abs/2504.02107) | `parametric` | 否 |
| [Trust-Memevo](https://arxiv.org/abs/2602.03224) | `procedural_workflow` | 否 |
| [UniEdit](https://arxiv.org/abs/2505.12345) | `parametric` | 否 |
| [VibeMemBench](https://arxiv.org/abs/2609.23570) | `procedural_workflow`, `coding_cross_session` | 是 |
| [WikiBigEdit](https://arxiv.org/abs/2503.05683) | `parametric` | 否 |
| [WikiDYK](https://arxiv.org/abs/2505.12306) | `parametric` | 否 |

### P1：被两个及以上列表收录的记忆 benchmark（20 个）

| Benchmark | 首次公开 | WEN6 | WEN6 fork 分支 | Tsinghua | TeleAI | IAAR | topoteretes | Cognee | 记忆类型 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [PersonaMem](https://arxiv.org/abs/2504.14225) | 2025-04 |  |  |  | ✓ | ✓ |  | ✓ | `personalization`, `conversational_longterm`, `semantic_knowledge_update` |
| [BEAM](https://arxiv.org/abs/2510.27246) | 2025-10 |  |  |  | ✓ |  | ✓ | ✓ | `conversational_longterm`, `semantic_knowledge_update`, `episodic`, `personalization` |
| [PersonaMem-v2](https://arxiv.org/abs/2512.06688) | 2025-12 |  |  | ✓ |  | ✓ |  | ✓ | `personalization`, `conversational_longterm` |
| [ATM-Bench](https://arxiv.org/abs/2603.01990) | 2026-03 |  |  |  | ✓ | ✓ | ✓ |  | `personalization`, `episodic`, `multimodal` |
| [EmbodiedMemory-Bench (EMem-Bench)](https://arxiv.org/abs/2609.28236) | 2026-09 |  | ✓ |  | ✓ | ✓ |  |  | `episodic`, `semantic_knowledge_update`, `multimodal`, `embodied` |
| [MADial-Bench](https://arxiv.org/abs/2409.15240) | 2024-09 |  |  | ✓ |  | ✓ |  |  | `conversational_longterm`, `episodic` |
| [Minerva](https://arxiv.org/abs/2502.03358) | 2025-02 |  |  |  | ✓ | ✓ |  |  | `semantic_knowledge_update` |
| [StoryBench](https://arxiv.org/abs/2506.13356) | 2025-06 |  |  | ✓ |  | ✓ |  |  | `episodic` |
| [ZH-4O (MOOM)](https://arxiv.org/abs/2509.11860) | 2025-09 |  |  |  | ✓ | ✓ |  |  | `conversational_longterm`, `personalization` |
| [ConvoMem](https://arxiv.org/abs/2511.10523) | 2025-11 |  |  | ✓ |  |  | ✓ |  | `conversational_longterm`, `personalization`, `semantic_knowledge_update` |
| [HaluMem](https://arxiv.org/abs/2511.03506) | 2025-11 |  |  |  | ✓ | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update`, `personalization`, `episodic` |
| [CloneMem](https://arxiv.org/abs/2601.07023) | 2026-01 |  |  | ✓ |  | ✓ |  |  | `personalization`, `episodic`, `semantic_knowledge_update` |
| [KnowMe-Bench](https://arxiv.org/abs/2601.04745) | 2026-01 |  |  | ✓ |  | ✓ |  |  | `personalization`, `episodic` |
| [RealMem](https://arxiv.org/abs/2601.06966) | 2026-01 |  |  | ✓ |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update`, `personalization`, `episodic` |
| [MemoryArena](https://arxiv.org/abs/2602.16313) | 2026-02 |  |  |  |  | ✓ |  | ✓ | `episodic`, `personalization` |
| [AMemGym](https://arxiv.org/abs/2603.01966) | 2026-03 |  |  |  | ✓ | ✓ |  |  | `conversational_longterm`, `personalization`, `semantic_knowledge_update` |
| [RHELM](https://arxiv.org/abs/2605.31086) | 2026-05 |  |  |  | ✓ | ✓ |  |  | `conversational_longterm`, `personalization`, `semantic_knowledge_update`, `episodic` |
| [MemoryData](https://arxiv.org/abs/2606.24775) | 2026-06 |  |  |  | ✓ | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update` |
| [StreamMemBench](https://arxiv.org/abs/2606.14571) | 2026-06 |  |  |  | ✓ | ✓ |  |  | `episodic`, `personalization`, `multimodal` |
| [VoxMem](https://arxiv.org/abs/2609.32607) | 2026-09 |  |  |  | ✓ | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update`, `multimodal` |

### P2：只被一个列表收录的记忆 benchmark（104 个）

| Benchmark | 首次公开 | WEN6 | WEN6 fork 分支 | Tsinghua | TeleAI | IAAR | topoteretes | Cognee | 记忆类型 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [SCM (Self-Controlled Memory) dataset](https://arxiv.org/abs/2304.13343) | 2023-04 |  |  |  |  | ✓ |  |  | `conversational_longterm` |
| [DMR (Deep Memory Retrieval, from MemGPT)](https://arxiv.org/abs/2310.08560) | 2023-10 |  |  |  |  |  |  | ✓ | `conversational_longterm`, `personalization` |
| [TeaFarm (THEANINE)](https://aclanthology.org/2025.naacl-long.435) | 2024-06 |  |  |  |  | ✓ |  |  | `conversational_longterm` |
| [GoodAI LTM Benchmark](https://arxiv.org/abs/2409.20222) | 2024-09 |  |  | ✓ |  |  |  |  | `conversational_longterm`, `semantic_knowledge_update` |
| [MemDaily (MemSim)](https://arxiv.org/abs/2409.20163) | 2024-09 |  |  |  |  | ✓ |  |  | `personalization`, `conversational_longterm` |
| [PersonaBench](https://aclanthology.org/2025.findings-acl.49) | 2025-02 |  |  |  |  | ✓ |  |  | `personalization` |
| [PrefEval](https://arxiv.org/abs/2502.09597) | 2025-02 |  |  |  |  | ✓ |  |  | `personalization`, `conversational_longterm` |
| [REALTALK](https://arxiv.org/abs/2502.13270) | 2025-02 |  |  | ✓ |  |  |  |  | `conversational_longterm`, `episodic` |
| [TReMu](https://arxiv.org/abs/2502.01630) | 2025-02 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `episodic` |
| [ImplexConv](https://aclanthology.org/2025.emnlp-main.580) | 2025-03 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization` |
| [MEMENTO](https://arxiv.org/abs/2505.16348) | 2025-05 |  |  |  |  | ✓ |  |  | `personalization`, `episodic`, `embodied` |
| [MS-TOD (MemGuide)](https://arxiv.org/abs/2505.20231) | 2025-05 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization` |
| [M3-Bench (M3-Agent)](https://arxiv.org/abs/2508.09736) | 2025-08 |  |  |  |  | ✓ |  |  | `episodic`, `multimodal` |
| [OdysseyBench](https://arxiv.org/abs/2508.09124) | 2025-08 |  |  |  | ✓ |  |  |  | `conversational_longterm` |
| [FlashAdventure](https://aclanthology.org/2025.emnlp-main.1192) | 2025-09 |  |  |  |  | ✓ |  |  | `episodic`, `multimodal` |
| [MemTrack](https://arxiv.org/abs/2510.01353) | 2025-10 |  |  |  |  |  |  | ✓ | `semantic_knowledge_update`, `episodic` |
| [TeleEgo](https://arxiv.org/abs/2510.23981) | 2025-10 |  |  |  | ✓ |  |  |  | `episodic`, `multimodal` |
| [AndroidIntent (PersonalAlign)](https://arxiv.org/abs/2601.09636) | 2026-01 |  |  |  |  | ✓ |  |  | `personalization` |
| [CAME-Bench](https://arxiv.org/abs/2601.10702) | 2026-01 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update` |
| [EvolMem](https://arxiv.org/abs/2601.03543) | 2026-01 |  |  |  |  | ✓ |  |  | `conversational_longterm` |
| [Mem-Gallery](https://arxiv.org/abs/2601.03515) | 2026-01 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update`, `episodic`, `multimodal` |
| [MemoryRewardBench](https://arxiv.org/abs/2601.11969) | 2026-01 |  |  |  |  | ✓ |  |  | `conversational_longterm` |
| [RPEval](https://arxiv.org/abs/2601.16621) | 2026-01 |  |  |  |  | ✓ |  |  | `personalization` |
| [AMA-Bench](https://arxiv.org/abs/2602.22769) | 2026-02 |  |  |  |  | ✓ |  |  | `episodic`, `semantic_knowledge_update` |
| [MemEmo (HLME)](https://arxiv.org/abs/2602.23944) | 2026-02 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update` |
| [Neuromem](https://arxiv.org/abs/2602.13967) | 2026-02 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update` |
| [PersistBench](https://arxiv.org/abs/2602.01146) | 2026-02 |  |  |  |  | ✓ |  |  | `personalization` |
| [LifeBench](https://arxiv.org/abs/2603.03781) | 2026-03 |  |  |  |  | ✓ |  |  | `personalization`, `episodic`, `semantic_knowledge_update` |
| [Persona-MME](https://arxiv.org/abs/2604.13074) | 2026-03 |  |  |  | ✓ |  |  |  | `personalization`, `conversational_longterm`, `semantic_knowledge_update`, `multimodal` |
| [RealPref](https://arxiv.org/abs/2603.04191) | 2026-03 |  |  |  |  | ✓ |  |  | `personalization`, `conversational_longterm` |
| [RMBench](https://arxiv.org/abs/2603.01229) | 2026-03 |  |  |  | ✓ |  |  |  | `embodied` |
| [LoCoMo-Refined](https://github.com/mem-eval-suite/LoCoMo_refined) | 2026-04 |  |  |  | ✓ |  |  |  | `conversational_longterm`, `episodic` |
| [MemHome / MemHomeLife](https://arxiv.org/abs/2604.10110) | 2026-04 |  |  |  |  | ✓ |  |  | `personalization`, `semantic_knowledge_update`, `conversational_longterm` |
| [StratMem-Bench](https://arxiv.org/abs/2604.26243) | 2026-04 |  |  |  |  | ✓ |  |  | `conversational_longterm` |
| [EgoStream](https://arxiv.org/abs/2605.31557) | 2026-05 |  |  |  |  | ✓ |  |  | `episodic`, `multimodal` |
| [MBench](https://arxiv.org/abs/2606.00793) | 2026-05 |  |  |  | ✓ |  |  |  | `multimodal` |
| [MEMAUDIT](https://arxiv.org/abs/2605.02199) | 2026-05 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update` |
| [MemEye](https://arxiv.org/abs/2605.15128) | 2026-05 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update`, `multimodal` |
| [Momento](https://arxiv.org/abs/2606.00832) | 2026-05 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization`, `semantic_knowledge_update` |
| [PrecisionMemBench](https://arxiv.org/abs/2605.11325) | 2026-05 |  |  | ✓ |  |  |  |  | `semantic_knowledge_update` |
| [RefMem-Bench](https://arxiv.org/abs/2606.01223) | 2026-05 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization`, `multimodal` |
| [RoboMemArena](https://arxiv.org/abs/2605.10921) | 2026-05 |  |  |  | ✓ |  |  |  | `embodied` |
| [STALE](https://arxiv.org/abs/2605.06527) | 2026-05 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update`, `conversational_longterm`, `personalization` |
| [SuperMemory-VQA](https://arxiv.org/abs/2606.00825) | 2026-05 |  |  |  |  | ✓ |  |  | `episodic`, `multimodal` |
| [WorldMemArena](https://arxiv.org/abs/2605.29341) | 2026-05 |  |  |  |  | ✓ |  |  | `episodic`, `semantic_knowledge_update`, `personalization`, `conversational_longterm`, `multimodal`, `embodied` |
| [DMV-Bench](https://arxiv.org/abs/2606.27499) | 2026-06 |  |  |  |  | ✓ |  |  | `episodic`, `multimodal` |
| [ForgetEval](https://arxiv.org/abs/2606.15903) | 2026-06 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update` |
| [GateMem](https://arxiv.org/abs/2606.18829) | 2026-06 |  |  |  |  | ✓ |  |  | `multi_agent_group`, `semantic_knowledge_update`, `conversational_longterm`, `memory_security` |
| [H2HMem](https://arxiv.org/abs/2606.09461) | 2026-06 |  |  |  |  | ✓ |  |  | `multi_agent_group`, `conversational_longterm`, `multimodal` |
| [HUSH-Bench](https://arxiv.org/abs/2606.06055) | 2026-06 |  |  |  |  | ✓ |  |  | `memory_security` |
| [MemoryDocDataSet](https://arxiv.org/abs/2606.04442) | 2026-06 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `multi_agent_group` |
| [MEMPROBE (MemAudit)](https://arxiv.org/abs/2606.24595) | 2026-06 |  |  |  |  | ✓ |  |  | `personalization`, `conversational_longterm` |
| [MemTrace](https://arxiv.org/abs/2606.17328) | 2026-06 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization`, `semantic_knowledge_update` |
| [MIST](https://arxiv.org/abs/2606.10949) | 2026-06 |  |  |  |  | ✓ |  |  | `conversational_longterm` |
| [MPBench](https://arxiv.org/abs/2606.04329) | 2026-06 |  |  |  |  | ✓ |  |  | `memory_security` |
| [SubtleMemory](https://arxiv.org/abs/2606.05761) | 2026-06 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update`, `personalization` |
| [Agent-Memory Integrity Benchmark](https://github.com/DanceNitra/agent-memory-integrity) | 2026-07 |  |  |  | ✓ |  |  |  | `semantic_knowledge_update` |
| [Bad Memory](https://arxiv.org/abs/2607.14611) | 2026-07 |  |  |  |  | ✓ |  |  | `memory_security` |
| [Ground Truth First (Veracium)](https://arxiv.org/abs/2607.21962) | 2026-07 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization`, `semantic_knowledge_update`, `episodic`, `memory_security` |
| [InMind](https://arxiv.org/abs/2607.24368) | 2026-07 |  |  |  |  | ✓ |  |  | `personalization`, `conversational_longterm` |
| [MemSecBench](https://arxiv.org/abs/2607.27080) | 2026-07 |  |  |  |  | ✓ |  |  | `memory_security` |
| [MemSyco-Bench](https://arxiv.org/abs/2607.01071) | 2026-07 |  |  |  |  | ✓ |  |  | `personalization`, `semantic_knowledge_update` |
| [MERIT](https://arxiv.org/abs/2609.05441) | 2026-07 |  |  |  |  | ✓ |  |  | `episodic`, `semantic_knowledge_update`, `personalization` |
| [PM-Bench](https://arxiv.org/abs/2607.12385) | 2026-07 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update` |
| [RECON](https://arxiv.org/abs/2607.16716) | 2026-07 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update`, `episodic` |
| [RUMBA](https://arxiv.org/abs/2607.21447) | 2026-07 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `episodic`, `semantic_knowledge_update` |
| [Sequential EQA](https://arxiv.org/abs/2607.21571) | 2026-07 |  |  |  |  | ✓ |  |  | `episodic`, `multimodal`, `embodied` |
| [ECCBench](https://arxiv.org/abs/2609.00103) | 2026-08 |  |  |  |  | ✓ |  |  | `multimodal` |
| [MemToC](https://arxiv.org/abs/2608.26295) | 2026-08 |  |  |  |  | ✓ |  |  | — |
| [MemTrapBench](https://arxiv.org/abs/2608.20202) | 2026-08 |  |  |  |  | ✓ |  |  | `memory_security` |
| [MemUse](https://arxiv.org/abs/2608.24189) | 2026-08 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization` |
| [MobileMem](https://arxiv.org/abs/2608.13606) | 2026-08 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization`, `episodic`, `semantic_knowledge_update`, `multimodal` |
| [SCALE-QA](https://arxiv.org/abs/2608.25655) | 2026-08 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update` |
| [StateMemBench](https://arxiv.org/abs/2608.19652) | 2026-08 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update` |
| [TANGLE](https://arxiv.org/abs/2608.13921) | 2026-08 |  |  |  |  | ✓ |  |  | `personalization`, `conversational_longterm`, `semantic_knowledge_update` |
| [UtilMem](https://arxiv.org/abs/2608.30508) | 2026-08 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization` |
| [APM-Bench](https://arxiv.org/abs/2609.37559) | 2026-09 |  |  |  |  | ✓ |  |  | `episodic`, `semantic_knowledge_update`, `multimodal` |
| [CapMem](https://arxiv.org/abs/2609.17688) | 2026-09 |  |  |  |  | ✓ |  |  | `episodic`, `multimodal` |
| [CICM](https://arxiv.org/abs/2609.38866) | 2026-09 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update` |
| [CoMemBench](https://arxiv.org/abs/2609.32192) | 2026-09 |  |  |  |  | ✓ |  |  | `multi_agent_group` |
| [CPB (Correlated Promotion Benchmark)](https://arxiv.org/abs/2609.30813) | 2026-09 |  |  |  |  | ✓ |  |  | `multi_agent_group`, `memory_security` |
| [CUE-Mem](https://arxiv.org/abs/2609.32574) | 2026-09 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization`, `multimodal` |
| [DolphinBench](https://arxiv.org/abs/2609.24971) | 2026-09 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization` |
| [ICM-Bench](https://arxiv.org/abs/2609.04438) | 2026-09 |  |  |  |  | ✓ |  |  | `episodic`, `multimodal` |
| [Impact Is Not Invalidation (claim-invalidation benchmark)](https://arxiv.org/abs/2609.25130) | 2026-09 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update` |
| [LAPSE](https://arxiv.org/abs/2609.36457) | 2026-09 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update` |
| [LOCOMO-CONV](https://arxiv.org/abs/2609.03467) | 2026-09 |  |  |  |  | ✓ |  |  | `conversational_longterm` |
| [LSREP](https://arxiv.org/abs/2609.16730) | 2026-09 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update` |
| [MemCalib](https://arxiv.org/abs/2609.24259) | 2026-09 |  |  |  |  | ✓ |  |  | `personalization` |
| [MemoReason](https://arxiv.org/abs/2609.35312) | 2026-09 |  |  |  |  | ✓ |  |  | — |
| [MemProbe](https://arxiv.org/abs/2609.30558) | 2026-09 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update`, `personalization` |
| [MemRiskBench](https://arxiv.org/abs/2609.14976) | 2026-09 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update`, `memory_security` |
| [MemTransfer](https://arxiv.org/abs/2609.32313) | 2026-09 |  |  |  |  | ✓ |  |  | `episodic`, `embodied` |
| [PairPref](https://arxiv.org/abs/2609.34526) | 2026-09 |  |  |  |  | ✓ |  |  | `personalization` |
| [PRAGMA](https://arxiv.org/abs/2609.09664) | 2026-09 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization`, `semantic_knowledge_update` |
| [SimLife-BP](https://arxiv.org/abs/2609.19610) | 2026-09 |  |  |  |  | ✓ |  |  | `personalization`, `semantic_knowledge_update`, `multimodal`, `embodied` |
| [TWIST](https://arxiv.org/abs/2609.28575) | 2026-09 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update`, `memory_security` |
| [Video2Skill](https://arxiv.org/abs/2609.36691) | 2026-09 |  |  |  |  | ✓ |  |  | `multimodal`, `embodied` |
| [What Should an Agent Remember? (bounded-memory streaming-recall benchmark)](https://arxiv.org/abs/2610.00366) | 2026-09 |  |  |  |  | ✓ |  |  | — |
| [CMSC-E (Memory Canonicalization)](https://arxiv.org/abs/2610.05124) | 2026-10 |  |  |  |  | ✓ |  |  | — |
| [DyadMem](https://arxiv.org/abs/2610.03020) | 2026-10 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization`, `episodic`, `semantic_knowledge_update` |
| [EMBER-Bench](https://arxiv.org/abs/2610.05013) | 2026-10 |  |  |  |  | ✓ |  |  | `episodic`, `multimodal`, `embodied` |
| [Knowing the Store](https://arxiv.org/abs/2610.04794) | 2026-10 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update` |
| [RealCompanion](https://arxiv.org/abs/2610.01780) | 2026-10 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization` |

## 对照表：benchmark × 来源列表 × 记忆类型

### 记忆 benchmark（164 个）

按被收录的列表数从多到少、再按时间排序。类型中的 `procedural_workflow` / `coding_cross_session` / `parametric` 只在两轮独立核实确认后才标；`multimodal` / `embodied` / `memory_security` 来自分类时提出的补充标签。

| Benchmark | 首次公开 | WEN6 | WEN6 fork 分支 | Tsinghua | TeleAI | IAAR | topoteretes | Cognee | 记忆类型 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [LoCoMo](https://arxiv.org/abs/2402.17753) （已入库） | 2024-02 | ✓ |  | ✓ | ✓ | ✓ | ✓ | ✓ | `conversational_longterm`, `episodic`, `multimodal` |
| [LongMemEval](https://arxiv.org/abs/2410.10813) （已入库） | 2024-10 | ✓ |  | ✓ | ✓ | ✓ | ✓ | ✓ | `conversational_longterm`, `personalization`, `episodic`, `semantic_knowledge_update` |
| [MemoryAgentBench](https://arxiv.org/abs/2507.05257) （已入库） | 2025-07 | ✓ |  | ✓ | ✓ | ✓ |  | ✓ | `conversational_longterm`, `episodic`, `semantic_knowledge_update` |
| [MemBench](https://arxiv.org/abs/2506.21605) （已入库） | 2025-06 | ✓ |  | ✓ | ✓ | ✓ |  |  | `conversational_longterm`, `personalization`, `semantic_knowledge_update` |
| [PerLTQA](https://arxiv.org/abs/2402.16288) （已入库） | 2024-02 | ✓ |  |  |  | ✓ |  | ✓ | `episodic`, `personalization` |
| [PersonaMem](https://arxiv.org/abs/2504.14225) | 2025-04 |  |  |  | ✓ | ✓ |  | ✓ | `personalization`, `conversational_longterm`, `semantic_knowledge_update` |
| [LifelongAgentBench](https://arxiv.org/abs/2505.11942) | 2025-05 |  |  | ✓ | ✓ | ✓ |  |  | `procedural_workflow` |
| [BEAM](https://arxiv.org/abs/2510.27246) | 2025-10 |  |  |  | ✓ |  | ✓ | ✓ | `conversational_longterm`, `semantic_knowledge_update`, `episodic`, `personalization` |
| [PersonaMem-v2](https://arxiv.org/abs/2512.06688) | 2025-12 |  |  | ✓ |  | ✓ |  | ✓ | `personalization`, `conversational_longterm` |
| [Mem2ActBench](https://arxiv.org/abs/2601.19935) （已入库） | 2026-01 | ✓ |  |  |  | ✓ |  | ✓ | `conversational_longterm`, `personalization` |
| [LoCoMo-Plus](https://arxiv.org/abs/2602.10715) （已入库） | 2026-02 | ✓ |  |  | ✓ | ✓ |  |  | `conversational_longterm`, `personalization` |
| [ATM-Bench](https://arxiv.org/abs/2603.01990) | 2026-03 |  |  |  | ✓ | ✓ | ✓ |  | `personalization`, `episodic`, `multimodal` |
| [EmbodiedMemory-Bench (EMem-Bench)](https://arxiv.org/abs/2609.28236) | 2026-09 |  | ✓ |  | ✓ | ✓ |  |  | `episodic`, `semantic_knowledge_update`, `multimodal`, `embodied` |
| [MSC (Multi-Session Chat)](https://arxiv.org/abs/2107.07567) （已入库） | 2021-07 | ✓ |  |  |  |  |  | ✓ | `conversational_longterm`, `personalization` |
| [DialSim](https://arxiv.org/abs/2406.13144) （已入库） | 2024-06 | ✓ |  |  |  | ✓ |  |  | `conversational_longterm`, `multi_agent_group`, `episodic` |
| [MADial-Bench](https://arxiv.org/abs/2409.15240) | 2024-09 |  |  | ✓ |  | ✓ |  |  | `conversational_longterm`, `episodic` |
| [Minerva](https://arxiv.org/abs/2502.03358) | 2025-02 |  |  |  | ✓ | ✓ |  |  | `semantic_knowledge_update` |
| [StoryBench](https://arxiv.org/abs/2506.13356) | 2025-06 |  |  | ✓ |  | ✓ |  |  | `episodic` |
| [ZH-4O (MOOM)](https://arxiv.org/abs/2509.11860) | 2025-09 |  |  |  | ✓ | ✓ |  |  | `conversational_longterm`, `personalization` |
| [MemoryBench](https://arxiv.org/abs/2510.17281) | 2025-10 |  |  |  | ✓ | ✓ |  |  | `conversational_longterm`, `procedural_workflow` |
| [ConvoMem](https://arxiv.org/abs/2511.10523) | 2025-11 |  |  | ✓ |  |  | ✓ |  | `conversational_longterm`, `personalization`, `semantic_knowledge_update` |
| [Evo-Memory](https://arxiv.org/abs/2511.20857) | 2025-11 |  |  |  | ✓ |  |  | ✓ | `procedural_workflow` |
| [HaluMem](https://arxiv.org/abs/2511.03506) | 2025-11 |  |  |  | ✓ | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update`, `personalization`, `episodic` |
| [CloneMem](https://arxiv.org/abs/2601.07023) | 2026-01 |  |  | ✓ |  | ✓ |  |  | `personalization`, `episodic`, `semantic_knowledge_update` |
| [KnowMe-Bench](https://arxiv.org/abs/2601.04745) | 2026-01 |  |  | ✓ |  | ✓ |  |  | `personalization`, `episodic` |
| [RealMem](https://arxiv.org/abs/2601.06966) | 2026-01 |  |  | ✓ |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update`, `personalization`, `episodic` |
| [MemoryArena](https://arxiv.org/abs/2602.16313) | 2026-02 |  |  |  |  | ✓ |  | ✓ | `episodic`, `personalization` |
| [AMemGym](https://arxiv.org/abs/2603.01966) | 2026-03 |  |  |  | ✓ | ✓ |  |  | `conversational_longterm`, `personalization`, `semantic_knowledge_update` |
| [RHELM](https://arxiv.org/abs/2605.31086) | 2026-05 |  |  |  | ✓ | ✓ |  |  | `conversational_longterm`, `personalization`, `semantic_knowledge_update`, `episodic` |
| [MemoryData](https://arxiv.org/abs/2606.24775) | 2026-06 |  |  |  | ✓ | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update` |
| [StreamMemBench](https://arxiv.org/abs/2606.14571) | 2026-06 |  |  |  | ✓ | ✓ |  |  | `episodic`, `personalization`, `multimodal` |
| [VoxMem](https://arxiv.org/abs/2609.32607) | 2026-09 |  |  |  | ✓ | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update`, `multimodal` |
| [SCM (Self-Controlled Memory) dataset](https://arxiv.org/abs/2304.13343) | 2023-04 |  |  |  |  | ✓ |  |  | `conversational_longterm` |
| [MemoryBank](https://arxiv.org/abs/2305.10250) （已入库） | 2023-05 | ✓ |  |  |  |  |  |  | `conversational_longterm`, `personalization` |
| [DMR (Deep Memory Retrieval, from MemGPT)](https://arxiv.org/abs/2310.08560) | 2023-10 |  |  |  |  |  |  | ✓ | `conversational_longterm`, `personalization` |
| [StreamBench](https://arxiv.org/abs/2406.08747) | 2024-06 |  |  |  |  | ✓ |  |  | `procedural_workflow` |
| [TeaFarm (THEANINE)](https://aclanthology.org/2025.naacl-long.435) | 2024-06 |  |  |  |  | ✓ |  |  | `conversational_longterm` |
| [GoodAI LTM Benchmark](https://arxiv.org/abs/2409.20222) | 2024-09 |  |  | ✓ |  |  |  |  | `conversational_longterm`, `semantic_knowledge_update` |
| [MemDaily (MemSim)](https://arxiv.org/abs/2409.20163) | 2024-09 |  |  |  |  | ✓ |  |  | `personalization`, `conversational_longterm` |
| [Episodic Memory Benchmark](https://arxiv.org/abs/2501.13121) | 2025-01 |  |  |  |  | ✓ |  |  | `episodic`, `semantic_knowledge_update`, `parametric` |
| [PersonaBench](https://aclanthology.org/2025.findings-acl.49) | 2025-02 |  |  |  |  | ✓ |  |  | `personalization` |
| [PrefEval](https://arxiv.org/abs/2502.09597) | 2025-02 |  |  |  |  | ✓ |  |  | `personalization`, `conversational_longterm` |
| [REALTALK](https://arxiv.org/abs/2502.13270) | 2025-02 |  |  | ✓ |  |  |  |  | `conversational_longterm`, `episodic` |
| [TReMu](https://arxiv.org/abs/2502.01630) | 2025-02 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `episodic` |
| [ImplexConv](https://aclanthology.org/2025.emnlp-main.580) | 2025-03 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization` |
| [MEMENTO](https://arxiv.org/abs/2505.16348) | 2025-05 |  |  |  |  | ✓ |  |  | `personalization`, `episodic`, `embodied` |
| [MS-TOD (MemGuide)](https://arxiv.org/abs/2505.20231) | 2025-05 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization` |
| [LOCCO](https://aclanthology.org/2025.findings-acl.1014) | 2025-07 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `parametric` |
| [M3-Bench (M3-Agent)](https://arxiv.org/abs/2508.09736) | 2025-08 |  |  |  |  | ✓ |  |  | `episodic`, `multimodal` |
| [MPR](https://arxiv.org/abs/2508.13250) | 2025-08 |  |  |  |  | ✓ |  |  | `personalization`, `parametric` |
| [OdysseyBench](https://arxiv.org/abs/2508.09124) | 2025-08 |  |  |  | ✓ |  |  |  | `conversational_longterm` |
| [StuLife](https://arxiv.org/abs/2508.19005) | 2025-08 |  |  | ✓ |  |  |  |  | `episodic`, `semantic_knowledge_update`, `procedural_workflow` |
| [FlashAdventure](https://aclanthology.org/2025.emnlp-main.1192) | 2025-09 |  |  |  |  | ✓ |  |  | `episodic`, `multimodal` |
| [MemTrack](https://arxiv.org/abs/2510.01353) | 2025-10 |  |  |  |  |  |  | ✓ | `semantic_knowledge_update`, `episodic` |
| [TeleEgo](https://arxiv.org/abs/2510.23981) | 2025-10 |  |  |  | ✓ |  |  |  | `episodic`, `multimodal` |
| [AndroidIntent (PersonalAlign)](https://arxiv.org/abs/2601.09636) | 2026-01 |  |  |  |  | ✓ |  |  | `personalization` |
| [CAME-Bench](https://arxiv.org/abs/2601.10702) | 2026-01 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update` |
| [EvolMem](https://arxiv.org/abs/2601.03543) | 2026-01 |  |  |  |  | ✓ |  |  | `conversational_longterm` |
| [Mem-Gallery](https://arxiv.org/abs/2601.03515) | 2026-01 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update`, `episodic`, `multimodal` |
| [MemoryRewardBench](https://arxiv.org/abs/2601.11969) | 2026-01 |  |  |  |  | ✓ |  |  | `conversational_longterm` |
| [RPEval](https://arxiv.org/abs/2601.16621) | 2026-01 |  |  |  |  | ✓ |  |  | `personalization` |
| [AMA-Bench](https://arxiv.org/abs/2602.22769) | 2026-02 |  |  |  |  | ✓ |  |  | `episodic`, `semantic_knowledge_update` |
| [ES-MemEval](https://arxiv.org/abs/2602.01885) （已入库） | 2026-02 | ✓ |  |  |  |  |  |  | `conversational_longterm`, `personalization`, `semantic_knowledge_update`, `episodic` |
| [MemEmo (HLME)](https://arxiv.org/abs/2602.23944) | 2026-02 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update` |
| [Neuromem](https://arxiv.org/abs/2602.13967) | 2026-02 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update` |
| [PersistBench](https://arxiv.org/abs/2602.01146) | 2026-02 |  |  |  |  | ✓ |  |  | `personalization` |
| [AMB (Agent Memory Benchmark)](https://github.com/vectorize-io/agent-memory-benchmark) | 2026-03 |  |  |  | ✓ |  |  |  | `conversational_longterm`, `personalization`, `semantic_knowledge_update`, `coding_cross_session` |
| [LifeBench](https://arxiv.org/abs/2603.03781) | 2026-03 |  |  |  |  | ✓ |  |  | `personalization`, `episodic`, `semantic_knowledge_update` |
| [Persona-MME](https://arxiv.org/abs/2604.13074) | 2026-03 |  |  |  | ✓ |  |  |  | `personalization`, `conversational_longterm`, `semantic_knowledge_update`, `multimodal` |
| [RealPref](https://arxiv.org/abs/2603.04191) | 2026-03 |  |  |  |  | ✓ |  |  | `personalization`, `conversational_longterm` |
| [RMBench](https://arxiv.org/abs/2603.01229) | 2026-03 |  |  |  | ✓ |  |  |  | `embodied` |
| [LoCoMo-Refined](https://github.com/mem-eval-suite/LoCoMo_refined) | 2026-04 |  |  |  | ✓ |  |  |  | `conversational_longterm`, `episodic` |
| [MemHome / MemHomeLife](https://arxiv.org/abs/2604.10110) | 2026-04 |  |  |  |  | ✓ |  |  | `personalization`, `semantic_knowledge_update`, `conversational_longterm` |
| [StratMem-Bench](https://arxiv.org/abs/2604.26243) | 2026-04 |  |  |  |  | ✓ |  |  | `conversational_longterm` |
| [EgoStream](https://arxiv.org/abs/2605.31557) | 2026-05 |  |  |  |  | ✓ |  |  | `episodic`, `multimodal` |
| [GroupMemBench](https://arxiv.org/abs/2605.14498) （已入库） | 2026-05 | ✓ |  |  |  |  |  |  | `multi_agent_group`, `conversational_longterm`, `semantic_knowledge_update` |
| [LongMemEval-V2](https://arxiv.org/abs/2605.12493) | 2026-05 |  |  |  |  |  |  | ✓ | `episodic`, `procedural_workflow` |
| [MBench](https://arxiv.org/abs/2606.00793) | 2026-05 |  |  |  | ✓ |  |  |  | `multimodal` |
| [MEMAUDIT](https://arxiv.org/abs/2605.02199) | 2026-05 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update` |
| [MemEye](https://arxiv.org/abs/2605.15128) | 2026-05 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update`, `multimodal` |
| [Momento](https://arxiv.org/abs/2606.00832) | 2026-05 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization`, `semantic_knowledge_update` |
| [PrecisionMemBench](https://arxiv.org/abs/2605.11325) | 2026-05 |  |  | ✓ |  |  |  |  | `semantic_knowledge_update` |
| [RefMem-Bench](https://arxiv.org/abs/2606.01223) | 2026-05 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization`, `multimodal` |
| [RoboMemArena](https://arxiv.org/abs/2605.10921) | 2026-05 |  |  |  | ✓ |  |  |  | `embodied` |
| [STALE](https://arxiv.org/abs/2605.06527) | 2026-05 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update`, `conversational_longterm`, `personalization` |
| [STATE-Bench](https://github.com/microsoft/STATE-Bench) | 2026-05 |  |  |  |  |  |  | ✓ | `procedural_workflow` |
| [SuperMemory-VQA](https://arxiv.org/abs/2606.00825) | 2026-05 |  |  |  |  | ✓ |  |  | `episodic`, `multimodal` |
| [WorldMemArena](https://arxiv.org/abs/2605.29341) | 2026-05 |  |  |  |  | ✓ |  |  | `episodic`, `semantic_knowledge_update`, `personalization`, `conversational_longterm`, `multimodal`, `embodied` |
| [DMV-Bench](https://arxiv.org/abs/2606.27499) | 2026-06 |  |  |  |  | ✓ |  |  | `episodic`, `multimodal` |
| [EvoArena](https://arxiv.org/abs/2606.13681) | 2026-06 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update`, `personalization`, `procedural_workflow` |
| [ForgetEval](https://arxiv.org/abs/2606.15903) | 2026-06 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update` |
| [GateMem](https://arxiv.org/abs/2606.18829) | 2026-06 |  |  |  |  | ✓ |  |  | `multi_agent_group`, `semantic_knowledge_update`, `conversational_longterm`, `memory_security` |
| [H2HMem](https://arxiv.org/abs/2606.09461) | 2026-06 |  |  |  |  | ✓ |  |  | `multi_agent_group`, `conversational_longterm`, `multimodal` |
| [HUSH-Bench](https://arxiv.org/abs/2606.06055) | 2026-06 |  |  |  |  | ✓ |  |  | `memory_security` |
| [MemoryDocDataSet](https://arxiv.org/abs/2606.04442) | 2026-06 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `multi_agent_group` |
| [MEMPROBE (MemAudit)](https://arxiv.org/abs/2606.24595) | 2026-06 |  |  |  |  | ✓ |  |  | `personalization`, `conversational_longterm` |
| [MemTrace](https://arxiv.org/abs/2606.17328) | 2026-06 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization`, `semantic_knowledge_update` |
| [MIST](https://arxiv.org/abs/2606.10949) | 2026-06 |  |  |  |  | ✓ |  |  | `conversational_longterm` |
| [MPBench](https://arxiv.org/abs/2606.04329) | 2026-06 |  |  |  |  | ✓ |  |  | `memory_security` |
| [OmniMemEval](https://github.com/MemTensor/OmniMemEval) | 2026-06 |  |  |  | ✓ |  |  |  | `conversational_longterm`, `personalization`, `semantic_knowledge_update`, `procedural_workflow`, `coding_cross_session` |
| [SEAGym](https://arxiv.org/abs/2606.17546) | 2026-06 |  |  |  | ✓ |  |  |  | `procedural_workflow` |
| [SubtleMemory](https://arxiv.org/abs/2606.05761) | 2026-06 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update`, `personalization` |
| [Agent Memory Leaderboard (AML)](https://github.com/AML-memory/agent-memory-leaderboard) | 2026-07 |  |  |  | ✓ |  |  |  | `conversational_longterm`, `personalization`, `semantic_knowledge_update`, `episodic`, `procedural_workflow`, `coding_cross_session`, `memory_security` |
| [Agent-Memory Integrity Benchmark](https://github.com/DanceNitra/agent-memory-integrity) | 2026-07 |  |  |  | ✓ |  |  |  | `semantic_knowledge_update` |
| [AgenticSTS](https://arxiv.org/abs/2607.02255) | 2026-07 |  |  |  |  | ✓ |  |  | `episodic`, `procedural_workflow` |
| [Bad Memory](https://arxiv.org/abs/2607.14611) | 2026-07 |  |  |  |  | ✓ |  |  | `memory_security` |
| [Ground Truth First (Veracium)](https://arxiv.org/abs/2607.21962) | 2026-07 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization`, `semantic_knowledge_update`, `episodic`, `memory_security` |
| [InMind](https://arxiv.org/abs/2607.24368) | 2026-07 |  |  |  |  | ✓ |  |  | `personalization`, `conversational_longterm` |
| [MemOps](https://arxiv.org/abs/2607.12893) | 2026-07 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update`, `parametric` |
| [MemSecBench](https://arxiv.org/abs/2607.27080) | 2026-07 |  |  |  |  | ✓ |  |  | `memory_security` |
| [MemSyco-Bench](https://arxiv.org/abs/2607.01071) | 2026-07 |  |  |  |  | ✓ |  |  | `personalization`, `semantic_knowledge_update` |
| [MERIT](https://arxiv.org/abs/2609.05441) | 2026-07 |  |  |  |  | ✓ |  |  | `episodic`, `semantic_knowledge_update`, `personalization` |
| [PM-Bench](https://arxiv.org/abs/2607.12385) | 2026-07 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update` |
| [RECON](https://arxiv.org/abs/2607.16716) | 2026-07 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update`, `episodic` |
| [RUMBA](https://arxiv.org/abs/2607.21447) | 2026-07 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `episodic`, `semantic_knowledge_update` |
| [Sequential EQA](https://arxiv.org/abs/2607.21571) | 2026-07 |  |  |  |  | ✓ |  |  | `episodic`, `multimodal`, `embodied` |
| [SLVMBench](https://arxiv.org/abs/2607.11312) | 2026-07 |  |  |  |  | ✓ |  |  | `procedural_workflow`, `multimodal` |
| [agent-memory-bench](https://github.com/GiulioDER/agent-memory-bench) | 2026-08 |  |  |  | ✓ |  |  |  | `semantic_knowledge_update`, `coding_cross_session` |
| [DreamBench-SWE](https://arxiv.org/abs/2608.20664) | 2026-08 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update`, `procedural_workflow`, `coding_cross_session` |
| [ECCBench](https://arxiv.org/abs/2609.00103) | 2026-08 |  |  |  |  | ✓ |  |  | `multimodal` |
| [Harness the Memory](https://arxiv.org/abs/2608.15008) | 2026-08 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update`, `parametric` |
| [MemToC](https://arxiv.org/abs/2608.26295) | 2026-08 |  |  |  |  | ✓ |  |  | — |
| [MemTrapBench](https://arxiv.org/abs/2608.20202) | 2026-08 |  |  |  |  | ✓ |  |  | `memory_security` |
| [MemUse](https://arxiv.org/abs/2608.24189) | 2026-08 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization` |
| [MobileMem](https://arxiv.org/abs/2608.13606) | 2026-08 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization`, `episodic`, `semantic_knowledge_update`, `multimodal` |
| [SCALE-QA](https://arxiv.org/abs/2608.25655) | 2026-08 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update` |
| [StateMemBench](https://arxiv.org/abs/2608.19652) | 2026-08 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update` |
| [TANGLE](https://arxiv.org/abs/2608.13921) | 2026-08 |  |  |  |  | ✓ |  |  | `personalization`, `conversational_longterm`, `semantic_knowledge_update` |
| [UtilMem](https://arxiv.org/abs/2608.30508) | 2026-08 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization` |
| [APM-Bench](https://arxiv.org/abs/2609.37559) | 2026-09 |  |  |  |  | ✓ |  |  | `episodic`, `semantic_knowledge_update`, `multimodal` |
| [CapMem](https://arxiv.org/abs/2609.17688) | 2026-09 |  |  |  |  | ✓ |  |  | `episodic`, `multimodal` |
| [CICM](https://arxiv.org/abs/2609.38866) | 2026-09 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update` |
| [CoMemBench](https://arxiv.org/abs/2609.32192) | 2026-09 |  |  |  |  | ✓ |  |  | `multi_agent_group` |
| [ConsolidationBench](https://arxiv.org/abs/2609.33013) | 2026-09 |  |  |  |  | ✓ |  |  | `procedural_workflow` |
| [CPB (Correlated Promotion Benchmark)](https://arxiv.org/abs/2609.30813) | 2026-09 |  |  |  |  | ✓ |  |  | `multi_agent_group`, `memory_security` |
| [Cross-Lingual Unlearning Tensor](https://arxiv.org/abs/2609.40286) | 2026-09 |  |  |  |  | ✓ |  |  | `parametric` |
| [CUE-Mem](https://arxiv.org/abs/2609.32574) | 2026-09 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization`, `multimodal` |
| [DolphinBench](https://arxiv.org/abs/2609.24971) | 2026-09 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization` |
| [EconSkills](https://arxiv.org/abs/2609.19523) | 2026-09 |  |  |  |  | ✓ |  |  | `procedural_workflow` |
| [ICM-Bench](https://arxiv.org/abs/2609.04438) | 2026-09 |  |  |  |  | ✓ |  |  | `episodic`, `multimodal` |
| [IDUnlearn-Bench](https://arxiv.org/abs/2609.33481) | 2026-09 |  |  |  |  | ✓ |  |  | `parametric`, `multimodal`, `memory_security` |
| [Impact Is Not Invalidation (claim-invalidation benchmark)](https://arxiv.org/abs/2609.25130) | 2026-09 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update` |
| [LAPSE](https://arxiv.org/abs/2609.36457) | 2026-09 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update` |
| [LOCOMO-CONV](https://arxiv.org/abs/2609.03467) | 2026-09 |  |  |  |  | ✓ |  |  | `conversational_longterm` |
| [LSREP](https://arxiv.org/abs/2609.16730) | 2026-09 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update` |
| [MemCalib](https://arxiv.org/abs/2609.24259) | 2026-09 |  |  |  |  | ✓ |  |  | `personalization` |
| [MemoReason](https://arxiv.org/abs/2609.35312) | 2026-09 |  |  |  |  | ✓ |  |  | — |
| [MemProbe](https://arxiv.org/abs/2609.30558) | 2026-09 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update`, `personalization` |
| [MemRiskBench](https://arxiv.org/abs/2609.14976) | 2026-09 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update`, `memory_security` |
| [MemTransfer](https://arxiv.org/abs/2609.32313) | 2026-09 |  |  |  |  | ✓ |  |  | `episodic`, `embodied` |
| [PairPref](https://arxiv.org/abs/2609.34526) | 2026-09 |  |  |  |  | ✓ |  |  | `personalization` |
| [PRAGMA](https://arxiv.org/abs/2609.09664) | 2026-09 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization`, `semantic_knowledge_update` |
| [SimLife-BP](https://arxiv.org/abs/2609.19610) | 2026-09 |  |  |  |  | ✓ |  |  | `personalization`, `semantic_knowledge_update`, `multimodal`, `embodied` |
| [TWIST](https://arxiv.org/abs/2609.28575) | 2026-09 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `semantic_knowledge_update`, `memory_security` |
| [VibeMemBench](https://arxiv.org/abs/2609.23570) | 2026-09 |  |  |  |  | ✓ |  |  | `procedural_workflow`, `coding_cross_session` |
| [Video2Skill](https://arxiv.org/abs/2609.36691) | 2026-09 |  |  |  |  | ✓ |  |  | `multimodal`, `embodied` |
| [What Should an Agent Remember? (bounded-memory streaming-recall benchmark)](https://arxiv.org/abs/2610.00366) | 2026-09 |  |  |  |  | ✓ |  |  | — |
| [CMSC-E (Memory Canonicalization)](https://arxiv.org/abs/2610.05124) | 2026-10 |  |  |  |  | ✓ |  |  | — |
| [DyadMem](https://arxiv.org/abs/2610.03020) | 2026-10 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization`, `episodic`, `semantic_knowledge_update` |
| [EMBER-Bench](https://arxiv.org/abs/2610.05013) | 2026-10 |  |  |  |  | ✓ |  |  | `episodic`, `multimodal`, `embodied` |
| [Knowing the Store](https://arxiv.org/abs/2610.04794) | 2026-10 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update` |
| [MetaKernelBench](https://arxiv.org/abs/2610.05014) | 2026-10 |  |  |  |  | ✓ |  |  | `procedural_workflow`, `coding_cross_session` |
| [MLE-InsightBench](https://arxiv.org/abs/2610.04927) | 2026-10 |  |  |  |  | ✓ |  |  | `procedural_workflow` |
| [RealCompanion](https://arxiv.org/abs/2610.01780) | 2026-10 |  |  |  |  | ✓ |  |  | `conversational_longterm`, `personalization` |

### 被列为记忆评测资源的通用 benchmark（51 个，不作为本库候选）

这些 benchmark 并非为记忆设计（多跳问答、单次长输入的长上下文测试、网页导航等），列表把它们当作记忆系统的评测基底收录。

| Benchmark | 首次公开 | WEN6 | WEN6 fork 分支 | Tsinghua | TeleAI | IAAR | topoteretes | Cognee | 记忆类型 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [LongBench](https://arxiv.org/abs/2308.14508) | 2023-08 |  |  |  | ✓ | ✓ |  | ✓ | — |
| [LongBench v2](https://arxiv.org/abs/2412.15204) | 2024-12 |  |  |  | ✓ | ✓ |  | ✓ | `conversational_longterm`, `multi_agent_group` |
| [HotpotQA](https://arxiv.org/abs/1809.09600) | 2018-09 |  |  |  |  | ✓ |  | ✓ | — |
| [InfiniteBench (∞Bench)](https://arxiv.org/abs/2402.13718) | 2024-02 |  |  |  | ✓ |  |  | ✓ | — |
| [RULER](https://arxiv.org/abs/2404.06654) | 2024-04 |  |  |  |  | ✓ |  | ✓ | — |
| [BABILong](https://arxiv.org/abs/2406.10149) | 2024-06 |  |  |  |  | ✓ |  | ✓ | — |
| [NoLiMa](https://arxiv.org/abs/2502.05167) | 2025-02 |  |  |  | ✓ |  |  | ✓ | — |
| [WebChoreArena](https://arxiv.org/abs/2506.01952) | 2025-06 |  |  | ✓ |  | ✓ |  |  | — |
| [AgentLongBench](https://arxiv.org/abs/2601.20730) | 2026-01 |  |  |  |  | ✓ |  | ✓ | `episodic`, `semantic_knowledge_update` |
| [2WikiMultiHopQA](https://arxiv.org/abs/2011.01060) | 2020-11 |  |  |  |  |  |  | ✓ | — |
| [MuSiQue](https://arxiv.org/abs/2108.00573) | 2021-08 |  |  |  |  |  |  | ✓ | — |
| [WebShop](https://arxiv.org/abs/2207.01206) | 2022-07 |  |  |  |  | ✓ |  |  | — |
| [LaMP](https://aclanthology.org/2024.acl-long.399) | 2023-04 |  |  |  |  | ✓ |  |  | `personalization` |
| [L-Eval](https://arxiv.org/abs/2307.11088) | 2023-07 |  |  |  |  |  |  | ✓ | — |
| [WebArena](https://arxiv.org/abs/2307.13854) | 2023-07 |  |  |  |  | ✓ |  |  | — |
| [EgoSchema](https://proceedings.neurips.cc/paper_files/paper/2023/file/90ce332aff156b910b002ce4e6880dec-paper-datasets_and_benchmarks) | 2023-08 |  |  |  | ✓ |  |  |  | `multimodal` |
| [StoryBench](https://proceedings.neurips.cc/paper_files/paper/2023/hash/f63f5fbed1a4ef08c857c5f377b5d33a-abstract-datasets_and_benchmarks.html) | 2023-08 |  |  |  | ✓ |  |  |  | `multimodal` |
| [LooGLE](https://aclanthology.org/2024.acl-long.859) | 2023-11 |  |  |  |  | ✓ |  |  | — |
| [Needle in a Haystack (NIAH)](https://github.com/gkamradt/LLMTest_NeedleInAHaystack) | 2023-11 |  |  |  |  |  |  | ✓ | — |
| [LvBench (MoVQA)](https://arxiv.org/abs/2312.04817) | 2023-12 |  |  |  | ✓ |  |  |  | `multimodal` |
| [MT-Eval](https://aclanthology.org/2024.emnlp-main.1124) | 2024-01 |  |  |  |  | ✓ |  |  | — |
| [MT-Mind2Web](https://arxiv.org/abs/2402.15057) | 2024-02 |  |  |  |  | ✓ |  |  | — |
| [MovieChat+ / MovieChat-1K](https://arxiv.org/abs/2404.17176) | 2024-04 |  |  |  | ✓ |  |  |  | `multimodal` |
| [CinePile](https://arxiv.org/abs/2405.08813) | 2024-05 |  |  |  | ✓ |  |  |  | `multimodal` |
| [Video-MME](https://arxiv.org/abs/2405.21075) | 2024-05 |  |  |  | ✓ |  |  |  | `multimodal` |
| [LVBench](https://arxiv.org/abs/2406.08035) | 2024-06 |  |  |  | ✓ |  |  |  | `multimodal` |
| [MMNeedle (Multimodal Needle in a Haystack)](https://aclanthology.org/2025.naacl-long.166) | 2024-06 |  |  |  |  | ✓ |  |  | `multimodal` |
| [AppWorld](https://arxiv.org/abs/2407.18901) | 2024-07 |  |  |  | ✓ |  |  |  | — |
| [LongVideoBench](https://arxiv.org/abs/2407.15754) | 2024-07 |  |  |  | ✓ |  |  |  | `multimodal` |
| [LongGenBench](https://arxiv.org/abs/2409.02076) | 2024-09 |  |  |  |  | ✓ |  |  | — |
| [Michelangelo](https://arxiv.org/abs/2409.12640) | 2024-09 |  |  |  |  |  |  | ✓ | — |
| [L-CiteEval](https://arxiv.org/abs/2410.02115) | 2024-10 |  |  |  |  | ✓ |  |  | — |
| [LongGenBench](https://aclanthology.org/2024.findings-emnlp.48) | 2024-10 |  |  |  |  | ✓ |  |  | — |
| [Muse](https://arxiv.org/abs/2412.18416) | 2024-12 |  |  |  |  | ✓ |  |  | `personalization`, `multimodal` |
| [SCBench](https://arxiv.org/abs/2412.10319) | 2024-12 |  |  |  |  | ✓ |  |  | — |
| Graphwalks | 2025-04 |  |  |  |  |  |  | ✓ | — |
| OpenAI MRCR | 2025-04 |  |  |  |  |  |  | ✓ | — |
| [MiniLongBench](https://aclanthology.org/2025.acl-long.560) | 2025-05 |  |  |  |  | ✓ |  |  | — |
| [AbsenceBench](https://arxiv.org/abs/2506.11440) | 2025-06 |  |  |  |  |  |  | ✓ | — |
| [OpenUnlearning](https://arxiv.org/abs/2506.12618) | 2025-06 |  |  |  |  | ✓ |  |  | `parametric` |
| [PersonaFeedback](https://arxiv.org/abs/2506.12915) | 2025-06 |  |  |  |  | ✓ |  |  | `personalization` |
| [Gaia2 (ARE)](https://arxiv.org/abs/2509.17158) | 2025-09 |  |  |  | ✓ |  |  |  | — |
| [LoCoBench-Agent](https://arxiv.org/abs/2511.13998) | 2025-11 |  |  | ✓ |  |  |  |  | — |
| [AgentLAB](https://arxiv.org/abs/2602.16901) | 2026-02 |  |  |  |  | ✓ |  |  | `memory_security` |
| [CL-bench](https://arxiv.org/abs/2602.03587) | 2026-02 |  |  |  | ✓ |  |  |  | — |
| [DISBench (DeepImageSearch)](https://arxiv.org/abs/2602.10809) | 2026-02 |  |  |  | ✓ |  |  |  | `episodic`, `multimodal` |
| [KnowU-Bench](https://arxiv.org/abs/2604.08455) | 2026-04 |  |  |  |  | ✓ |  |  | `personalization` |
| [OmniBehavior](https://arxiv.org/abs/2604.08362) | 2026-04 |  |  |  |  | ✓ |  |  | `personalization` |
| [LegalWorld / LongJud-Bench](https://arxiv.org/abs/2606.18728) | 2026-06 |  |  |  |  | ✓ |  |  | — |
| [PrivDrift](https://arxiv.org/abs/2609.30094) | 2026-09 |  |  |  |  | ✓ |  |  | `memory_security` |
| [Ego2World](https://arxiv.org/abs/2610.02715) | 2026-10 |  |  |  |  | ✓ |  |  | `semantic_knowledge_update`, `embodied` |

<details><summary>列表中收录、但核对后不是 benchmark 的条目（63 个）</summary>

| 条目 | 来源 | 判定理由 |
| --- | --- | --- |
| [DMAS LTM cost-accuracy testbed (dmas-memory)](https://arxiv.org/abs/2601.07978) | TeleAI, IAAR | Empirical comparison study (mem0, Graphiti, cognee, RAG, full-context) in a simulated cloud-edge setup. It adds no new dataset or questions and evaluates only on LoCoMo categories 1-4. The repo README says 'The benchmark |
| [Anatomy of Agentic Memory](https://arxiv.org/abs/2602.19320) | TeleAI, IAAR | A survey with taxonomy and empirical analysis of the limits of existing benchmarks and systems. It introduces no new benchmark or dataset. |
| [HOMER](https://arxiv.org/abs/2404.10308) | IAAR | Training-free method (hierarchical context merging) for extending LLM context. It contributes no benchmark or dataset. IAAR lists it under Long-Context Evaluation / Datasets & Benchmark, but the paper is a method paper. |
| [Unlearning with Control (UWC)](https://arxiv.org/abs/2406.09179) | IAAR | Evaluation-methodology paper for LLM unlearning: it picks a robust metric (Extraction Strength) and adds model-mixing calibration. Experiments use only the existing TOFU benchmark, and no new dataset is released. It rela |
| [EM-LLM](https://arxiv.org/abs/2407.09450) | IAAR | Method paper: an episodic-memory-inspired architecture for long or infinite context. It is evaluated on the existing LongBench and InfiniteBench, and introduces no benchmark. |
| [AgenticLU](https://arxiv.org/abs/2502.15920) | IAAR | A method paper (Chain-of-Clarifications, SFT plus DPO) for long-context understanding. It evaluates on existing long-context tasks such as NarrativeQA and releases no new benchmark. IAAR lists it under Datasets & Benchma |
| [MEXTRA](https://aclanthology.org/2025.acl-long.1227) | IAAR | An attack paper (arXiv 2502.13172). It proposes the Memory EXTRaction Attack against the memory of LLM agents and tests it on two agents (EHRAgent, RAP). It does not release a reusable benchmark or dataset as a main cont |
| [USP (User Simulator with Implicit Profiles)](https://aclanthology.org/2025.acl-long.1025) | IAAR | A method paper (arXiv 2502.18968). It proposes a user simulator that extracts implicit profiles and is trained with conditional SFT and reinforcement learning. It does not contribute a memory benchmark or dataset as a ma |
| [MIRIX](https://arxiv.org/abs/2507.07957) | IAAR | A memory-system paper. It introduces ScreenshotVQA, collected from three PhD students' screen activity, but the dataset does not appear to be released: the paper gives no dataset URL, and the public_evaluation branch con |
| [Evaluating Long-Term Memory for Long-Context QA](https://arxiv.org/abs/2510.23730) | TeleAI | Systematic evaluation study of memory-augmented methods (RAG, agentic, episodic via reflections, procedural via prompt optimization) on existing datasets LoCoMo and QMSum; releases no new benchmark or dataset and no code |
| [ReMe](https://arxiv.org/abs/2512.10696) | IAAR | Procedural-memory method/framework (distillation, reuse, refinement of experience pool) evaluated on existing benchmarks BFCL-V3 and AppWorld; the released reme.library is an experience library, not an evaluation benchma |
| Survey on AI Memory | TeleAI | A survey paper that proposes a '4W Memory Taxonomy' and reviews memory systems and evaluation. The official repo (BAI-LAB/Survey-on-AI-Memory) hosts the PDF; no arXiv ID was found and the README's arXiv badge is still a  |
| [Panini](https://arxiv.org/abs/2602.15156) | IAAR | A method paper: non-parametric continual learning via Generative Semantic Workspaces, evaluated on six existing QA benchmarks. It contributes no reusable benchmark or dataset. |
| [Personalized LLM-Powered Agents survey](https://arxiv.org/abs/2602.22680) | IAAR | A survey of personalized agents (profile modeling, memory, planning, action), including a review of evaluation methods. It introduces no benchmark. |
| [Zombie Agents](https://arxiv.org/abs/2602.15654) | IAAR | An attack paper: persistent memory-injection attack on self-evolving agents, evaluated on representative setups. It contributes no reusable benchmark or dataset. |
| [Dakera](https://github.com/dakera-ai/dakera-mcp) | Tsinghua | Self-hosted MCP memory server product. It only reports its own LoCoMo score; there is no benchmark contribution. |
| [Memory for Autonomous LLM Agents (survey)](https://arxiv.org/abs/2603.07670) | TeleAI | Survey of agent memory mechanisms and evaluation; it introduces no benchmark or dataset. |
| [Multi-Layer Memory Framework (MLMF)](https://arxiv.org/abs/2603.29194) | IAAR | Method paper proposing a multi-layer memory architecture, evaluated on existing benchmarks (LoCoMo, LOCCO). |
| [Memory in the LLM Era (unified framework)](https://arxiv.org/abs/2604.01707) | IAAR | Unified framework and empirical comparison of memory methods on existing conversational and agentic benchmarks, plus a new method; no new benchmark or dataset. IAAR lists it under Datasets & Benchmark anyway. |
| [Agent Memory Techniques](https://github.com/NirDiamant/Agent_Memory_Techniques) | Tsinghua | Tutorial collection of 30 runnable Jupyter notebooks on memory techniques. Some notebooks use LoCoMo, but the repo introduces no benchmark of its own. |
| [Agentic Environment Engineering (survey)](https://arxiv.org/abs/2606.12191) | IAAR | A survey of environment modeling, synthesis, evaluation and application for LLM agents. It introduces no benchmark or dataset. |
| [Memory Makes the Difference](https://arxiv.org/abs/2606.25361) | IAAR | An analysis paper that proposes a taxonomy of memory roles and a user-centric LLM-judge framework. Its experiments run on existing datasets (LongMemEval-m, Long-MT-Bench+), with no new benchmark or dataset. IAAR lists it |
| [OpenThoughts-Agent](https://arxiv.org/abs/2606.24855) | IAAR | A data-curation recipe and a 100K-example training set for agentic models, evaluated on seven generic agentic benchmarks. It is a training dataset, not a memory evaluation resource. |
| [Toward Secure LLM Agents (survey)](https://arxiv.org/abs/2606.10749) | IAAR | A survey synthesizing 247 papers on LLM agent security. It releases no benchmark or dataset. |
| [GemmaSV (Auditable Deletion)](https://arxiv.org/abs/2607.27539) | IAAR | Method plus audit study: installs a support-vector gate in frozen Gemma 3 and audits deletion of exchange-linked key/value rows. It uses existing benchmarks (TOFU, LongMemEval) as test material and introduces no new benc |
| [Hindsight Memory-PRM](https://arxiv.org/abs/2608.29605) | IAAR | Method paper (process reward model / critic for memory-management operations), evaluated on existing LoCoMo and LongMemEval. No new benchmark or dataset. |
| [MAFIA](https://arxiv.org/abs/2608.03844) | IAAR | Attack-framework paper (query-only memory poisoning against audited agent memory). No reusable benchmark or dataset is presented as a main contribution. |
| [Measure Before You Manage](https://arxiv.org/abs/2608.31057) | IAAR | Empirical/analysis study of task-local working memory using 55 archived SWE-bench Lite coding-agent trajectories. The paper states no public release is claimed. Memory management happens only within a single task run (25 |
| [When Memory Lies](https://arxiv.org/abs/2608.04574) | IAAR | Self-described empirical study of spatial-memory staleness on a dynamic FrozenLake testbed. The testbed is an experimental instrument, and no release of testbed, code or data was found on the arXiv page. |
| [Wontopos tablet-2](https://arxiv.org/abs/2608.23920) | IAAR | System evaluation report of a closed-source production memory engine on existing benchmarks (LongMemEval-S, BEAM-1M, Crossmodal-3600). It releases a harness and per-question records but introduces no new benchmark as its |
| [After the Fix](https://arxiv.org/abs/2609.34603) | IAAR | Empirical study (3,300 runs) of whether repaired agent experience (Full/Skill/Hybrid handoffs) transfers to a related target task, using existing ThinkingBox and APEX-Agents benchmarks (business/professional workflows, n |
| [Auditing Long-Term Memory Evaluation (LongMemEval-S retrieval chain)](https://arxiv.org/abs/2609.38021) | IAAR | An evaluation-audit report on a retrieval-chain method using the existing LongMemEval-S (and LoCoMo). The arXiv title differs from the list title. Ancillary data supports only recounting; no new benchmark is released. |
| [Delayed Supervision for Test-Time LMs](https://arxiv.org/abs/2609.32312) | IAAR | Training-method paper (delayed QA supervision for test-time-memory models LaCT/DeltaNet/RWKV-7), evaluated on existing BABILong and RULER; no new benchmark. |
| [DerivAudit](https://arxiv.org/abs/2609.36130) | IAAR | An audit framework and analysis of whether written memories are supported by history. It reuses LoCoMo and HaluMem-Medium (400 memory writes) and releases no named benchmark or dataset. No code link is given. |
| [FAME](https://arxiv.org/abs/2609.39473) | IAAR | A training-free method for detecting false memory from hidden states, scored by AUROC against baselines. It releases counterfactual templates built on GSM-Symbolic, GitChameleon and BBH, but these support the method rath |
| [Graph-Based Personalized Memory survey](https://arxiv.org/abs/2609.08599) | IAAR | Self-described survey ('This survey develops a lifecycle-oriented view of graph-based personalized memory'); no benchmark or dataset contributed. |
| [In-Context Binding Capacity](https://arxiv.org/abs/2609.30634) | IAAR | Analysis/measurement paper fitting scaling laws to recall of in-context entity-obligation bindings using a synthetic probe; paper (HTML) releases recall curves but no named benchmark or dataset as a main contribution. |
| [MemDream](https://arxiv.org/abs/2609.34545) | IAAR | Method paper (self-probing memory evolution with offline dream cycles and a GRPO-trained repair policy), evaluated on existing LoCoMo and MemoryAgentBench. |
| [Memory Misalignment in Human-LLM Interaction](https://arxiv.org/abs/2609.33623) | IAAR | HCI mixed-methods study (usage logs, diary study, co-design workshops, speed dating) producing a taxonomy of memory misalignment and design space; no benchmark or dataset as main contribution. |
| [Memory Portability](https://arxiv.org/abs/2609.05339) | IAAR | Self-described controlled study of memory portability across model/embedding upgrades, using 48 synthetic histories with 160 questions each. The histories are 'available upon request' and not presented as a reusable benc |
| [Memory vs. Context replication](https://arxiv.org/abs/2609.24238) | IAAR | Reproducibility study of Yu et al. (2023) on parametric-vs-context knowledge conflict across 31 models, reusing world-capitals probes and the existing ParaConflict dataset; no new benchmark contributed. |
| [MT fine-tuning forgetting mitigation study](https://arxiv.org/abs/2609.28395) | IAAR | Analysis study comparing catastrophic-forgetting mitigation methods (EWC, data mixing) for MT fine-tuning on existing benchmarks; no benchmark or dataset contribution. |
| [Price of Safety (memory-poisoning defense overhead)](https://arxiv.org/abs/2609.22818) | IAAR | Measurement study of benign-case cost of memory-poisoning defenses over five conversations with a fixed backend; no reusable benchmark/dataset contributed. |
| [ProTTT](https://arxiv.org/abs/2609.32564) | IAAR | Method paper: meta-learned test-time-training user memory for personalization, evaluated on existing benchmarks; no new benchmark. |
| [ReplayLens](https://arxiv.org/abs/2609.34177) | IAAR | Black-box audit methodology (four interventions on stored outcome history) for how agents use logged experience; applied to model selection, experiment planning and a code-debugging agent, but no reusable benchmark/datas |
| [RoutePrism](https://arxiv.org/abs/2609.34160) | IAAR | Diagnostic protocol that rebuilds memory in two processing orders and traces differences; evaluated on existing PersonaMem-32K and LongMemEval-S. No new benchmark/dataset. |
| [SCLATE](https://arxiv.org/abs/2609.32391) | IAAR | Paper presents SCLATE as infrastructure ('an execution substrate') that schedules multi-session events for existing benchmarks (MetaClaw, GAIA-2, AppWorld, LongMemEval, PersonaMem, SWE-Gym, SWE-bench Verified); no new be |
| [Selection vs Extraction (Jev/Engram)](https://arxiv.org/abs/2609.34227) | IAAR | Pre-registered empirical comparison of raw-turn selection vs LLM-extracted memory on existing LoCoMo and LongMemEval; no new benchmark. |
| [Separating Memory and Workflow Effects (OwnWords)](https://arxiv.org/abs/2609.33321) | IAAR | Empirical study of memory construction vs answer workflow for predicting a person's interview answers; its 1,768-task 'private benchmark' stays in restricted storage and is not listed as a contribution; also uses existin |
| [Share-Borne AI Virus](https://arxiv.org/abs/2609.35576) | IAAR | A threat/attack study of artifact-mediated propagation through persistent memory. It evaluates on 36 synthetic human-agent universes that are not named or framed as a reusable benchmark. Attack templates are mostly withh |
| [TAGGRAPH](https://arxiv.org/abs/2609.38353) | IAAR | A controlled evaluation framework plus a graph-retrieval method (AdaptiveGraph/TagGraph). It reuses LongMemEval-S and ATANT and releases no new benchmark. Code is promised but not linked. |
| [TRIAGE](https://arxiv.org/abs/2609.32103) | IAAR | Self-described 'benchmark-agnostic evaluation framework' (Fisher/Hessian-diagonal metrics plus Forget/Adjacent-Retain/Generic-Retain partition) applied on top of existing unlearning benchmarks WMDP, TOFU, MUSE; paper tex |
| [U-Fuzz](https://arxiv.org/abs/2609.38275) | IAAR | A fuzzing method for memory-use failures. It builds seeds from existing LoCoMo and LongMemEval-S checkpoints and tests Mem0, A-Mem, Graphiti and MemOS. No dataset of failures is released and no code URL is given. |
| [Update Sufficiency Audit (Correct Now, Insufficient Later)](https://arxiv.org/abs/2609.20045) | IAAR | Paper frames its paired-history audit as an evaluation methodology and failure analysis: 'support a scoped evaluation methodology and reproducible failure analysis'; the 24-pair synthetic set is a small development set ( |
| [Where the Evidence Lives (companion self-description audit)](https://arxiv.org/abs/2609.38753) | IAAR | An audit procedure applied to one deployed companion agent (Lita, nine users, one month). It is a case study, not a reusable benchmark or dataset. |
| [Controlled Audit of Personal AI Memory for Rating Prediction](https://arxiv.org/abs/2610.02764) | IAAR | The abstract calls its contribution 'a reproducible diagnostic study'. It uses permutation controls on existing Coat and MovieLens rating data with Mem0 extraction. No new benchmark is introduced. |
| [Cross-Lingual Transferability of TDE Attacks](https://arxiv.org/abs/2610.06093) | IAAR | Attack study of training-data extraction (memorized PII) across languages. The PII dataset is a means to the study and is explicitly not released ('We do not release the underlying dataset itself'); only code is linked.  |
| [MemLeak](https://arxiv.org/abs/2610.04195) | IAAR | Empirical security study and proof of concept of cross-user leakage in shared vector memory. The paper's data is hand-authored fixtures; it names no reusable benchmark and links no code or data (checked arXiv HTML). |
| [Mining Agent Skills from Production Traces](https://arxiv.org/abs/2610.05777) | IAAR | Empirical study of skill-mining configurations (evidence regime x skill form) for procedural skills. It evaluates on the existing enterprise benchmarks ThinkingBox-Bench and APEX-Agents and introduces no new benchmark or |
| [No Hindsight for LLM Fact-Checkers](https://arxiv.org/abs/2610.04888) | IAAR | Analysis of leakage channels (memorized outcomes in pre-training and post-claim retrieved evidence) on the existing fact-checking benchmarks AVeriTeC and QuanTemp++. It is related to parametric memory but releases no new |
| [Self-Propagating Misalignment in LLM Agents](https://arxiv.org/abs/2610.04083) | IAAR | Primarily a threat study of misaligned goals spread through persistent memory or the filesystem, across 20 scenarios in 17 environments with 11 models. The scenarios are released only as a supporting testbed for defenses |
| [StegoMemory](https://arxiv.org/abs/2610.04589) | IAAR | The abstract frames it as 'a large-scale red-teaming exercise' (14,000 trials) on memory as a covert cross-session channel. The arXiv abstract page links no code, data or harness; the HTML version returned 404. |
| [When Evidence Changes (memory repair vs re-reading)](https://arxiv.org/abs/2610.03902) | IAAR | A cost and evaluation analysis of memory repair versus re-reading on eICU demo medication and problem-list tasks. It names no benchmark, and the paper says 'No code or data accompany this preprint'. |

</details>
