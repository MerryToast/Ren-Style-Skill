# examples/ — public example layer

Contains only:
- excerpts from **open-access** papers (e.g. P22, IEEE Access, CC BY 4.0) — attribute in `NOTICE.md`;
- **synthetic** paragraphs written in Ren's style with fictitious content (`pipeline/prompts/synthetic_example.md`);
- `contrastive/` pairs (AI-default vs Ren) built from synthetic or open-access originals.

Layout: `<section>/<function>_NN.md`, 150–250 words each, with frontmatter:

```markdown
---
section: introduction
function: gap
source: P22 (IEEE Access 2020, doi:10.1109/ACCESS.2020.2994085, CC BY 4.0)   # or: synthetic
moves: [...]
rules: [R..]
notes: ...
---
<paragraph>
```

Copyrighted excerpts go to `../examples.local/` (gitignored), never here.
