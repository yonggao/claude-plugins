---
allowed-tools: Bash(find:*), Bash(ls:*), Bash(git:*), Read, Glob
description: Analyze team's git commit history across all repositories for activity, performance, and working areas per developer
---

# Team Git Analytics

Analyze the git commit history across all repositories in the current directory
to understand team activity patterns, individual developer contributions,
performance metrics, and working areas.

## Analysis Parameters

- **Time Period**: $ARGUMENTS (default: "90 days ago" if not specified)
- **Scope**: All subdirectories containing git repositories
- **Focus**: Developer-specific metrics, collaboration patterns, repository
  health

## Execution Instructions

Please perform a comprehensive git analysis following these steps:

### 1. Repository Discovery

First, discover all git repositories in the current directory and
subdirectories:

```bash
find . -maxdepth 2 -name ".git" -type d
```

Then list the subdirectories to identify repositories:

```bash
ls -la
```

### 2. Data Collection Phase

For each repository directory found, navigate to it and collect detailed git
data using the time period: **$ARGUMENTS** (or "90 days ago" if no arguments
provided).

For each repository, execute these git commands:

**Basic repository info:**

```bash
git status
git branch --show-current
```

**Commit statistics:**

```bash
git rev-list --count --since="90 days ago" HEAD
git shortlog --since="90 days ago" -sne
```

**Detailed commit history:**

```bash
git log --since="90 days ago" --pretty=format:"%H|%an|%ae|%ad|%s" --date=iso
```

**File change statistics:**

```bash
git log --since="90 days ago" --numstat --pretty=format:"%an|%ad" --date=short
```

**Most active files:**

```bash
git log --since="90 days ago" --name-only --pretty=format:
```

**Author activity:**

```bash
git log --since="90 days ago" --pretty=format:"%an"
```

### 3. Analysis Instructions

Based on the collected git data from all repositories, provide a comprehensive
analysis including:

#### Developer Profiles (per individual):

- **Commit Activity**: Total commits, commit frequency, timeline patterns
- **Code Changes**: Lines added/deleted, net contribution, change velocity
- **Working Areas**: Primary files/directories worked on, specialization areas
- **Collaboration**: Cross-repository contributions, patterns across repos
- **Commit Patterns**: Timing patterns, commit message analysis, work
  categorization

#### Repository Analysis:

- **Activity Level**: Commit frequency, contributor diversity, health score
- **Hot Spots**: Most active files and directories, maintenance areas
- **Collaboration**: Multi-contributor files, knowledge sharing indicators
- **Trends**: Growth patterns, contributor activity patterns

#### Team Insights:

- **Overall Velocity**: Team commit rate, productivity trends
- **Work Distribution**: Balance of contributions, specialization vs
  collaboration
- **Process Health**: Regular commit patterns, documentation updates
- **Recommendations**: Process improvements, resource allocation suggestions

### 4. Processing Instructions

Please analyze the time period specified in $ARGUMENTS (use "90 days ago" if no
arguments provided).

For each repository directory you find:

1. Navigate to the repository
2. Execute the git commands listed above
3. Collect and analyze the output
4. Build comprehensive developer and team insights

Focus especially on:

- Individual developer contribution patterns
- Cross-repository collaboration
- Working area specializations
- Team velocity and health metrics

### 4. Output Format

- All in Chinese
- Structure the analysis following 2025-08-15-云平台工程师日常工作分析.md as
  much as possible
- Detail analysis of each developer and team overall

### 5. Visualization Suggestions

Where helpful, suggest ways to visualize:

- Commit timeline patterns
- Code change distributions
- Collaboration networks
- Repository activity heat maps

## Expected Behavior

This command should automatically:

- ✅ Find all git repositories in subdirectories
- ✅ Handle missing or invalid git repositories gracefully
- ✅ Execute git commands safely with proper error handling
- ✅ Analyze both individual and team patterns
- ✅ Provide actionable insights for team improvement
- ✅ Support flexible time periods via arguments
- ✅ Present results in a clear, structured format

Use the time period specified in $ARGUMENTS, or default to "90 days ago" if no
arguments are provided.
