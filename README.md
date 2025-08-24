# 🎓 Claude Learning System

A personal learning framework for mastering Claude Code, AI agents, context engineering, and MCP through structured video analysis and practical implementations.

## 🎯 Purpose

Transform YouTube video transcripts about AI coding into:
- Structured, actionable learning notes
- Practical code implementations
- Connected knowledge graph
- Personal agent library

## 🚀 Quick Start

```bash
# 1. Get transcript from any video
# Use youtube-transcript-analyzer to get transcript first

# 2. Extract learning
python extractors/learning_extractor.py path/to/transcript.txt

# 3. Build implementation from learnings
python implementations/create_from_notes.py my_notes/latest.md
```

## 📂 Structure

```
claude-learning-system/
├── extractors/              # Tools to analyze content
│   ├── learning_extractor.py
│   ├── concept_mapper.py
│   └── quiz_generator.py
├── templates/               # Reusable templates
│   ├── claude.md
│   ├── learning_template.md
│   └── project_template.py
├── my_notes/               # Your extracted learnings
│   ├── by_date/
│   ├── by_topic/
│   └── INDEX.md
├── implementations/        # Code you've built
│   ├── agents/
│   ├── tools/
│   └── workflows/
└── knowledge_graph/       # Connected concepts
    ├── concepts.json
    ├── relationships.md
    └── learning_path.md
```

## 🛠️ Tools Included

### Learning Extractor
Analyzes video transcripts to extract:
- Key concepts and definitions
- Tools and commands mentioned
- Practical implementations
- Action items and experiments

### Concept Mapper (Coming Soon)
- Links related concepts
- Builds knowledge graph
- Suggests learning paths

### Implementation Generator (Coming Soon)
- Creates boilerplate from concepts
- Generates test cases
- Provides variations to try

## 📚 Learning Workflow

### Step 1: Capture
Get transcripts from videos about Claude Code, MCP, agents, etc.

### Step 2: Extract
```bash
python extractors/learning_extractor.py transcript.txt
```

### Step 3: Implement
Build small projects based on extracted concepts

### Step 4: Connect
Link new knowledge to existing concepts

### Step 5: Apply
Use learnings in real projects

## 🎯 Focus Areas

- **Claude Code**: Advanced usage, patterns, best practices
- **Context Engineering**: BMAD method, prompt optimization
- **MCP (Model Context Protocol)**: Server creation, integration
- **AI Agents**: Tool use, orchestration, workflows
- **CLI Integration**: Automation with terminal tools

## 📈 Progress Tracking

Track your learning journey:
- Videos analyzed: `my_notes/INDEX.md`
- Concepts mastered: `knowledge_graph/concepts.json`
- Implementations built: `implementations/README.md`
- Agents created: `implementations/agents/`

## 🔗 Related Projects

- [YouTube Transcript Analyzer](https://github.com/nelgonzalez1/-youtube-transcript-analyzer) - Extract transcripts
- [Claude Code Docs](https://claude.ai/code) - Official documentation
- [MCP Specification](https://github.com/anthropics/mcp) - Protocol details

## 💡 Philosophy

> "Learn by doing. Every concept should result in working code."

The goal isn't to memorize, but to build a practical toolkit of patterns and implementations you can immediately use in your daily workflow.

## 🚀 Next Steps

1. Watch a Claude Code video
2. Extract transcript with youtube-transcript-analyzer
3. Run learning_extractor on it
4. Build something from what you learned
5. Share your implementations!

---

**Note**: This is a personal learning system. Customize it to match your learning style and goals!