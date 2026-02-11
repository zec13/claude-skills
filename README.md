# Claude Skills

Personal collection of Claude skills for use with Claude Code and Cowork.

## Skills

### Table Clay (Brand)
| Skill | Description |
|-------|-------------|
| **social-media-engagement** | Automated social media engagement across Instagram and Facebook: follows, likes/reactions, comments, and Group participation via browser automation with swappable brand context. |
| **native-image-ad-generator** | Creates native-looking image ads for social media campaigns. |
| **product-placer** | Places product images into contextual lifestyle settings. |
| **ad-swipe-engine** | Captures and analyzes competitor ads for creative inspiration. |
| **product-research** | Deep product research and competitive analysis workflows. |

### Seurat Group (Consulting)
| Skill | Description |
|-------|-------------|
| **seurat-meeting-notes** | Transforms meeting transcripts into polished Seurat Group notes with Next Steps, Key Takeaways, and Full Notes. |
| **headline-writer** | Generates consulting slide headlines at three boldness levels (Conservative, Balanced, Bold). |
| **qc-cookbook** | QC recipes and checklists for consulting deliverables. |
| **survey-document-builder** | Converts survey wireframes into fully programmed quantitative survey documents. |

### General / Meta
| Skill | Description |
|-------|-------------|
| **email-responder** | Drafts email responses in Nick Fisher's writing style. |
| **meta-ads-research** | Deep competitor research using Meta Ad Library with browser automation. |
| **skill-creator** | Advanced skill creation with eval runs, benchmarking, and automated testing. |

## Folder Structure

```
claude-skills/
├── README.md
├── ad-swipe-engine/
│   ├── SKILL.md
│   └── references/
├── email-responder/
│   ├── SKILL.md
│   └── references/
├── headline-writer/
│   └── SKILL.md
├── meta-ads-research/
│   ├── SKILL.md
│   ├── assets/
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
├── skill-creator/
│   ├── SKILL.md
│   ├── agents/
│   ├── references/
│   └── scripts/
├── social-media-engagement/
│   ├── SKILL.md
│   ├── references/
│   └── engagement-log.csv
└── survey-document-builder/
    ├── SKILL.md
    └── references/
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
- The `engagement-log.csv` in social-media-engagement is a persistent session tracker across both Instagram and Facebook (will grow over time)
