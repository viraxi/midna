# GitHub Labels for Midna

This document defines the labels used for issues and pull requests in the Midna repository.

## Type Labels

- **bug** - Something isn't working correctly
- **enhancement** - New feature or request
- **documentation** - Improvements or additions to documentation
- **question** - Further information is requested
- **security** - Security-related issues

## Status Labels

- **needs-triage** - Needs initial review and categorization
- **in-progress** - Currently being worked on
- **blocked** - Blocked by another issue or external factor
- **needs-feedback** - Waiting for feedback from reporter or community
- **needs-review** - Awaiting code review

## Priority Labels

- **priority: critical** - Critical issue requiring immediate attention
- **priority: high** - High priority issue
- **priority: medium** - Medium priority issue
- **priority: low** - Low priority issue

## Complexity Labels

- **good first issue** - Good for newcomers
- **help wanted** - Extra attention is needed
- **easy** - Easy to implement
- **medium** - Moderate complexity
- **hard** - Complex implementation required

## Component Labels

- **component: cli** - Related to CLI interface
- **component: discovery** - Related to auto-discovery
- **component: parser** - Related to requirements parsing
- **component: installer** - Related to package installation
- **component: tests** - Related to testing
- **component: ci-cd** - Related to CI/CD workflows

## Resolution Labels

- **wontfix** - This will not be worked on
- **duplicate** - This issue or pull request already exists
- **invalid** - This doesn't seem right
- **stale** - No recent activity

## Special Labels

- **breaking-change** - Introduces breaking changes
- **dependencies** - Pull requests that update dependencies
- **performance** - Performance improvements
- **refactor** - Code refactoring without feature changes

## Creating Labels

Use these commands to create labels via GitHub CLI:

```bash
# Type labels
gh label create "bug" --description "Something isn't working correctly" --color "d73a4a"
gh label create "enhancement" --description "New feature or request" --color "a2eeef"
gh label create "documentation" --description "Improvements or additions to documentation" --color "0075ca"
gh label create "question" --description "Further information is requested" --color "d876e3"
gh label create "security" --description "Security-related issues" --color "ee0701"

# Status labels
gh label create "needs-triage" --description "Needs initial review and categorization" --color "fbca04"
gh label create "in-progress" --description "Currently being worked on" --color "0e8a16"
gh label create "blocked" --description "Blocked by another issue or external factor" --color "b60205"
gh label create "needs-feedback" --description "Waiting for feedback from reporter or community" --color "d4c5f9"
gh label create "needs-review" --description "Awaiting code review" --color "fbca04"

# Priority labels
gh label create "priority: critical" --description "Critical issue requiring immediate attention" --color "b60205"
gh label create "priority: high" --description "High priority issue" --color "ff9800"
gh label create "priority: medium" --description "Medium priority issue" --color "fbca04"
gh label create "priority: low" --description "Low priority issue" --color "0e8a16"

# Complexity labels
gh label create "good first issue" --description "Good for newcomers" --color "7057ff"
gh label create "help wanted" --description "Extra attention is needed" --color "008672"
gh label create "easy" --description "Easy to implement" --color "c2e0c6"
gh label create "medium" --description "Moderate complexity" --color "fef2c0"
gh label create "hard" --description "Complex implementation required" --color "f9d0c4"

# Component labels
gh label create "component: cli" --description "Related to CLI interface" --color "5319e7"
gh label create "component: discovery" --description "Related to auto-discovery" --color "5319e7"
gh label create "component: parser" --description "Related to requirements parsing" --color "5319e7"
gh label create "component: installer" --description "Related to package installation" --color "5319e7"
gh label create "component: tests" --description "Related to testing" --color "5319e7"
gh label create "component: ci-cd" --description "Related to CI/CD workflows" --color "5319e7"

# Resolution labels
gh label create "wontfix" --description "This will not be worked on" --color "ffffff"
gh label create "duplicate" --description "This issue or pull request already exists" --color "cfd3d7"
gh label create "invalid" --description "This doesn't seem right" --color "e4e669"
gh label create "stale" --description "No recent activity" --color "eeeeee"

# Special labels
gh label create "breaking-change" --description "Introduces breaking changes" --color "d93f0b"
gh label create "dependencies" --description "Pull requests that update dependencies" --color "0366d6"
gh label create "performance" --description "Performance improvements" --color "1d76db"
gh label create "refactor" --description "Code refactoring without feature changes" --color "fbca04"
```

## Label Usage Guidelines

### For Issues

- Always add at least one **type label** (bug, enhancement, etc.)
- Add a **status label** to track progress
- Add **priority** if urgent
- Add **complexity** to help contributors choose issues
- Add relevant **component labels**

### For Pull Requests

- Add **type label** based on the changes
- Add **component labels** for affected areas
- Add **breaking-change** if applicable
- Status labels are automatically managed by reviews

### Automation

Consider using GitHub Actions to automatically:
- Add "needs-triage" to new issues
- Add "needs-review" to new PRs
- Add "stale" to inactive issues/PRs
- Update status labels based on PR reviews
