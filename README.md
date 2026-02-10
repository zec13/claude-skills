# Claude Skills

Personal collection of Claude skills for use with Claude Code and Cowork.

## Skills

### Table Clay (Brand)
| Skill | Description |
|-------|-------------|
| **tableclay-instagram-engagement** | Automated Instagram engagement: 15 follows/likes and 5 comments per session via Explore tab discovery. |
| **tableclay-prompts** | Table Clay brand prompts and context for consistent messaging. |
| **native-image-ad-generator** | Creates native-looking image ads for social media campaigns. |
| **nano-banana-product-swap** | Swaps product images into lifestyle scenes and templates. |
| **product-placer** | Places product images into contextual lifestyle settings. |
| **ad-swipe-engine** | Captures and analyzes competitor ads for creative inspiration. |
| **product-research** | Deep product research and competitive analysis workflows. |

### Seurat Group (Consulting)
| Skill | Description |
|-------|-------------|
| **seurat-meeting-notes** | Transforms meeting transcripts into polished Seurat Group notes with Next Steps, Key Takeaways, and Full Notes. |
| **seurat-prompts** | Seurat Group brand prompts and context for consistent consulting outputs. |
| **headline-writer** | Generates consulting slide headlines at three boldness levels (Conservative, Balanced, Bold). |
| **slide-qc** | Quality checks presentation slides for formatting, content, and consistency. |
| **qc-cookbook** | QC recipes and checklists for consulting deliverables. |
| **survey-document-builder** | Converts survey wireframes into fully programmed quantitative survey documents. |
| **cpg-consulting-copilot** | End-to-end CPG consulting assistant for research, strategy, and deliverables. |

### General / Meta
| Skill | Description |
|-------|-------------|
| **email-responder** | Drafts email responses in Nick Fisher's writing style. |
| **meta-ads-research** | Deep competitor research using Meta Ad Library with browser automation. |
| **skill-builder** | Practical guide for building high-quality Claude skills from scratch. |
| **skill-creator** | Advanced skill creation with eval runs, benchmarking, and automated testing. |

## Folder Structure

```
claude-skills/
├── README.md
├── ad-swipe-engine/
│   ├── SKILL.md
│   └── references/
├── cpg-consulting-copilot/
│   └── SKILL.md
├── email-responder/
│   ├── SKILL.md
│   └── references/
├── headline-writer/
│   └── SKILL.md
├── meta-ads-research/
│   ├── SKILL.md
│   ├── assets/
│   └── references/
├── nano-banana-product-swap/
│   ├── SKILL.md
│   └── references/
├── native-image-ad-generator/
│   ├── SKILL.md
│   ├── assets/
│   └── references/
├── product-placer/
│   ├── SKILL.md
│   └── references/
├── product-research/
│   ├── SKILL.md
│   └── references/
├── qc-cookbook/
│   └── SKILL.md
├── seurat-meeting-notes/
│   ├── SKILL.md
│   └── references/
├── seurat-prompts/
│   └── SKILL.md
├── skill-builder/
│   └── SKILL.md
├── skill-creator/
│   ├── SKILL.md
│   ├── agents/
│   ├── references/
│   └── scripts/
├── slide-qc/
│   └── SKILL.md
├── survey-document-builder/
│   ├── SKILL.md
│   └── references/
├── tableclay-instagram-engagement/
│   ├── SKILL.md
│   └── engagement-log.csv
└── tableclay-prompts/
    └── SKILL.md
```

## Setup

### With Claude Code

Clone this repo, then symlink or copy skills into your Claude Code skills directory:

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/claude-skills.git

# Option 1: Symlink the whole repo as your skills directory
ln -s /path/to/claude-skills ~/.claude/skills

# Option 2: Symlink individual skills
ln -s /path/to/claude-skills/email-responder ~/.claude/skills/email-responder
```

### With Cowork

Skills in this repo can be loaded into Cowork by placing them in the Cowork skills directory (typically `~/.claude/skills/` or the `.skills/skills/` path Cowork reads from).

## Adding a New Skill

1. Create a new folder with a kebab-case name
2. Add a `SKILL.md` with frontmatter (name + description) and instructions
3. Optionally add `references/`, `assets/`, or `scripts/` subdirectories
4. Update this README's table and folder structure
5. Commit and push

## Notes

- Each skill's `SKILL.md` is the entry point Claude reads when the skill triggers
- `references/` folders contain supporting docs that SKILL.md can reference
- `assets/` folders contain templates and reusable content
- `scripts/` folders contain executable helper scripts
- The `engagement-log.csv` in tableclay-instagram-engagement is a persistent session tracker (will grow over time)
