# Contributing to Claude Plugins

Thank you for considering contributing to this collection of Claude Code plugins! This document provides guidelines and best practices for contributions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yonggao/claude-plugins.git
   cd claude-plugins
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/my-new-skill
   ```

## Types of Contributions

### 1. New Skills

Skills are reusable capabilities that extend Claude Code's functionality.

**Requirements for new skills:**
- Must include a `SKILL.md` file with proper frontmatter
- Should be well-documented with examples
- Must handle dependencies gracefully
- Should include error handling
- Must work cross-platform (macOS/Linux) when possible

**Skill Structure:**
```
skills/my-skill/
├── SKILL.md           # Required: Skill definition and docs
├── README.md          # Optional: Extended documentation
├── implementation.*   # Your code (Python, JS, Shell, etc.)
├── requirements.txt   # For Python dependencies
├── package.json       # For Node.js dependencies
└── examples/          # Optional: Example files
```

**SKILL.md Template:**
```markdown
---
name: my-skill-name
description: Brief description of what this skill does. Use this skill when...
---

# Skill Name

## When to Use This Skill

- Use case 1
- Use case 2

## Features

- Feature 1
- Feature 2

## Usage

\`\`\`bash
# Example command
\`\`\`

## Dependencies

- List dependencies
- Installation instructions

## Examples

Provide working examples
```

### 2. Statusline Improvements

Contributions to the statusline script should:
- Maintain backward compatibility
- Be performance-conscious (< 100ms execution)
- Handle missing dependencies gracefully
- Document new features

### 3. Documentation

Documentation improvements are always welcome:
- Fix typos
- Improve clarity
- Add examples
- Update outdated information

## Development Guidelines

### Code Style

**Python:**
- Follow PEP 8
- Use type hints where appropriate
- Include docstrings for functions/classes
- Keep dependencies minimal

**Shell Scripts:**
- Use `#!/bin/bash` shebang
- Include comments for complex logic
- Handle errors with `set -e` or explicit checks
- Quote variables: `"$variable"`

**JavaScript/Node:**
- Use ES6+ features
- Include JSDoc comments
- Use async/await over callbacks

### Testing

Before submitting:

1. **Test your skill locally:**
   ```bash
   # Copy to Claude directory
   cp -r skills/my-skill ~/.claude/skills/

   # Test with Claude Code
   claude
   ```

2. **Verify all dependencies are documented**

3. **Test error handling:**
   - Missing dependencies
   - Invalid inputs
   - File not found scenarios

4. **Cross-platform testing** (if possible)

### Documentation Standards

All contributions should include:

1. **Clear descriptions** of what the code does
2. **Usage examples** with expected output
3. **Dependency requirements** with installation instructions
4. **Error handling** documentation
5. **Performance characteristics** if relevant

## Pull Request Process

1. **Update documentation:**
   - Add your skill to main README.md
   - Include comprehensive SKILL.md
   - Update CHANGELOG.md if exists

2. **Commit message format:**
   ```
   type(scope): brief description

   Longer description if needed

   - Bullet points for details
   ```

   Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

   Examples:
   ```
   feat(skills): add image-optimizer skill
   fix(statusline): handle missing git repository
   docs(readme): update installation instructions
   ```

3. **Create pull request:**
   - Use a clear, descriptive title
   - Reference any related issues
   - Describe what your changes do
   - Include screenshots/examples if applicable

4. **Respond to feedback:**
   - Be open to suggestions
   - Make requested changes promptly
   - Ask questions if unclear

## Skill Ideas

Looking for contribution ideas? Consider:

- **File conversion skills**: DOCX to Markdown, SVG to PNG, etc.
- **Data processing**: CSV analysis, JSON formatting, etc.
- **Integration skills**: GitHub API, Jira, Slack, etc.
- **Development tools**: Code formatters, linters, dependency checkers
- **Documentation**: API doc generators, changelog creators
- **Testing**: Test generators, coverage reporters

## Community Guidelines

### Be Respectful

- Use welcoming and inclusive language
- Respect differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community

### Quality Over Quantity

- One well-documented skill is better than several half-finished ones
- Test thoroughly before submitting
- Keep code clean and maintainable

### Ask Questions

- Unsure about something? Open an issue to discuss
- Better to ask before spending time on unwanted changes

## Getting Help

- **Questions about Claude Code**: [Official Documentation](https://docs.claude.com/)
- **Skill development**: Open a Discussion on GitHub
- **Bug reports**: Open an Issue with reproduction steps

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md (if we create one)
- Mentioned in release notes for significant contributions
- Credited in skill documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License (same as the project).

## Additional Resources

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Claude Code Skills Guide](https://docs.claude.com/en/docs/claude-code/skills)
- [MCP Protocol](https://modelcontextprotocol.io/)

## Example Contribution Workflow

```bash
# 1. Fork and clone
git clone https://github.com/yonggao/claude-plugins.git
cd claude-plugins

# 2. Create branch
git checkout -b feature/awesome-skill

# 3. Create your skill
mkdir -p skills/awesome-skill
# ... create files ...

# 4. Test locally
cp -r skills/awesome-skill ~/.claude/skills/
# Test with Claude Code

# 5. Document
# Update README.md, create SKILL.md, etc.

# 6. Commit
git add skills/awesome-skill
git add README.md
git commit -m "feat(skills): add awesome-skill for data processing"

# 7. Push
git push origin feature/awesome-skill

# 8. Create PR on GitHub
```

---

Thank you for contributing to make Claude Code more powerful and useful! 🚀
