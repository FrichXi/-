# CLAUDE.md - AI Assistant Guide

This document provides comprehensive guidance for AI assistants (like Claude) working with this codebase. It outlines the repository structure, development workflows, coding conventions, and best practices to follow.

## Table of Contents

1. [Repository Overview](#repository-overview)
2. [Repository Structure](#repository-structure)
3. [Development Workflow](#development-workflow)
4. [Git Operations](#git-operations)
5. [Code Conventions](#code-conventions)
6. [Task Approach Guidelines](#task-approach-guidelines)
7. [File Operations](#file-operations)
8. [Testing and Quality Assurance](#testing-and-quality-assurance)
9. [Documentation Standards](#documentation-standards)
10. [Common Pitfalls to Avoid](#common-pitfalls-to-avoid)

---

## Repository Overview

**Repository Name:** -
**Status:** Early stage / Minimal codebase
**Primary Purpose:** [To be determined as the project evolves]

### Current State
- Fresh repository with initial commit
- Minimal file structure
- Ready for development

---

## Repository Structure

```
/
├── .git/           # Git version control
├── README.md       # Project documentation
└── CLAUDE.md       # This file - AI assistant guide
```

### Key Directories (to be created as needed)
- `/src/` - Source code
- `/tests/` - Test files
- `/docs/` - Additional documentation
- `/scripts/` - Utility scripts
- `/config/` - Configuration files

---

## Development Workflow

### Branch Strategy

**Feature Branches:**
- All development should occur on feature branches
- Branch naming convention: `claude/<description>-<session-id>`
- Example: `claude/claude-md-miwtl5bblg1805c7-01LSSBjmH7R7pvmEnh3kSfrz`

**Important Rules:**
1. **NEVER** push directly to main/master branches
2. **ALWAYS** develop on designated feature branches
3. **CREATE** branches locally if they don't exist
4. **VERIFY** branch name starts with `claude/` and ends with session ID before pushing

### Commit Strategy

**Commit Message Format:**
```
<type>: <concise description>

[Optional detailed explanation of changes]
```

**Commit Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks
- `style:` - Code style changes (formatting, etc.)

**Best Practices:**
- Commit logical units of work
- Write clear, descriptive commit messages
- Focus on "why" rather than "what" in descriptions
- Avoid empty commits
- Use heredoc for multi-line commit messages

**Example:**
```bash
git commit -m "$(cat <<'EOF'
feat: Add user authentication system

Implements JWT-based authentication with refresh tokens.
Includes middleware for protected routes.
EOF
)"
```

---

## Git Operations

### Pushing Changes

**Standard Push Command:**
```bash
git push -u origin <branch-name>
```

**Critical Requirements:**
- Branch MUST start with `claude/`
- Branch MUST end with matching session ID
- Push will fail with 403 if naming convention is not followed

**Retry Logic for Network Failures:**
If push fails due to network errors, retry up to 4 times with exponential backoff:
- 1st retry: wait 2 seconds
- 2nd retry: wait 4 seconds
- 3rd retry: wait 8 seconds
- 4th retry: wait 16 seconds

### Fetching and Pulling

**Fetch Specific Branch:**
```bash
git fetch origin <branch-name>
```

**Pull Changes:**
```bash
git pull origin <branch-name>
```

Apply the same retry logic for network failures.

### Git Safety Protocol

**NEVER:**
- Update git config without permission
- Run destructive operations (force push, hard reset) without explicit user request
- Skip hooks (--no-verify, --no-gpg-sign) without permission
- Force push to main/master branches
- Amend commits unless explicitly requested or fixing pre-commit hook changes

**ALWAYS:**
- Check authorship before amending: `git log -1 --format='%an %ae'`
- Verify branch is not pushed before amending
- Use pull requests for merging to protected branches

### Pre-commit Hook Handling

If a commit fails due to pre-commit hook modifications:
1. Verify it's safe to amend (check authorship and push status)
2. If safe: amend the commit
3. If not safe: create a new commit
4. Never amend other developers' commits

---

## Code Conventions

### General Principles

1. **Simplicity Over Complexity**
   - Avoid over-engineering
   - Only make requested changes
   - Keep solutions focused and minimal
   - Three similar lines > premature abstraction

2. **Security First**
   - Prevent command injection
   - Avoid XSS vulnerabilities
   - Prevent SQL injection
   - Follow OWASP Top 10 guidelines
   - Fix insecure code immediately

3. **No Unnecessary Additions**
   - Don't add features beyond the request
   - Don't refactor unrelated code
   - Don't add comments to unchanged code
   - Don't add error handling for impossible scenarios
   - Only validate at system boundaries

4. **Clean Deletions**
   - Delete unused code completely
   - No backwards-compatibility hacks
   - No `_unused` variable renaming
   - No `// removed` comments
   - No re-exporting unused types

### Code Style

**File Organization:**
- Logical grouping of related functionality
- Clear separation of concerns
- Consistent file naming conventions

**Naming Conventions:**
- Use descriptive, meaningful names
- Follow language-specific conventions
- Be consistent within the codebase

**Comments:**
- Only add where logic isn't self-evident
- Explain "why" not "what"
- Keep comments up-to-date with code

**Error Handling:**
- Handle errors at appropriate boundaries
- Provide meaningful error messages
- Don't catch errors you can't handle

---

## Task Approach Guidelines

### Before Starting Any Task

1. **Read Before Modifying**
   - NEVER propose changes without reading the file first
   - Understand existing code before suggesting modifications
   - Use Read tool to examine files

2. **Plan Complex Tasks**
   - Use TodoWrite tool for multi-step tasks (3+ steps)
   - Break down large tasks into manageable pieces
   - Track progress throughout execution

3. **Understand Context**
   - Explore related code
   - Check for similar implementations
   - Understand dependencies

### Task Execution

**For Bug Fixes:**
1. Reproduce and understand the bug
2. Identify root cause
3. Implement minimal fix
4. Verify fix works
5. Don't refactor surrounding code

**For New Features:**
1. Clarify requirements if ambiguous
2. Check for existing similar features
3. Plan implementation approach
4. Implement in logical steps
5. Test functionality

**For Refactoring:**
1. Understand current implementation
2. Identify specific improvements
3. Refactor incrementally
4. Ensure behavior is preserved
5. Update tests if needed

**For Code Exploration:**
1. Use Task tool with Explore agent for broad searches
2. Use Grep for specific code patterns
3. Use Read for examining specific files
4. Document findings clearly

### Tool Usage Priorities

1. **File Operations:**
   - Read tool (not cat/head/tail)
   - Edit tool (not sed/awk)
   - Write tool (not echo/heredoc)

2. **Search Operations:**
   - Grep for content search (not bash grep)
   - Glob for file patterns (not find/ls)
   - Task tool with Explore agent for broad exploration

3. **Multiple Operations:**
   - Run independent operations in parallel
   - Use sequential operations for dependencies
   - Use && for dependent command chains

---

## File Operations

### Reading Files

**Use Read Tool:**
```
Read tool for any file reading operations
```

**Never Use:**
- `cat`, `head`, `tail` via Bash
- Multiple reads when one will suffice

**Best Practices:**
- Read entire files when possible
- Use offset/limit only for very large files
- Read multiple files in parallel when independent

### Editing Files

**Use Edit Tool:**
```
Edit tool for precise string replacements
```

**Requirements:**
- MUST read file before editing
- Preserve exact indentation
- Make old_string unique enough
- Use replace_all for renaming across file

**Never Use:**
- `sed`, `awk`, or other bash text processors
- Edit without reading first

### Writing Files

**Use Write Tool:**
```
Write tool for creating new files
```

**Important:**
- ALWAYS prefer editing existing files
- NEVER create files unless absolutely necessary
- Read existing file first if overwriting
- Don't create markdown/documentation proactively

### File Creation Guidelines

**When to Create New Files:**
- Explicitly requested by user
- Absolutely necessary for the task
- No existing file can be adapted

**When NOT to Create Files:**
- Documentation (unless requested)
- README files (unless requested)
- Helper files for one-time operations

---

## Testing and Quality Assurance

### Testing Approach

1. **Write Tests When:**
   - Adding new functionality
   - Fixing bugs (regression tests)
   - Explicitly requested

2. **Test Coverage:**
   - Focus on critical paths
   - Test edge cases
   - Don't test trivial code

3. **Running Tests:**
   - Run tests before committing
   - Fix all failing tests
   - Don't mark tasks complete if tests fail

### Code Quality

**Before Committing:**
1. Review changes with `git diff`
2. Run tests if they exist
3. Check for security vulnerabilities
4. Verify code follows conventions
5. Ensure no unnecessary changes included

**Quality Checklist:**
- [ ] Code is secure
- [ ] Tests pass
- [ ] No over-engineering
- [ ] Only requested changes included
- [ ] Documentation updated if needed

---

## Documentation Standards

### When to Document

**DO Document:**
- New features (in code and/or separate docs)
- Complex algorithms
- API changes
- Configuration options
- When explicitly requested

**DON'T Document:**
- Self-evident code
- Unchanged code
- Obvious functionality
- Unless specifically requested

### Documentation Format

**Code Comments:**
```
// Explain WHY, not WHAT
// Good: Calculate using Haversine formula for accuracy
// Bad: Calculate distance between coordinates
```

**README Updates:**
- Update when adding features
- Keep sections focused
- Use clear examples
- Maintain consistency

**CLAUDE.md Updates:**
- Update when conventions change
- Add new patterns discovered
- Document project-specific workflows
- Keep this file current

---

## Common Pitfalls to Avoid

### What NOT to Do

1. **Over-Engineering**
   - ❌ Creating abstractions for single use
   - ❌ Adding features not requested
   - ❌ Designing for hypothetical requirements
   - ❌ Premature optimization

2. **Unnecessary Changes**
   - ❌ Refactoring unrelated code
   - ❌ Adding comments to unchanged code
   - ❌ "Improving" code beyond the request
   - ❌ Adding docstrings unnecessarily

3. **Security Issues**
   - ❌ Command injection vulnerabilities
   - ❌ XSS vulnerabilities
   - ❌ SQL injection vulnerabilities
   - ❌ Insecure defaults

4. **Git Mistakes**
   - ❌ Pushing to wrong branch
   - ❌ Force pushing to protected branches
   - ❌ Amending others' commits
   - ❌ Skipping hooks without permission

5. **Tool Misuse**
   - ❌ Using bash for file operations
   - ❌ Using echo/cat for communication
   - ❌ Guessing file contents instead of reading
   - ❌ Not using specialized tools

### Best Practices Summary

✅ Read files before modifying
✅ Use specialized tools for operations
✅ Plan complex tasks with TodoWrite
✅ Keep changes minimal and focused
✅ Write secure code
✅ Follow git conventions strictly
✅ Test changes before committing
✅ Document when appropriate
✅ Run independent operations in parallel
✅ Be honest about limitations and uncertainties

---

## Communication Guidelines

### Tone and Style

- Be concise and direct
- Avoid unnecessary emojis (unless requested)
- Use markdown for formatting
- Focus on technical accuracy
- Provide objective guidance

### Providing Information

**DO:**
- State facts objectively
- Admit when uncertain
- Investigate before confirming
- Provide direct, honest feedback
- Disagree when necessary for correctness

**DON'T:**
- Use excessive praise ("You're absolutely right!")
- Validate incorrect beliefs to be agreeable
- Use superlatives unnecessarily
- Provide time estimates for tasks
- Make assumptions without verification

### Code References

When referencing code, use this format:
```
file_path:line_number
```

Example: "The error handling is in src/services/process.ts:712"

---

## Maintenance

### Keeping CLAUDE.md Updated

**Update When:**
- New patterns emerge in the codebase
- Conventions change
- Project structure evolves
- New workflows are established
- Common issues are discovered

**How to Update:**
1. Read current version first
2. Make targeted updates
3. Keep format consistent
4. Update table of contents if needed
5. Commit with clear message

### Version History

- **v1.0** - Initial comprehensive guide created for minimal repository

---

## Quick Reference

### Essential Commands

```bash
# Check status
git status

# Create and switch to feature branch
git checkout -b claude/<description>-<session-id>

# Stage changes
git add <files>

# Commit with message
git commit -m "type: description"

# Push to remote
git push -u origin <branch-name>

# View recent commits
git log --oneline -10

# View changes
git diff
```

### Tool Priority

1. **Read** for viewing files
2. **Edit** for modifying files
3. **Write** for new files (rarely)
4. **Grep** for searching code
5. **Glob** for finding files
6. **Bash** for system operations only
7. **Task** for complex multi-step operations

---

## Getting Help

If you encounter situations not covered in this guide:
1. Ask the user for clarification
2. Research the codebase for similar patterns
3. Follow general best practices
4. Document new patterns discovered
5. Update this file with new learnings

---

**Last Updated:** 2025-12-08
**Maintained By:** AI Assistants working with this repository
**Purpose:** Provide comprehensive guidance for consistent, high-quality development
