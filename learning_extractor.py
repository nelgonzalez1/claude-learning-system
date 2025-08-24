#!/usr/bin/env python3
"""
Learning Extractor for Claude Code Video Transcripts
Automatically extracts key learnings, examples, and action items
"""

import json
import re
import os
from datetime import datetime
from typing import Dict, List, Any
import argparse

class LearningExtractor:
    def __init__(self):
        self.patterns = {
            'tools': r'(?:tool|CLI|command|program|application)s?\s+(?:like|called|named)?\s+(\w+)',
            'concepts': r'(?:concept|idea|approach|method|framework|pattern)s?\s+(?:is|are|called)?\s+([^.]+)',
            'commands': r'(?:run|execute|use|call)\s+(?:the\s+)?(?:command\s+)?([`"\']?)([^`"\']+)\1',
            'workflows': r'(?:workflow|process|steps?|procedure)s?\s+(?:is|are|works?)?\s+([^.]+)',
            'time_estimates': r'(\d+)\s+(?:hours?|minutes?|days?)\s+(?:to|of)\s+(?:build|work|create)',
        }
        
    def extract_from_transcript(self, transcript_path: str) -> Dict[str, Any]:
        """Extract structured learning from transcript"""
        with open(transcript_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract video metadata
        metadata = self.extract_metadata(content)
        
        # Extract learning components
        learning = {
            'metadata': metadata,
            'key_concepts': self.extract_concepts(content),
            'tools_mentioned': self.extract_tools(content),
            'commands_shown': self.extract_commands(content),
            'workflows': self.extract_workflows(content),
            'code_examples': self.extract_code_blocks(content),
            'action_items': self.generate_action_items(content),
            'implementation_ideas': self.generate_implementation_ideas(content),
        }
        
        return learning
    
    def extract_metadata(self, content: str) -> Dict[str, str]:
        """Extract video metadata from transcript header"""
        metadata = {}
        
        # Extract URL
        url_match = re.search(r'\*\*Video URL:\*\*\s+(https?://[^\s]+)', content)
        if url_match:
            metadata['url'] = url_match.group(1)
            metadata['video_id'] = url_match.group(1).split('v=')[-1].split('&')[0]
        
        # Extract duration
        duration_match = re.search(r'\*\*Duration:\*\*\s+(\d+:\d+)', content)
        if duration_match:
            metadata['duration'] = duration_match.group(1)
        
        # Extract date
        date_match = re.search(r'extracted on\s+(\d{4}-\d{2}-\d{2})', content)
        if date_match:
            metadata['extracted_date'] = date_match.group(1)
        
        return metadata
    
    def extract_concepts(self, content: str) -> List[Dict[str, str]]:
        """Extract key concepts and their explanations"""
        concepts = []
        
        # Key phrases that indicate important concepts
        concept_indicators = [
            'AI agents', 'context engineering', 'MCP', 'claude code',
            'bash tool', 'CLI', 'workflow', 'automation', 'framework',
            'integration', 'token', 'prompt', 'agent', 'tool'
        ]
        
        for indicator in concept_indicators:
            if indicator.lower() in content.lower():
                # Find sentences containing the concept
                sentences = re.findall(
                    rf'[^.]*{re.escape(indicator)}[^.]*\.',
                    content,
                    re.IGNORECASE
                )
                
                if sentences:
                    concepts.append({
                        'concept': indicator,
                        'mentions': len(sentences),
                        'example': sentences[0].strip() if sentences else ""
                    })
        
        return sorted(concepts, key=lambda x: x['mentions'], reverse=True)[:10]
    
    def extract_tools(self, content: str) -> List[Dict[str, str]]:
        """Extract tools and their purposes"""
        tools = []
        tool_patterns = [
            r'(\w+(?:dl|cli|agent)?)\s+(?:is\s+)?a\s+(?:command|tool|program)',
            r'tool\s+(?:called|named)\s+(\w+)',
            r'using\s+(\w+)\s+(?:tool|command|CLI)',
        ]
        
        found_tools = set()
        for pattern in tool_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            found_tools.update(matches)
        
        # Known tools from the transcript
        known_tools = {
            'gallery-dl': 'Downloads images from galleries',
            'aria2': 'Fast parallel downloader',
            'yt-dlp': 'YouTube video downloader',
            'gitingest': 'Converts repos to LLM-readable format',
            'click': 'Python CLI framework',
            'claude code': 'AI coding assistant',
            'cursor': 'AI-powered code editor',
        }
        
        for tool in found_tools:
            tool_lower = tool.lower()
            if tool_lower in known_tools:
                tools.append({
                    'name': tool,
                    'purpose': known_tools[tool_lower],
                    'category': 'CLI Tool'
                })
        
        return tools
    
    def extract_commands(self, content: str) -> List[str]:
        """Extract actual commands shown in the transcript"""
        commands = []
        
        # Look for command patterns
        command_patterns = [
            r'`([^`]+)`',  # Backtick commands
            r'(?:run|execute)\s+([a-z\-]+\s+[^\n]+)',  # Run/execute patterns
            r'^\$\s+(.+)$',  # Shell prompt commands
        ]
        
        for pattern in command_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            commands.extend(matches)
        
        # Clean and deduplicate
        commands = list(set([cmd.strip() for cmd in commands if len(cmd) < 100]))
        
        return commands[:20]  # Top 20 commands
    
    def extract_workflows(self, content: str) -> List[Dict[str, str]]:
        """Extract workflow descriptions"""
        workflows = []
        
        # Look for numbered steps or workflow descriptions
        workflow_sections = re.findall(
            r'(?:workflow|process|steps?).*?:\s*\n((?:\d+\..*?\n)+)',
            content,
            re.IGNORECASE | re.DOTALL
        )
        
        for section in workflow_sections:
            steps = re.findall(r'\d+\.\s*(.+)', section)
            if steps:
                workflows.append({
                    'name': 'Extracted Workflow',
                    'steps': steps
                })
        
        return workflows
    
    def extract_code_blocks(self, content: str) -> List[Dict[str, str]]:
        """Extract code examples from transcript"""
        code_blocks = []
        
        # Look for code-like patterns
        code_patterns = [
            r'```(\w*)\n(.*?)```',  # Markdown code blocks
            r'(?:import|from|def|class|function)\s+\w+',  # Code keywords
        ]
        
        for match in re.finditer(code_patterns[0], content, re.DOTALL):
            language = match.group(1) or 'python'
            code = match.group(2)
            
            if code.strip():
                code_blocks.append({
                    'language': language,
                    'code': code.strip(),
                    'lines': len(code.strip().split('\n'))
                })
        
        return code_blocks
    
    def generate_action_items(self, content: str) -> List[str]:
        """Generate actionable tasks from the content"""
        action_items = []
        
        # Extract mentioned tools to try
        tools = self.extract_tools(content)
        for tool in tools[:3]:  # Top 3 tools
            action_items.append(f"Install and test {tool['name']}: {tool['purpose']}")
        
        # Look for explicit suggestions
        suggestion_patterns = [
            r'you (?:should|can|could) (\w+[^.]+)',
            r'try (?:to\s+)?(\w+[^.]+)',
            r'(?:build|create|make) (?:a\s+)?(\w+[^.]+)',
        ]
        
        for pattern in suggestion_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches[:2]:  # Limit to 2 per pattern
                if len(match) < 100:  # Reasonable length
                    action_items.append(f"Try to {match.strip()}")
        
        # Add standard learning actions
        action_items.extend([
            "Create a claude.md file for your most common workflow",
            "Build a simple CLI tool using Click framework",
            "Test bash commands through Claude Code",
        ])
        
        return list(set(action_items))[:10]  # Top 10 unique items
    
    def generate_implementation_ideas(self, content: str) -> List[Dict[str, str]]:
        """Generate practical implementation ideas"""
        ideas = []
        
        # Based on concepts found, suggest implementations
        if 'download' in content.lower():
            ideas.append({
                'name': 'Personal Download Manager',
                'description': 'Agent that organizes downloads by type and date',
                'difficulty': 'Easy',
                'time_estimate': '1 hour'
            })
        
        if 'git' in content.lower() or 'repository' in content.lower():
            ideas.append({
                'name': 'Repository Documentation Agent',
                'description': 'Automatically extract and summarize repo documentation',
                'difficulty': 'Medium',
                'time_estimate': '2-3 hours'
            })
        
        if 'workflow' in content.lower():
            ideas.append({
                'name': 'Daily Workflow Automator',
                'description': 'Agent that handles repetitive daily tasks',
                'difficulty': 'Medium',
                'time_estimate': '2 hours'
            })
        
        # Add generic ideas
        ideas.extend([
            {
                'name': 'Learning Notes Organizer',
                'description': 'Automatically organize and index learning materials',
                'difficulty': 'Easy',
                'time_estimate': '1 hour'
            },
            {
                'name': 'Code Snippet Manager',
                'description': 'Store and retrieve useful code snippets',
                'difficulty': 'Easy',
                'time_estimate': '30 minutes'
            }
        ])
        
        return ideas[:5]  # Top 5 ideas
    
    def save_learning_notes(self, learning: Dict[str, Any], output_path: str):
        """Save extracted learning as structured markdown"""
        
        video_id = learning['metadata'].get('video_id', 'unknown')
        date = datetime.now().strftime('%Y-%m-%d')
        
        output = f"""# 📚 Learning Notes: Video Analysis
**Generated**: {date}
**Video ID**: {video_id}
**URL**: {learning['metadata'].get('url', 'N/A')}

## 🎯 Key Concepts ({len(learning['key_concepts'])} found)
"""
        
        for concept in learning['key_concepts'][:5]:
            output += f"- **{concept['concept']}** ({concept['mentions']} mentions)\n"
            if concept['example']:
                output += f"  - Example: \"{concept['example'][:100]}...\"\n"
        
        output += f"\n## 🛠️ Tools & Technologies ({len(learning['tools_mentioned'])} found)\n"
        for tool in learning['tools_mentioned']:
            output += f"- **{tool['name']}**: {tool['purpose']}\n"
        
        output += f"\n## 💻 Commands to Try ({len(learning['commands_shown'])} found)\n```bash\n"
        for cmd in learning['commands_shown'][:10]:
            output += f"{cmd}\n"
        output += "```\n"
        
        if learning['workflows']:
            output += f"\n## 📋 Workflows Identified\n"
            for workflow in learning['workflows']:
                output += f"### {workflow['name']}\n"
                for i, step in enumerate(workflow['steps'], 1):
                    output += f"{i}. {step}\n"
        
        output += f"\n## ✅ Action Items\n"
        for item in learning['action_items']:
            output += f"- [ ] {item}\n"
        
        output += f"\n## 💡 Implementation Ideas\n"
        for idea in learning['implementation_ideas']:
            output += f"\n### {idea['name']}\n"
            output += f"- **Description**: {idea['description']}\n"
            output += f"- **Difficulty**: {idea['difficulty']}\n"
            output += f"- **Time Estimate**: {idea['time_estimate']}\n"
        
        # Save markdown
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)
        
        # Also save JSON for programmatic access
        json_path = output_path.replace('.md', '.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(learning, f, indent=2, ensure_ascii=False)
        
        print(f"Learning notes saved to: {output_path}")
        print(f"JSON data saved to: {json_path}")
        
        return output_path

def main():
    parser = argparse.ArgumentParser(description='Extract learning from video transcripts')
    parser.add_argument('transcript', help='Path to transcript file')
    parser.add_argument('--output', '-o', help='Output path for learning notes')
    parser.add_argument('--format', choices=['md', 'json', 'both'], default='both',
                       help='Output format (default: both)')
    
    args = parser.parse_args()
    
    # Initialize extractor
    extractor = LearningExtractor()
    
    # Extract learning
    print(f"Analyzing transcript: {args.transcript}")
    learning = extractor.extract_from_transcript(args.transcript)
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        # Create learning_notes directory if it doesn't exist
        os.makedirs('learning_notes', exist_ok=True)
        
        # Generate filename from date and video ID
        video_id = learning['metadata'].get('video_id', 'unknown')
        date = datetime.now().strftime('%Y%m%d')
        output_path = f"learning_notes/{date}_{video_id}_notes.md"
    
    # Save results
    extractor.save_learning_notes(learning, output_path)
    
    # Print summary
    print(f"\nExtraction Summary:")
    print(f"  - Concepts found: {len(learning['key_concepts'])}")
    print(f"  - Tools identified: {len(learning['tools_mentioned'])}")
    print(f"  - Commands extracted: {len(learning['commands_shown'])}")
    print(f"  - Action items: {len(learning['action_items'])}")
    print(f"  - Implementation ideas: {len(learning['implementation_ideas'])}")

if __name__ == '__main__':
    main()