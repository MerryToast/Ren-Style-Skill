# Ren-Style-Skill 项目方案 v2

> **目标**：以 Wanbin Ren（任万滨，哈工大电气工程及自动化学院）的 30 篇英文论文为语料，构建一个**可移植的科研写作 Skill**，提供 4 种模式：**风格模仿写作 / 中译英 / 英文润色 / 风格审查**。项目以**公开** GitHub 仓库 `Ren-Style-Skill` 发布。
>
> **v2 更新内容**：依据你的回复，并实际读取了语料目录中 30 个 PDF 的首页，补充了语料清单与权重、留出集划分、PDF 抽取中已发现的问题、电接触领域的章节体系、已观察到的作者风格线索，以及公开仓库的版权策略。

---

## 0. 基本设定（已确认）

| 项 | 值 |
|---|---|
| 语料路径 | `E:\张寅楠\03.个人文件夹\04.实验室论文集\*.pdf`（只处理 PDF，忽略其他文件；共 30 篇，均为英文，年份 2013–2020） |
| 领域 | 电气工程，研究方向为电接触（微动腐蚀、接触电阻、继电器触点熔焊、电弧、连接器可靠性） |
| 学习对象 | 以 Wanbin Ren 为**第一作者**的论文为主；Ren 只担任通讯作者的论文降权，或用作校验 |
| 最高权重 | 01、03、13 三篇（见 §1） |
| 仓库 | 公开仓库，名称 `Ren-Style-Skill` |
| Skill 名称 | 目录名和 frontmatter 中的 `name` 统一用 **`ren-style-skill`**（规范要求小写加连字符）；README 标题和仓库名用 `Ren-Style-Skill` |
| 本机环境 | Python 3.12.8，PyMuPDF 1.28.2，pypdf 6.16，poppler `pdftotext` 均已安装 |

---

## 1. 语料清单与权重分级（依据首页署名整理）

### 分级规则

| 等级 | 含义 | 统计权重 | 用途 |
|---|---|---|---|
| **S** | 你指定的 3 篇核心范文 | **3.0** | 风格档案的锚点；黄金切片优先从这里选；**不能放进留出集** |
| **A** | Ren 为第一作者 | 1.0 | 风格统计主体；切片候选；部分划为留出集 |
| **B** | Ren 只是通讯作者（学生一作） | 0.3 | 只作参考统计和**第二校验集**，不从中挑选切片 |

### 清单

| # | 题目（简） | 期刊/会议 | 年份 | 一作 | 等级 |
|---|---|---|---|---|---|
| 01 | Effects of current load on wear and fretting corrosion of gold-plated electrical contacts | Tribology International | 2013 | Ren | **S** |
| 02 | Role of Sphere Indenter in Measuring Contact Resistance of Flat Rivets | IEICE Trans. Electron. | 2014 | Ren | A |
| 03 | Research on fretting regimes of gold-plated copper alloy … amplitude and frequency combinations | Wear | 2014 | Ren | **S** |
| 04 | Effects of temperature on fretting corrosion behaviors of gold-plated copper alloy contacts | Tribology International | 2014 | Ren | A |
| 05 | Effects of frequency on the intermittent failure phenomena … under fretting conditions | Materials Research Innovations | 2015 | Ren | A |
| 06 | Preliminary Study of Electrical Contact Behaviors of Au-plated Material at Super Low Making/Breaking Velocity | IEICE Trans. Electron. | 2015 | Ren | A |
| 07 | Surface Adhesion Phenomena … at Superlow Making/Breaking Speed | IEEE TCPMT | 2015 | Ren | A |
| 08 | Intermittent Molten Bridge Phenomena … Superlow Opening Speed | IEEE TCPMT | 2016 | Ren | A ⚠ 与 10 高度重复 |
| 09 | Temperature–Voltage Relation … Correction of Kohlrausch's Equation | IEEE TED | 2016 | Ren | A |
| 10 | Formation Process of Intermittent Molten Bridge … Super Low Breaking Velocity | Plasma Sci. Technol. | 2016 | Ren | A ⚠ 与 08 高度重复 |
| 11 | μN level adhesion force characteristics of gold-coated materials in air | J. Adhesion | 2016 | Ren | A |
| 12 | Contact bounce behaviors and dynamic welding phenomena for electromechanical relay | Rev. Sci. Instrum. | 2016 | Ren | A |
| 13 | Electrical Contact Resistance of Coated Spherical Contacts | IEEE TED | 2016 | Ren | **S** |
| 14 | Fretting Behavior … High-Frequency Vibration and Different Temperature | IEEE TCPMT | 2017 | Ren | A |
| 15 | Initial Unstable Electrical Contact Behaviors | IEEE TCPMT | 2017 | Ren | A |
| 16 | Switching Characteristics … Contact Material Under Capacitive Load | IEEE TCPMT | 2018 | Ren | A |
| 17 | Contact a-Spots Features and Electrodynamic Repulsion Force | IEEE TCPMT | 2018 | L. Zhou | B |
| 18 | Effect of Electrical Load on Contact Welding Failure of AgSnO₂ in DC Relays | IEEE Access（开放获取） | 2019 | X. Zhang | B |
| 19 | ECR of connector response to mechanical vibration environment | IEEE TCPMT（录用稿） | 2019 | Ren | A |
| 20 | Contact Sliding Behavior for Flexible Spring Components | IEEE TCPMT | 2019 | C. Zhang | B |
| 21 | Static Contact Behaviors of Rod and Spring for MEMS Relay | IEEE TCPMT | 2019 | C. Zhang | B |
| 22 | Electrical Contact Resistance of Contact Bodies With Cambered Surface | IEEE Access（开放获取） | 2020 | Ren | A |
| 23 | Contact Welding Characteristics of Electromechanical Relays | IEEE TIE（录用稿） | 2020 | X. Zhang（Ren 为通讯作者） | B |
| 24 | Material Welding Characteristics for Low Current Switching Devices | MDPI Materials（开放获取） | 2020 | X. Zhang | B |
| 25 | Contact welding strength measurement … inrush electrical current | Rev. Sci. Instrum. | 2020 | Ren | A |
| 26 | Novel experimental evaluation method of welding characteristics | 会议论文 | — | X. Zhang | B |
| 27 | Improved method … rough surface contact by the elliptical asperity | 会议论文 | — | Ren | A |
| 28 | FEM … Considering Asperity Interactions | 会议论文 | — | C. Zhang | B |
| 29 | Hot Switching Capability … Electrical Connectors | 会议论文 | — | T. Wang | B |
| 30 | AC arc behavior and contact welding failure for general-purpose relay | 会议论文 | — | Z. Zheng | B |

**统计**：S 级 3 篇，A 级 17 篇，B 级 10 篇。

> [!NOTE]
> - 06、10、12、13、16、17、19 等文件名没有题目。Phase 1 中会把文件**重命名或映射**为规范 ID（如 `P13_TED2016_CoatedSphericalECR`），但原文件保持不动。
> - **近重复论文对**：08/10 内容高度重复，06/07 主题相近。统计时需要去重或减半计权；划分留出集时必须**成对处理**，否则评测会被重复内容“泄题”。

### 留出集（评测用，不参与切片挑选）

建议从 A 级中选 **4 篇**，兼顾不同主题、类型和期刊：

| 留出 | 理由 |
|---|---|
| 05 | 实验类，微动方向，与 S 级主题相近，最能检验“像不像” |
| 09 | 仿真和理论类（IEEE TED） |
| 16 | 开关和熔焊方向（TCPMT 2018） |
| 19 | 连接器振动方向（TCPMT 2019，较新） |

全部 10 篇 B 级论文作为**第二校验集**，用来检验 Skill 输出是否更接近 Ren 本人，而不是“课题组平均风格”。

---

## 2. 已观察到的线索（只看了首页摘要，需在 Phase 2 中用全文验证）

### 2.1 作者的风格线索

| 线索 | 摘要中的例子 | 启示 |
|---|---|---|
| **`explicitly` 用得很多**，常放在句尾 | "are recorded explicitly"、"is investigated explicitly"、"was measured explicitly" | 这是典型的**个人签名词**，通用的 AI 黑名单根本不会覆盖到，正说明特征词需要靠脚本统计得出 |
| 介绍自研装置的固定说法 | "by introducing our new(ly) designed test rig"、"using our designed novel model switch" | 写入实验装置段落的模板 |
| 结论用“形式主语 + 被动”引出 | "It is shown that …"、"It is demonstrated that …"、"It was found that …" | 结果和摘要中的主力句式 |
| 递进连接词 | "Furthermore,"、"Moreover,"、"Subsequently,"、"Also," | 统计这些词的频率分布 |
| 相关性表述 | "closely correlates with"、"is closely dependent on" | 写进偏好表 |
| 开篇的重要性陈述 | "… is a very important concern to …"、"… are widely used in … to meet the requirements of high quality and high reliability for aviation and aerospace engineering" | 引言和摘要第一句的模板 |
| 摘要结构 | 背景一句 → "In this paper, …" → 方法 → 现象 → 机理解释 → 结论 | 写入摘要的写作模板 |

### 2.2 风格与语言错误要区分（这是需要你确认的设计决策）

首页中也出现了一些非母语表达，例如："are resulted from"、"our new designed test rig"、"ever published results have shown that limit hot switching cycles results from …"、"reoccurring the welding phenomenon"。

**建议的默认策略**：Skill **模仿 Ren 的修辞结构、句式偏好和签名用词**，但**修正语法错误**，保证输出能通过期刊审稿。
- 在 Phase 3 中把每条特征归为三类：`保留：风格特征` / `修正：语言错误` / `可选：非母语但无害`（例如偏爱 "Also," 开头）。
- SKILL.md 提供一个开关 `fidelity_level: strict | balanced(默认)`；选 strict 时连无害的非母语习惯也保留。

### 2.3 PDF 抽取中已经发现的问题（Phase 1 必须处理）

| 问题 | 出现的论文 |
|---|---|
| Elsevier 版式里的字母间空格，如 "a b s t r a c t"、"a r t i c l e i n f o" | 01、03、04 |
| 符号乱码，如 "25\u0001125 1C"（应为 25–125 °C） | 04 等 |
| 合字 "ﬁ" "ﬀ"、行尾连字符断词 "mea- suring" | 大量论文 |
| 首页是出版社封面或推荐文章（"Articles you may be interested in"） | 12、25 |
| IEEE 录用稿的版权横幅 | 19、23 |
| 首字下沉导致首字母丢失（"LECTROMECHANICAL"）、每行只有一个词 | 23 |
| 双栏版式、公式、图表标题混入正文 | IEEE 期刊论文 |

---

## 3. 电接触领域的章节和功能体系

这批论文以**实验型**和**建模仿真型**为主，常见结构是：Introduction → Experimental Setup / Model → Results and Discussion → Mechanism Analysis → Conclusions。标准章节标签据此调整如下：

| 章节标签 | 功能切片（examples 子目录） |
|---|---|
| `abstract` | `full`（整段摘要） |
| `introduction` | `background`（应用背景与可靠性需求）、`prior_work`（前人工作综述）、`gap`（尚未解决的问题）、`this_paper`（"In this paper, …" 段） |
| `experimental` | `test_rig`（自研装置介绍）、`specimen`（试样与材料）、`procedure`（测试条件与流程） |
| `modeling` | `model_setup`（有限元或解析模型的建立）、`derivation`（公式推导叙述）、`validation`（与 Holm 等经典理论或实验对比） |
| `results` | `waveform`（典型波形描述）、`trend`（参数影响趋势）、`surface_analysis`（SEM / EDS / 形貌分析） |
| `mechanism` | `explanation`（失效或物理机理解释） |
| `conclusion` | `numbered`（编号结论列表）或 `summary` |

---

## 4. 公开仓库的版权策略

> [!CAUTION]
> 仓库公开后，S 级的 01、03（Elsevier）和 13（IEEE）都是**出版社持有版权**的论文，不能把原文段落大量放进公开仓库。

采用**两层结构**：

| 层 | 内容 | 是否入库 |
|---|---|---|
| **公开层** `skills/ren-style-skill/` | ① 统计结论和规则（只是事实与规则的提炼，不涉及版权问题）；② **开放获取论文**的原文切片：22（IEEE Access，Ren 一作）可以按 CC BY 许可注明出处后引用；18、24（同为开放获取，B 级）只作对比参考；③ 每个“章节/功能”配 1 段**仿写示例**（由 Argon 按 Ren 的句式模板、用虚构的电接触实验内容写成，并经评测验证风格距离） | ✅ |
| **私有层** `skills/ren-style-skill/examples.local/` | 从 S/A 级受版权保护论文中选出的原文黄金切片 | ❌ 加入 gitignore，只在本地使用 |

- SKILL.md 中的加载逻辑：**如果存在 `examples.local/`，优先加载其中对应的切片，否则使用公开层的示例**。这样你本地效果最好，公开用户也能直接使用。
- 每个切片的 frontmatter 都要写清出处（DOI）。
- README 中写明：本项目用于辅助 Ren 课题组成员的写作和润色，不得用于代写或学术不端；**建议在公开前告知 Ren 老师并征得他的同意**。
- 原始 PDF、全文和 `data/` 目录一律不入库。

---

## 5. 仓库目录结构

```text
Ren-Style-Skill/
├── README.md / README.zh-CN.md
├── LICENSE                         # 代码 MIT；文本示例另附 NOTICE 说明出处与许可
├── NOTICE.md                       # 开放获取切片的 CC BY 署名
├── .gitignore                      # data/、config.yaml、**/examples.local/
├── requirements.txt
├── config.example.yaml             # corpus_dir、作者名、权重表、留出集
│
├── pipeline/
│   ├── 00_build_manifest.py        # 扫描 PDF → corpus_meta.csv（ID、题目、期刊、年份、一作、等级、权重、split）
│   ├── 01_extract_pdf.py           # PyMuPDF 按块抽取 + 双栏处理 + 封面和横幅剔除
│   ├── 02_clean_segment.py         # 去合字、去断词、修复符号、[EQ]/[CIT]/[FIG] 占位、分节分段 → paragraphs.jsonl
│   ├── 03_stylometry.py            # 按章节加权统计 → stats.json + stats_report.md
│   ├── 04_distinctive_lexicon.py   # 作者 vs AI 基线 vs B 级学生论文，计算加权对数几率比
│   ├── 05_rank_candidates.py       # 按典型性给段落排序 → candidates/
│   └── prompts/
│       ├── move_analysis.md
│       ├── style_vs_error.md       # 区分“风格”和“语言错误”
│       ├── profile_synthesis.md
│       ├── synthetic_example.md    # 生成公开层仿写示例
│       └── contrastive_pair.md
│
├── data/                           # gitignore：raw/、processed/、baseline/、candidates/
│
├── skills/ren-style-skill/         # ★ 交付物（自包含，可以单独复制使用）
│   ├── SKILL.md
│   ├── references/
│   │   ├── style_profile.md        # 规则编号 R01…，每条附语料证据（公开层只放短引用）
│   │   ├── style_profile.json      # lint 阈值
│   │   ├── lexicon.md              # 签名词、偏好动词和连接词、替换表、经语料验证的禁用词
│   │   ├── error_policy.md         # 风格与错误的区分表 + fidelity_level 说明
│   │   ├── glossary_zh_en.md       # 电接触术语表（微动 fretting、熔焊 contact welding、收缩电阻 constriction resistance、a 斑点 a-spot …）
│   │   ├── translation_guide.md
│   │   └── playbooks/{abstract,introduction,experimental,modeling,results,mechanism,conclusion}.md
│   ├── examples/                   # 公开层：开放获取原文 + 仿写示例 + 对比样例
│   │   ├── <section>/<function>_NN.md
│   │   └── contrastive/
│   ├── examples.local/             # 私有层（gitignore）
│   ├── scripts/
│   │   ├── style_lint.py
│   │   └── fidelity_check.py
│   └── templates/{polish_report,translation_report,review_report}.md
│
├── eval/
│   ├── splits.yaml                 # heldout: [05,09,16,19]，secondary: B 级全部
│   ├── run_eval.py
│   └── results/
└── docs/
    ├── design_notes.md             # 本方案
    └── build_your_own.md
```

---

## 6. 分阶段执行计划

### Phase 0：仓库初始化（约 0.5 天）
- `git init`；按 §5 建好目录骨架；写 `.gitignore`、`config.example.yaml`、`requirements.txt`（`pymupdf`、`spacy`、`nltk`、`pandas`、`textstat`、`scikit-learn`、`pyyaml`）；安装 `en_core_web_sm`。
- 把本方案保存为 `docs/design_notes.md`。
- **验收**：`git status` 中看不到任何 PDF、data 或 examples.local 文件。

### Phase 1：清单、抽取与清洗（约 1–2 天）
1. `00_build_manifest.py`：从 PDF 首页抽取题目、作者、期刊和年份，生成 `corpus_meta.csv`，并按 §1 预填等级、权重和 split。**生成后先停下来让你核对**，尤其是 23 的作者、05 的期刊和年份。
2. `01_extract_pdf.py`：用 PyMuPDF `get_text("blocks")` 按坐标处理双栏；剔除封面页（12、25）、版权横幅（19、23）和页眉页脚；参考文献之后的内容全部丢弃。
3. `02_clean_segment.py`：修复 §2.3 列出的全部问题；公式、引用、图表编号分别替换为 `[EQ]`、`[CIT]`、`[FIG n]`；按 §3 的标签分节。
4. 输出 `paragraphs.jsonl`：`{paper_id, tier, weight, split, section, para_idx, text, n_words}`。
- **验收**：每篇至少识别出 abstract、introduction、conclusion 和一个主体章节；随机抽 15 段（S 级至少 5 段）人工核对无乱码；文本中不再残留 "a b s t r a c t"、"ﬁ" 和断词。

### Phase 2：定量风格统计（约 1 天，全部由脚本完成）
- 只使用 **S 级和 A 级中 split=train 的论文**，按权重加权，**按章节分组**统计：句长分布、段长、被动语态比例、`we`/`our` 频率、"It is shown/found/demonstrated that" 类句式频率、各章节的时态比例、句首和段首连接词排行、报告动词排行、`explicitly` 等副词的位置、对冲词、分号和括号的使用、美式还是英式拼写、单位和数字格式（如 "0.2/0.5/1 A"、"25∼150 nm/s"）、缩写首次定义方式。
- `04_distinctive_lexicon.py` 做**三方对比**：
  - Ren（S+A） vs **AI 基线**（Argon 根据同样的摘要要点重写 30 段），得到“AI 腔纠偏表”；
  - Ren（S+A） vs **B 级学生论文**，得到 Ren 个人特有的特征，与课题组共性区分开。
- **验收**：`stats_report.md` 中每个章节都有完整指标；签名词列表中应能看到 `explicitly` 这类词（可作为脚本正确性的检查）。

### Phase 3：定性分析与风格档案（约 1–2 天，由 Argon 完成）
- `move_analysis.md`：按章节分别输入 S 级 3 篇加 A 级若干篇的对应段落，分析修辞步骤、论证推进方式、对前人工作的评价方式、结论的写法（编号列表还是段落）。
- `style_vs_error.md`：对 Phase 2 得到的每个特征，按 §2.2 的三类打标签。
- `profile_synthesis.md`：产出 `style_profile.md/.json`、`lexicon.md`、`error_policy.md`、`playbooks/*.md`。每条规则都要有编号、统计依据和一条短证据句。
- `glossary_zh_en.md`：从语料中抽取电接触术语，你可以补充课题组习惯的中文叫法。
- **验收**：不出现空泛规则；每条规则都能追溯来源；S 级特征与 A 级特征冲突时以 S 级为准，并注明。

### Phase 4：切片与示例（约 1–2 天）
- `05_rank_candidates.py`：计算每个段落到所在“章节/功能”质心的典型性距离（S 级段落距离 × 0.7 作为加分），每个功能保留前 8 个作为候选。
- 由你和 Argon 一起精选：
  - **私有层**：每个功能 2–3 段原文，每段 150–250 词，**至少 1 段来自 S 级**，覆盖不同论文；
  - **公开层**：论文 22 的原文切片，加上每个功能 1 段仿写示例（`synthetic_example.md`，用虚构的实验参数和现象，并通过 Phase 6 的风格距离检查）；
  - **对比样例**：6–8 组“AI 腔版本 vs Ren 版本”，标注差异对应的规则编号。
- **验收**：每个“章节/功能”在两层都有示例；留出集和 B 级论文没有出现在任何原文切片中。

### Phase 5：编写 Skill 本体（约 1–2 天）
Frontmatter：

```yaml
---
name: ren-style-skill
description: >-
  Use this skill when the user asks to draft, translate Chinese to English,
  polish, or style-check academic text on electrical contacts / electrical
  engineering in the writing style of Wanbin Ren (HIT). Covers abstract,
  introduction, experimental setup, modeling, results, mechanism, and conclusion.
---
```

正文流程（SKILL.md 控制在 200 行以内）：
1. **判定模式**：A 起草 / B 中译英 / C 润色 / D 审查；同时读取 `fidelity_level`（默认 balanced）。
2. **定位“章节/功能”**：按 §3 的标签体系判断，不确定时询问用户。
3. **按需加载**（顺序固定：**材料在前，指令在后**）：`examples.local/`（如果存在）或 `examples/` 中对应的 2–3 段 → 1–2 组 contrastive → 对应的 playbook → `style_profile.md` → `lexicon.md` / `error_policy.md` → 模式 B 再加 glossary 和 translation_guide。
4. **分块生成**：一次只处理一个小节，**≤ 600–800 词**；内容更长时带上上一块的最后一段续写，并重新加载切片。
5. **自检闭环**：运行 `style_lint.py`（检查禁用词、句长分布、被动比例、签名词密度是否在合理区间，签名词**不能堆砌**）；模式 B 和 C 还要运行 `fidelity_check.py`（数字、单位、`[CIT]`、公式、术语都不能改变），最多修订 2 轮。
6. **按模板输出**：润色给出“修改说明表”，每处修改引用规则编号；翻译附上存疑术语；审查只指出问题、不直接重写。

硬规则：不新增原文没有的论断、数据或引用；不照抄示例中的具体内容；禁用词表优先级最高；签名词使用频率不能超过统计上限。
- **验收**：4 种模式各用一个真实的课题组手稿片段测试，确认路由、加载和脚本运行都正确。

### Phase 6：评测与迭代（约 1–2 天，可循环多轮）

| 测试 | 数据 | 指标 |
|---|---|---|
| 回译还原 | 留出集 4 篇：段落 → 中文 → 模式 B 译回英文 | 与 Ren 质心的风格距离，对比不加载 Skill 的基线 |
| 去风格还原 | 留出集：段落 → AI 腔改写 → 模式 C 润色 | 同上，外加禁用词命中数 |
| 个人性检验 | B 级论文段落经模式 C 润色 | 输出应**向 Ren（S+A）质心靠近**，远离学生质心 |
| 盲测判别 | 原文与 Skill 输出混合，由另一个模型和你分别判断 | 判别准确率越接近 50% 越好 |
| 事实保真 | 所有模式 B 和 C 的输出 | 数字、单位、引用的改动数必须为 0 |
| 消融实验 | 分别去掉 examples、profile、contrastive、私有层 | 量化各组件的贡献，也衡量公开层与私有层的效果差距 |
| 跨模型 | 用 Argon 之外至少一个模型重复回译测试 | 检验可移植性 |

- **验收**：在风格距离和盲测两项上都显著优于基线；事实保真零改动；公开层效果不低于私有层的约 80%。

### Phase 7：GitHub 发布（约 0.5–1 天）
- 双语 README：功能介绍、安装方法（把 `skills/ren-style-skill/` 复制到 `.agents/skills/` 或 `~/.gemini/config/skills/`，也适用于 Claude Code、Gemini CLI 等工具的 skills 目录）、4 种模式示例、评测结果、局限性、版权声明。
- 增加 `dist/single_prompt.md`，供不支持 Skill 机制的对话模型直接使用。
- `docs/build_your_own.md`：说明如何用 pipeline 为其他作者构建风格 Skill。
- 发布前检查：`git ls-files` 中不能出现 PDF、data 或 examples.local；打 tag `v0.1.0`。

---

## 7. 给 Argon 的执行方式

- 一个 Phase 开一次会话；每次开头让它阅读 `docs/design_notes.md`，执行完按验收标准自检，提交 git commit 后再汇报。
- Phase 1、Phase 6 这类长任务可以使用 `/goal`；开始前可以先用 `/plan` 让它把任务拆细给你确认。
- **需要你本人参与的节点**：Phase 1 核对清单、Phase 3 审核规则（尤其是风格与错误的区分）、Phase 4 精选切片、Phase 6 盲测。

### Phase 0+1 启动提示词

```text
请阅读 docs/design_notes.md，执行 Phase 0 和 Phase 1。
语料目录：E:\张寅楠\03.个人文件夹\04.实验室论文集（只处理 *.pdf，不修改原文件）。
要求：
1. 完成 Phase 0 骨架后先提交一次 commit；
2. 运行 00_build_manifest.py 生成 corpus_meta.csv，按 §1 预填等级、权重和 split，
   然后停下来让我核对（重点：23 的作者、05 的期刊和年份）；
3. 我确认后再实现 01、02，并修复 §2.3 列出的全部抽取问题；
4. 按 Phase 1 的验收标准自检：随机抽取 15 段（S 级至少 5 段）展示给我，
   并报告每篇论文识别出的章节；
5. 确保 data/、config.yaml、examples.local/ 不会被 git 追踪。
```

---

## 8. 风险与应对

| 风险 | 应对 |
|---|---|
| 08/10 等近重复论文导致统计偏差和评测泄题 | 去重或减半计权；划分留出集时成对处理 |
| 模仿时把语法错误也学了进去 | 用 `error_policy.md` 区分，默认 balanced |
| 签名词（explicitly 等）被过度使用、显得刻意 | lint 中设置密度上限（按统计的 P90） |
| 公开层只有开放获取原文和仿写示例，效果偏弱 | 用消融实验量化差距；用对比样例和规则补偿 |
| 2013–2020 年间风格有演变 | Phase 2 中比较早期和晚期的指标；如果差异明显，以 S 级所在的早期风格为主，并在档案中注明 |
| 期刊版式不同（Elsevier 与 IEEE）带来格式差异 | 格式类规则（摘要标题、Index Terms 等）与文风规则分开，前者按目标期刊切换 |

---

## 9. 已确认的决策（2026-11-17）

1. **§2.2 风格与错误**：采用“模仿风格、修正语法”，即 `fidelity_level: balanced` 为默认值。
2. **§4 公开仓库的两层结构**：同意。受版权保护的原文切片只放在本地 `examples.local/`；已告知 Ren 老师并获得同意。
3. **§1 留出集**：05、09、16、19 留作测试；B 级论文全部作为第二校验集。
4. **23 号与 05 号论文核实（Phase 1 已确认）**：23 号一作为 Xu Zhang（B 级，Ren 为通讯作者）；05 号发表于 *Materials Research Innovations*（2015，Vol. 19, Suppl. 5, pp. S5-127–S5-132）。
