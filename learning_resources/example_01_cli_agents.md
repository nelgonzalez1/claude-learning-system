# 📚 Learning Notes: Building AI Agents with CLI Tools

**Video**: CLI Tools + Claude Code = Personal AI Agents
**Date**: 2024-08-24
**Duration**: 11:18

## 🎯 Top 3 Takeaways

1. **CLI tools + Claude Code = Powerful Agents**: Any terminal tool can become an AI-controlled agent
2. **Context is King**: The claude.md file defines how the agent behaves
3. **2-Hour Development**: Complex automations can be built incredibly fast

## 💡 Core Concepts Explained

### AI Agents vs Basic Models
- **Basic Models**: Generate code snippets, answer questions
- **AI Agents**: Execute commands, control tools, complete workflows
- **Key Difference**: Agents have "hands" (bash tool) to actually DO things

### Tool Integration Pattern
```
User Request → Claude Code → Bash Tool → CLI Program → Result
```

### Context Engineering
- **Definition**: Providing the right information at the right time to AI
- **Implementation**: claude.md file with commands, examples, workflows
- **Result**: Specialized agent for specific tasks

## 🛠️ Practical Examples to Build

### Example 1: Simple Download Agent
```python
# claude.md content
"""
You are a download assistant. When given URLs:
1. Use aria2c for general downloads
2. Use gallery-dl for image galleries
3. Use yt-dlp for videos

Commands:
- aria2c [URL] - Fast parallel downloader
- gallery-dl [URL] - Gallery/image downloader
- yt-dlp [URL] - YouTube/video downloader
"""

# Usage in Claude Code:
# "Download this file: https://example.com/file.pdf"
# Claude automatically runs: aria2c https://example.com/file.pdf
```

### Example 2: Git Repository Analyzer
```python
# cli.py using Click framework
import click
import subprocess

@click.group()
def git_agent():
    """Git repository analysis agent"""
    pass

@git_agent.command()
@click.argument('repo_url')
def analyze(repo_url):
    """Analyze a GitHub repository"""
    # 1. Check repository size
    size = check_repo_size(repo_url)
    
    # 2. If small, get full content
    if size < 200000:
        content = get_full_repo(repo_url)
    else:
        # Get only docs and README
        content = get_docs_only(repo_url)
    
    # 3. Save for analysis
    save_to_file(content)
    
    click.echo(f"Repository ready for analysis: {size} tokens")

# In claude.md:
"""
When given a GitHub URL:
1. Run: git-agent analyze [URL]
2. Read the extracted content
3. Provide analysis based on user request
"""
```

### Example 3: Daily Automation Script
```bash
#!/bin/bash
# morning_routine.sh

# Called by Claude Code every morning
echo "🌅 Starting morning routine..."

# 1. Check emails (using CLI email client)
mutt -f ~/Mail/inbox -e "set sort=reverse-date"

# 2. Update repositories
for repo in ~/projects/*; do
    cd "$repo"
    git pull
done

# 3. Check calendar
gcalcli agenda

# 4. Generate daily summary
echo "Today's priorities:" > daily_summary.md
```

## 🔧 Immediate Action Items

### 1. Install Essential CLI Tools
```bash
# Package managers
brew install aria2        # Fast downloads
brew install gallery-dl   # Image galleries
brew install yt-dlp       # Video downloads
pip install click         # CLI framework
pip install gitingest     # Repository analyzer
```

### 2. Create Your First claude.md
```markdown
# claude.md - My Download Assistant

## Your Role
You are my personal download assistant. You help me download files efficiently.

## Available Tools
- aria2c: For general file downloads
- gallery-dl: For image galleries
- yt-dlp: For videos

## Workflow
1. When I give you a URL, identify the type
2. Choose the appropriate tool
3. Run the download command
4. Organize files in ~/Downloads/[date]/

## Example Commands
```bash
aria2c -d ~/Downloads/2024-08-24/ https://example.com/file.pdf
gallery-dl -d ~/Downloads/2024-08-24/images/ https://imgur.com/gallery/xyz
yt-dlp -o "~/Downloads/2024-08-24/videos/%(title)s.%(ext)s" https://youtube.com/watch?v=abc
```
```

### 3. Build Mini Git Agent
```python
# mini_git_agent.py
import click
import requests
import os

@click.command()
@click.argument('repo_url')
@click.option('--save', default='./repos', help='Where to save')
def analyze_repo(repo_url, save):
    """Simple repository analyzer"""
    
    # Extract owner/repo from URL
    parts = repo_url.split('/')
    owner = parts[-2]
    repo = parts[-1].replace('.git', '')
    
    # Get README via API
    api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        readme = response.json()
        content = requests.get(readme['download_url']).text
        
        # Save to file
        filename = f"{save}/{repo}_README.md"
        with open(filename, 'w') as f:
            f.write(content)
        
        click.echo(f"✅ Saved README to {filename}")
        click.echo(f"📊 Size: {len(content)} characters")
    else:
        click.echo("❌ Could not fetch README")

if __name__ == '__main__':
    analyze_repo()
```

## 🔗 Resources to Explore

1. **Click Documentation**: https://click.palletsprojects.com/
2. **GitIngest Tool**: https://github.com/cyclotruc/gitingest
3. **Awesome CLI Tools**: https://github.com/agarrharr/awesome-cli-apps
4. **Claude.md Best Practices**: Search for "BMAD method context engineering"

## 💭 Personal Implementation Ideas

### My Daily Workflow Agent
- Morning: Check emails, calendar, news
- Coding: Auto-setup development environment
- Research: Extract and summarize articles
- Evening: Generate daily report

### Project Ideas
1. **PDF Research Agent**: Extract, summarize, organize PDFs
2. **Code Review Agent**: Analyze PRs, suggest improvements
3. **Learning Agent**: Track progress, suggest next topics
4. **Writing Agent**: Research, outline, draft articles

## 🚀 Next Steps

1. **Today**: Install 3 CLI tools and test them
2. **Tomorrow**: Create first claude.md file
3. **This Week**: Build mini automation with Click
4. **Next Week**: Combine tools into workflow agent

## 📝 Questions to Explore

- How can MCP servers enhance these agents?
- What's the token limit for different Claude models?
- How to handle async operations in CLI tools?
- Best practices for error handling in agents?

---

**Remember**: Start simple, iterate often, document everything!