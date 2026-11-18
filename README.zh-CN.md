# Ren-Style-Skill (`v0.1.0`)

> 面向 **电接触与机电电器工程** 领域的学术英文写作 Agent **Skill**，基于 **任万滨教授（哈尔滨工业大学）** 30 篇代表性学术论文构建，支持论文起草、中译英、英文润色与文风审查。
>
> English documentation: **[README.md](README.md)** | 架构与设计细节：**[docs/design_notes.md](docs/design_notes.md)**

---

## 1. 核心功能与 4 种工作模式

本 Skill 从 30 篇课题组英文论文（`P01`–`P30`：含 S 级锚点论文 3 篇、A 级任老师一作论文 17 篇、以及作为“学生腔”负向对照的 B 级学生一作论文 10 篇）中提炼出分章节定量句法档案（`R01`–`R33`）、三方对比特征词表（Ren S+A vs. AI 基线 vs. B 级学生集）及修辞步进（Move）剧本。

| 模式 | 适用场景 / 输入 | 输出格式 | 自动校验闭环 |
| :--- | :--- | :--- | :--- |
| **Mode A — 起草（Draft）** | 某小节实验记录、公式推导或要点提纲 | 符合 Ren 文风的英文学术段落 | `style_lint.py` |
| **Mode B — 中译英（Translate）** | 中文初稿段落 | Ren 风格英文译文 + 专业术语对照与存疑说明（[translation_report.md](skills/ren-style-skill/templates/translation_report.md)） | `style_lint.py` + `fidelity_check.py --mode translate` |
| **Mode C — 润色（Polish）** | 英文初稿（AI 腔或学生初稿） | 润色后正文 + 逐处引用规则编号（`R01`–`R33` / `F01`–`F36`）的修改说明表（[polish_report.md](skills/ren-style-skill/templates/polish_report.md)） | `style_lint.py` + `fidelity_check.py --mode polish` |
| **Mode D — 审查（Review）** | 英文初稿 | 仅输出偏离文风/语法的诊断报告与改法建议，不直接重写（[review_report.md](skills/ren-style-skill/templates/review_report.md)） | `style_lint.py` |

- **默认策略 `fidelity_level: balanced`（推荐）**：严格模仿任老师的修辞推进、句长交替节奏与签名表达（`KEEP_STYLE` `R01`–`R33`），**同时自动修正非母语语法瑕疵**（`FIX_ERROR` `F01`–`F16`），并彻底清除大模型套话（`AI_CLICHE` `F17`–`F28`）与学生一作常见漂移表达（`F29`–`F36`），确保输出可直接用于期刊投稿。
- **可选策略 `fidelity_level: strict`**：在 `balanced` 基础上保留语料中无害的习惯表达（`O01`–`O08`，如 `4-wires method`、句首 `And` 等）。

---

## 2. 安装与使用方式

### 方式一：作为 Agent Skill 安装（Antigravity / Claude Code / Gemini CLI / Cursor）

将自包含目录 [`skills/ren-style-skill/`](skills/ren-style-skill/)（无任何第三方运行时依赖，自检脚本仅依赖 Python 标准库）复制到对应工具的 `skills` 目录：

- **Google Antigravity（工作区级）**：`<项目根目录>/.agents/skills/ren-style-skill/`
- **Google Antigravity（全局级）**：`~/.gemini/config/skills/ren-style-skill/`
- **Claude Code**：`<项目根目录>/.claude/skills/ren-style-skill/` 或 `~/.claude/skills/ren-style-skill/`
- **其他支持 `SKILL.md` 的 Agent**：复制到其对应的 skills 目录。

### 方式二：单文件提示词包（适用于网页端对话模型）

对于不支持多文件 Skill 机制的对话端（如网页版 ChatGPT、Claude、DeepSeek、Gemini），直接复制 **[dist/single_prompt.md](dist/single_prompt.md)** 全文粘贴至对话窗口，并在末尾附上待处理的段落与模式指令。

---

## 3. 四种模式调用示例

> **最佳实践**：建议**每次处理一个小节（≤ 600–800 词）**，并在提示词中指明目标 `section/function` 槽位（共 17 个槽位，涵盖 `abstract`、`introduction`、`experimental`、`modeling`、`results`、`mechanism`、`conclusion`）。

### 示例 1 — Mode A 起草（根据实验要点写正文）
```text
使用 ren-style-skill（Mode A，章节槽位：results/waveform）：
根据以下实验记录起草一段英文正文：
- 图号 [FIG 5]：微动幅值 25 μm、频率 100 Hz、法向载荷 2.0 N 下接触电阻与切向摩擦力随循环次数的演化曲线。
- 分为三个阶段：第 I 阶段跑合期（0–600 次，接触电阻从 8.5 mΩ 降至 6.2 mΩ，切向摩擦力从 0.45 N 升至 0.78 N）；第 II 阶段低波动平台期（600–8.5×10^3 次，维持在 6.0–7.4 mΩ）；第 III 阶段快速退化期（超过 8.8×10^3 次后出现 >150 mΩ 的间歇尖峰，在 1.12×10^4 次达到 0.5 Ω 失效阈值）。
```

### 示例 2 — Mode B 中译英（中文手稿翻译）
```text
使用 ren-style-skill（Mode B，章节槽位：experimental/procedure，保真度：balanced）：
将以下实验方法段落译为英文并输出术语对照表：
法向接触力设定为 3 N，负载电流为 10 mA。动触头为直径 2 mm 的球形骑子（rider），静电极为平面试样。基体材料采用铜合金，表面镀覆厚度为 1 μm 的纯金镀层。采用四线法实时记录接触电阻的瞬态值，测量原理由 [FIG 1] 给出……
```

### 示例 3 — Mode C 润色（消除 AI 腔或学生腔）
```text
使用 ren-style-skill（Mode C，章节槽位：introduction/gap，保真度：balanced）：
将以下带有明显 AI 腔的段落润色为任万滨老师的写作风格，并附上带规则编号的修改说明表：
"Despite its critical practical importance, there remains a glaring gap in our comprehensive understanding of how radial slip gradients govern the wear-through durability of duplex palladium-nickel coatings. Furthermore, existing theoretical frameworks fail to capture the intricate interplay between stick and slip zones..."
```

### 示例 4 — Mode D 审查（仅诊断不重写）
```text
使用 ren-style-skill（Mode D，章节槽位：introduction/background）：
审查以下英文初稿段落，指出偏离任老师文风或存在非母语语法问题的句子并给出修改建议（不要直接重写整段）：
"It is top-urgent to understand and determine the failure mechanisms of silver tin oxide composite material used in switching devices. Ever published research results have determined that..."
```

---

## 4. 留出集（Heldout `[P05, P09, P16, P19]`）定量评测结果

通过运行 `python pipeline/06_evaluate.py`，在严格未参与统计与切片的 4 篇留出集论文（`P05, P09, P16, P19`，覆盖全部 7 个章节）及 B 级学生一作论文集上完成全量评测（完整报告见本地 `data/eval_report.md`）：

### 4.1 回译还原与消融实验（`留出集原文 → 中文 → Mode B 英文`）

| 系统配置 | 到 Ren (S+A) 质心平均风格距离 $d(\cdot, \mu_{\text{Ren S+A}})$ ↓ | `style_lint.py` 通过率 ↑ | 禁用词命中数 ↓ | `fidelity_check.py` 事实保真率 ↑ |
| :--- | :---: | :---: | :---: | :---: |
| **Baseline（不加载 Skill）** | `1.2367` | `0.0%` | `16` | `100.0%` |
| **消融：`-Profile/Lexicon`（仅示例）** | `1.2869` | `25.0%` | `0` | `100.0%` |
| **消融：`-Examples`（仅规则与 Playbook）** | `1.6819` | `25.0%` | `0` | `100.0%` |
| **消融：`-Contrastive`（无对比对）** | `0.7077` | `75.0%` | `0` | `100.0%` |
| **Skill Mode B（仅公开层 `examples/`）** | **`0.6913`** | **`100.0%`** | **`0`** | **`100.0%`** |
| **Skill Mode B（完整版：私有层 + 公开层）** | **`0.6639`** | **`100.0%`** | **`0`** | **`100.0%`** |

- **公开层 vs. 私有层效果对比**：在不包含受版权保护原文切片的情况下，仅使用可公开分发的 `examples/`（`P22` OA 摘录 + 合成示例 + 对比样例 + 规则库）在回译任务上达到了完整私有层风格距离改善幅度的 **`95.2%`**，在 Mode C 去风格润色任务上达到 **`88.5%`**（均超过设计指标要求的 `≥ 80%`）。

### 4.2 个人性检验（`B 级学生一作段落 → Mode C 润色`）

- 润色前，6 段 B 级学生初稿到 `Ren (S+A)` 质心平均距离为 `1.3999`，到 `Student (B)` 质心距离为 `0.9095`；
- 经 Mode C 润色后，到 `Ren (S+A)` 质心距离大幅缩短至 **`0.5071`（`-63.8%`）**，而到 `Student (B)` 质心距离拉远至 **`1.1601`（`+27.6%`）**，10 处典型学生腔（如 `It is top-urgent`、`Ever published`、`to the best of our knowledge`、句首设问等）**100% 清除**，且数字、单位、引用与公式 **0 改动**。

### 4.3 三方盲测判别（`16 组留出集盲测对/臂`，理想不可区分值 $\approx 50\%$）

- **`Original vs. Baseline（不加载 Skill）`**：双判别器平均识别准确率高达 **`92.2%`**；
- **`Original vs. Skill（Public 公开层）`**：平均识别准确率降至 **`39.1%`**；
- **`Original vs. Skill（Full 私有层）`**：平均识别准确率降至 **`40.6%`**（与真实原文不可区分）。

---

## 5. 本地复现与为其他学者构建风格 Skill

如需在本地重新运行完整数据处理与评测管线，或使用本仓库管线为其他学者构建写作风格 Skill（详见 **[docs/build_your_own.md](docs/build_your_own.md)**）：

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item config.example.yaml config.yaml   # 将 corpus_dir 修改为本地 PDF 文件夹路径
python pipeline/00_build_manifest.py
python pipeline/01_extract_pdf.py
python pipeline/02_clean_segment.py
python pipeline/03_stylometry.py
python pipeline/04_distinctive_lexicon.py
python pipeline/05_rank_candidates.py
python pipeline/06_evaluate.py
python pipeline/07_pack_single_prompt.py
```

---

## 6. 局限性、版权隔离与学术伦理声明

- **适用领域边界**：本 Skill 的专业术语表与修辞剧本针对**电接触、机电开关/继电器、微动磨损与导电镀层退化、有限元接触建模**专门标定；跨学科使用前请按 [docs/build_your_own.md](docs/build_your_own.md) 重新提取目标领域语料。
- **双层版权隔离设计**：
  - 本仓库**不包含任何论文 PDF 或全文**。受出版商版权保护的原文黄金摘录仅保存在本地 `skills/ren-style-skill/examples.local/` 目录（已严格配置 `.gitignore`，绝不上传或分发）。
  - 公开仓库 `skills/ren-style-skill/examples/` 仅包含来自开放获取论文 `P22`（*IEEE Access* 2020, CC BY 4.0，已在 [NOTICE.md](NOTICE.md) 完整署名）的短摘录及虚构内容的合成示例（`source: synthetic`）。
- **知情同意与学术诚信**：本工具旨在辅助课题组成员进行论文起草、中译英与语言润色，绝不捏造实验数据、数值或参考文献，作者须对论文的科学真实性与原创性承担全部责任。

## 开源许可

代码、统计规则与合成示例采用 [MIT License](LICENSE) 开源；引用的开放获取短摘录遵循 CC BY 4.0 许可（详见 [NOTICE.md](NOTICE.md)）。
