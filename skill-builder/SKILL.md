---
name: skill-builder
description: Comprehensive guide for building high-quality Claude skills from scratch. Use whenever the user wants to create a new skill, design a SKILL.md file, write skill instructions, structure a skill folder, craft a skill description, or plan a skill's architecture. Also use when the user says "build a skill", "make a skill", "write a skill", "create a skill", "new skill", "skill template", or asks about skill best practices, skill structure, or how to write effective skill instructions. This skill covers the full lifecycle from planning through testing. Do NOT use for running evals, benchmarking, or iterating on existing skills with automated testing — use the skill-creator skill for those workflows.
---

# Skill Builder

A practical guide to building skills that work reliably across diverse prompts. This skill distills the best practices from Anthropic's official guidance, proven patterns from production skills, and hard-won lessons about what actually makes Claude follow instructions consistently.

## Quick Reference

| I want to... | Go to |
|---|---|
| Start a new skill from scratch | Phase 1: Planning below |
| Write the YAML frontmatter | Read `references/frontmatter-guide.md` |
| Write effective instructions | Read `references/instruction-patterns.md` |
| Choose an architecture pattern | Read `references/architecture-patterns.md` |
| Test and iterate on my skill | Read `references/testing-and-iteration.md` |
| Debug a skill that isn't working | Read `references/troubleshooting.md` |
| Get a blank starter template | Copy from `assets/skill-template.md` |

---

## The Core Idea

A skill is a folder with a SKILL.md file that teaches Claude *how* to do something it already *can* do. Think of it as encoding your expertise into reusable instructions — the difference between "Claude can write emails" and "Claude writes emails that sound like me, using my company's tone, with the right greeting for each recipient."

Skills work because they solve a real problem: without them, every conversation starts from zero. You re-explain your preferences, your process, your edge cases. A good skill captures all of that once, and Claude applies it every time.

**Three levels of progressive disclosure:**

1. **Frontmatter** (name + description) — Always loaded in Claude's context (~100 words). This is how Claude decides whether to use your skill.
2. **SKILL.md body** — Loaded when the skill triggers. Your main instructions live here. Keep it under 500 lines.
3. **Bundled resources** (references/, scripts/, assets/) — Loaded on demand. Put detailed docs, templates, and code here. Claude reads them when needed.

This layering matters because context is a finite resource. A skill that dumps 2,000 lines of instructions into every conversation will crowd out the user's actual work. Front-load the essentials, and let Claude pull in details as needed.

---

## Phase 1: Planning

Before writing anything, answer these four questions. They shape every decision downstream.

### 1. What should this skill enable?

Be specific about the outcome. Not "help with documents" — rather "transform meeting transcripts into structured notes with action items, key decisions, and follow-ups in a .docx format."

### 2. What are 2-3 concrete use cases?

Write them as realistic user prompts — the actual things someone would type:

```
Use Case: Weekly Meeting Notes
Trigger: "Here's the transcript from our standup, can you turn it into notes?"
Steps:
1. Parse transcript for speakers, topics, decisions
2. Extract action items with owners and deadlines
3. Format into standard template
4. Save as .docx
Result: Polished meeting notes document
```

These use cases become your test suite later. If you can't write specific use cases, the skill isn't scoped tightly enough yet.

### 3. Which tools does this skill need?

Claude has built-in capabilities (code execution, file creation, web search) and may have access to MCP servers. Map out what your skill requires:

- **Built-in only**: File generation skills (docx, presentations, data analysis)
- **Single MCP**: Workflows for one service (Linear project setup, Notion pages)
- **Multi-MCP**: Cross-service orchestration (design handoff from Figma to Linear to Slack)

This determines whether you need a `compatibility` field in frontmatter and how you handle tool availability.

### 4. Is this problem-first or tool-first?

- **Problem-first**: User describes an outcome ("I need to set up a project workspace") and the skill orchestrates the right tools. The user doesn't need to know which APIs are called.
- **Tool-first**: User already has access to tools ("I have the Notion MCP connected") and the skill teaches Claude best practices for using them effectively.

Most skills lean one direction. Knowing which helps you choose the right architecture pattern from `references/architecture-patterns.md`.

---

## Phase 2: Building the Skill

### Step 1: Create the folder structure

```
your-skill-name/
├── SKILL.md                    # Required — main instructions
├── scripts/                    # Optional — executable code
│   └── validate.py             # Example: data validation script
├── references/                 # Optional — detailed documentation
│   └── api-patterns.md         # Example: API usage patterns
└── assets/                     # Optional — templates, fonts, icons
    └── report-template.md      # Example: output template
```

Naming rules that will save you debugging time:
- Folder name: kebab-case only (`my-cool-skill`, never `My_Cool_Skill`)
- Main file: exactly `SKILL.md` (case-sensitive — `skill.md` won't work)
- No README.md inside the skill folder — all documentation belongs in SKILL.md or references/
- The folder name should match the `name` field in your frontmatter

### Step 2: Write the frontmatter

The frontmatter is the single most important part of your skill. It's the only thing Claude sees *before* deciding whether to load your skill, so it controls when your skill activates.

```yaml
---
name: your-skill-name
description: [What it does] + [When to use it] + [Key capabilities]. Use when user mentions [specific triggers]. Also handles [related tasks].
---
```

The description field has a specific job: give Claude enough information to make a good triggering decision without loading the full skill. For the complete guide on writing effective descriptions — including good/bad examples, the formula that works, and how to handle under/over-triggering — read `references/frontmatter-guide.md`.

**Quick rules:**
- Under 1024 characters
- No XML angle brackets (< or >)
- Include real phrases users would say
- Say what NOT to use it for if there's a similar skill
- Be slightly "pushy" — Claude tends to under-trigger, so err on the side of encouraging activation

### Step 3: Write the instructions

This is the body of your SKILL.md, below the frontmatter. It's where you teach Claude your workflow.

**Recommended structure:**

```markdown
# Your Skill Name

## Quick overview
One paragraph explaining what this skill does and the general approach.

## Workflow
### Step 1: [First Major Step]
Clear explanation of what happens, why it matters, and exactly how to do it.

### Step 2: [Second Major Step]
...continue for each step...

## Output format
Define what the final deliverable looks like.
Use a template if the structure should be consistent.

## Common issues
### [Problem scenario]
What causes it and how to handle it.

## Examples
### Example 1: [Typical case]
Input: [What the user provides]
Output: [What the skill produces]
```

The art of writing good instructions is a deep topic. Read `references/instruction-patterns.md` for the complete guide on writing style, the "explain why" principle, working with examples, handling edge cases, and progressive disclosure.

**The most important principle**: explain *why*, not just *what*. Claude is smart — when it understands the reasoning behind an instruction, it generalizes better to novel situations. "Format dates as YYYY-MM-DD because the downstream system parses this format" is more robust than "Format dates as YYYY-MM-DD" alone.

### Step 4: Add bundled resources (if needed)

When your SKILL.md is getting long (approaching 500 lines), move detailed content into reference files and point Claude to them. For example, in your own skill you might write:

```markdown
# Example of how you'd reference a file in YOUR skill:
Before writing API queries, read `references/api-patterns.md` for:
- Rate limiting guidance
- Pagination patterns
- Error codes and handling
```

Guidelines for what goes where:

| Content type | Location | Why |
|---|---|---|
| Core workflow (always needed) | SKILL.md body | Loaded every time skill triggers |
| Detailed reference (sometimes needed) | references/ | Loaded on demand, saves context |
| Executable code (deterministic tasks) | scripts/ | Runs without loading into context |
| Templates and static files | assets/ | Used in output generation |

Scripts are especially powerful for validation. Code is deterministic — it either passes or fails — while language instructions can be interpreted loosely. If something can be checked programmatically (JSON structure, required fields, file formats), write a script for it.

---

## Phase 3: Refining

### Write a draft, then step back

After your first draft, re-read the whole skill with fresh eyes. Common things to catch:

1. **Overfit instructions** — Rules so specific they only work for your test cases but break on real-world variation. Generalize by explaining the *principle* behind the rule.
2. **Missing context** — You know things about your workflow that you forgot to write down. Ask: "If someone with no context read this, would they understand the steps?"
3. **Heavy-handed language** — If you have lots of ALWAYS/NEVER in all-caps, try reframing as explanations. "Always validate before proceeding" becomes "Validate data before proceeding — catching format errors here prevents silent failures downstream that are much harder to debug."
4. **Unused instructions** — Lines that sound good but don't change behavior. Every instruction should pull its weight. If removing a line wouldn't change the output, it's dead weight consuming context.

### Test with realistic prompts

Generate 2-3 test prompts that sound like things a real user would actually type — casual language, varying specificity, sometimes including typos or incomplete information. Then run them.

The first run reveals more about your skill's quality than hours of re-reading the instructions. Read `references/testing-and-iteration.md` for the full testing methodology.

### Iterate based on what you see

When something doesn't work:
1. Read the transcript (not just the output) — understand *where* Claude went off track
2. Identify whether the issue is in triggering, instructions, or output formatting
3. Make targeted changes rather than wholesale rewrites
4. Test again to verify the fix didn't break something else

---

## Phase 4: Pre-launch Checklist

Before deploying your skill, run through this:

**Structure**
- [ ] Folder is kebab-case, matches `name` field
- [ ] SKILL.md exists (exact spelling, case-sensitive)
- [ ] Frontmatter has `---` delimiters, `name`, and `description`
- [ ] No XML angle brackets anywhere in frontmatter
- [ ] SKILL.md is under 500 lines (move overflow to references/)

**Description quality**
- [ ] Includes what the skill does AND when to use it
- [ ] Contains specific trigger phrases users would say
- [ ] Mentions relevant file types if applicable
- [ ] Specifies what NOT to use it for (if competing skills exist)
- [ ] Under 1024 characters

**Instructions quality**
- [ ] Instructions are specific and actionable (not vague)
- [ ] Explains why behind important rules
- [ ] Includes examples for complex or ambiguous tasks
- [ ] Error handling for common failure modes
- [ ] References to bundled resources are clear and purposeful

**Testing**
- [ ] Triggers on obvious tasks
- [ ] Triggers on paraphrased/casual requests
- [ ] Does NOT trigger on unrelated topics
- [ ] Produces correct output on 2-3 test cases
- [ ] Output format matches expectations

---

## Key Principles (Keep These Close)

**1. Progressive disclosure saves context.** SKILL.md is your main stage. References are backstage. Scripts are the tech booth. Don't put everything on stage at once.

**2. The description is your skill's resume.** It's the only thing Claude reads before deciding to hire your skill for a task. Make it specific, include trigger phrases, and be slightly pushy.

**3. Explain why, not just what.** Claude generalizes from understanding. "Validate inputs because downstream systems fail silently on bad data" beats "Always validate inputs."

**4. Code beats language for deterministic checks.** If you can write a script to validate something, do it. Language instructions are flexible; scripts are precise.

**5. Test with realistic prompts.** Not "please execute the standard workflow" but "hey can you clean up these meeting notes from yesterday, they're kind of a mess."

**6. Skills are living documents.** Your first version won't be perfect. Ship it, use it, notice what breaks, fix it. The feedback loop between real usage and skill improvement is where quality lives.

**7. Composability over monoliths.** Your skill should work well alongside other skills, not try to do everything. If you find yourself building a 1,000-line skill, consider splitting it into two focused skills.
