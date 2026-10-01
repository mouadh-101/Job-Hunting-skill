# Multi-Agent Setup & Execution Guide

**Job-Hunting-skill** is built to be agent-agnostic. Whether you use **Google Antigravity**, **Claude Code**, **Cursor**, **Windsurf**, or **ChatGPT Web**, this repository works right out of the box.

---

## 1. Using with Google Antigravity / Gemini CLI

Google Antigravity natively loads Agent Skills defined in `skills/*/SKILL.md`.

### Method A: Workspace Installation (Immediate)
Simply open this repository as your active workspace in Antigravity. Antigravity will automatically discover:
`skills/job-hunter/SKILL.md`

### Method B: Global Skill Installation
To make the skill globally accessible across all your Antigravity sessions:
```bash
# Windows
mkdir -p "$HOME\.gemini\config\skills\job-hunter"
cp -r skills/job-hunter/* "$HOME\.gemini\config\skills\job-hunter\"

# macOS / Linux
mkdir -p ~/.gemini/config/skills/job-hunter
cp -r skills/job-hunter/* ~/.gemini/config/skills/job-hunter/
```

---

## 2. Using with Claude Code (`claude`)

Claude Code automatically reads the `CLAUDE.md` file located at the repository root.

1. Open your terminal in the cloned repository folder:
   ```bash
   cd Job-Hunting-skill
   claude
   ```
2. Onboard your profile:
   > *"Extract my background from my_profile/old_cv/resume.pdf and build my_profile/candidate_profile.md"*
3. Apply to a job:
   > *"Tailor an application for this job posting: [PASTE URL OR JOB DESCRIPTION]"*

---

## 3. Using with Cursor

Cursor automatically ingests `.cursorrules` and rules inside `.cursor/rules/job-tailor.mdc`.

1. Open `Job-Hunting-skill` in Cursor (`File > Open Folder...`).
2. Press `Ctrl+L` (or `Cmd+L`) to open the Cursor Composer or Chat.
3. Prompt your Cursor agent:
   > *"Here is a job offer from Stripe for a Software Engineer role. Research the company, create the application folder, tailor my 1-page CV and Cover Letter, and compile to PDF."*

---

## 4. Using with Windsurf (Cascade)

Windsurf natively picks up `.windsurfrules` in the root directory.

1. Open the project folder in Windsurf.
2. Open Cascade (`Ctrl+I` or `Cmd+I`).
3. Send your job application request directly to Cascade.

---

## 5. Using with Web LLMs (ChatGPT, Claude.ai, Gemini Web)

If you don't use a coding agent and prefer using web interfaces:
1. Open [SYSTEM_PROMPT.md](SYSTEM_PROMPT.md).
2. Copy the system prompt and paste it into ChatGPT (Custom GPT, Project, or standard chat).
3. Paste the contents of your `my_profile/candidate_profile.md`.
4. Paste the job description you want to apply for.
5. ChatGPT will generate your LaTeX code and email drafts.
6. Copy the `.tex` code and paste it into [Overleaf.com](https://www.overleaf.com/) to compile into a PDF in one click!
