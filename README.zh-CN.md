# Ren-Style-Skill

> 一个用于模仿 **任万滨（Wanbin Ren，哈尔滨工业大学）** 论文写作风格的 Agent **Skill**，面向**电接触 / 电气工程**领域论文。
>
> English: [README.md](README.md)

> [!NOTE]
> **状态：建设中（v0.0.x）**。仓库框架已搭好，风格规则和示例由构建管线生成。详见 [docs/design_notes.md](docs/design_notes.md)。

## 功能

| 模式 | 输入 | 输出 |
|---|---|---|
| **A 起草** | 某个小节的要点或草稿 | 符合 Ren 风格的段落 |
| **B 中译英** | 中文手稿 | Ren 风格的英文译文 + 存疑术语表 |
| **C 润色** | 英文草稿 | 润色后正文 + 修改说明（引用规则编号） |
| **D 审查** | 英文草稿 | 列出偏离风格的位置和改法（不直接重写） |

默认策略 `fidelity_level: balanced`：模仿 Ren 的修辞结构、句式偏好和签名用词，**同时修正语法错误**，保证输出可以直接投稿。

## 安装

把自包含目录 [`skills/ren-style-skill/`](skills/ren-style-skill/) 复制到对应 Agent 的 skills 目录：

- Antigravity（项目级）：`<项目>/.agents/skills/ren-style-skill/`
- Antigravity（全局）：`~/.gemini/config/skills/ren-style-skill/`
- 其他支持 `SKILL.md` 的 Agent：放到它们的 skills 目录

不支持 Skill 的对话模型可以使用 `dist/single_prompt.md`（Phase 7 生成）。

## 使用示例

```text
使用 ren-style-skill，模式 B：把下面这段引言中“研究空白”段翻译成英文。
<中文段落>
```

**每次只处理一个小节（≤ 800 词）**，风格一致性最好。

## 自行构建

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_sm
Copy-Item config.example.yaml config.yaml   # 修改 corpus_dir
python pipeline/00_build_manifest.py        # 依次运行 00 → 05
```

## 版权与伦理

- 仓库不分发任何论文原文或全文。受版权保护论文的摘录只保存在本地 `examples.local/`（已加入 gitignore）；开放获取论文的摘录在 [NOTICE.md](NOTICE.md) 中注明出处。
- 已告知任万滨老师并获得同意。
- 仅用于**辅助课题组成员写作与润色**，不得用于代写、冒名或任何学术不端行为。

## 许可

代码与原创文档：[MIT](LICENSE)；引用的文本摘录见 [NOTICE.md](NOTICE.md)。
