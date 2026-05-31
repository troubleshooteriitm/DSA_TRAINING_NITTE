"""
Git Workflow Practice
======================
Common git workflows documented as Python functions that print commands.
"""


def print_commands(title, commands):
    """Print a set of git commands with descriptions."""
    print(f"\n   {title}")
    print(f"  {'' * 55}")
    for cmd, desc in commands:
        print(f"  $ {cmd:<45} # {desc}")


print("=" * 60)
print("  GIT WORKFLOW REFERENCE")
print("=" * 60)

# 1. Initial Setup
print_commands("Initial Setup", [
    ("git config --global user.name 'Your Name'", "Set name"),
    ("git config --global user.email 'you@email.com'", "Set email"),
    ("git config --list", "View config"),
])

# 2. New Project
print_commands("Start New Project", [
    ("git init", "Initialize repo"),
    ("git add .", "Stage all files"),
    ("git commit -m 'Initial commit'", "First commit"),
    ("git remote add origin <url>", "Add remote"),
    ("git push -u origin main", "Push to remote"),
])

# 3. Daily Workflow
print_commands("Daily Workflow", [
    ("git pull origin main", "Get latest"),
    ("git status", "Check status"),
    ("git add <file>", "Stage changes"),
    ("git commit -m 'feat: add feature'", "Commit"),
    ("git push", "Push to remote"),
])

# 4. Feature Branch Workflow
print_commands("Feature Branch Workflow", [
    ("git checkout -b feature/login", "Create branch"),
    ("git add . && git commit -m 'Add login'", "Work & commit"),
    ("git push -u origin feature/login", "Push branch"),
    ("# Create Pull Request on GitHub", "Code review"),
    ("git checkout main", "Switch to main"),
    ("git pull origin main", "Update main"),
    ("git merge feature/login", "Merge locally"),
    ("git branch -d feature/login", "Delete branch"),
])

# 5. Handling Merge Conflicts
print_commands("Merge Conflict Resolution", [
    ("git merge feature-branch", "Attempt merge"),
    ("# Edit conflicted files manually", "Resolve"),
    ("git add <resolved-files>", "Stage resolved"),
    ("git commit -m 'Resolve conflicts'", "Commit merge"),
])

# 6. Useful Commands
print_commands("Useful Commands", [
    ("git log --oneline -10", "Recent history"),
    ("git diff", "Unstaged changes"),
    ("git diff --staged", "Staged changes"),
    ("git stash", "Stash changes"),
    ("git stash pop", "Restore stash"),
    ("git reset --soft HEAD~1", "Undo last commit"),
    ("git revert <commit-hash>", "Revert a commit"),
    ("git cherry-pick <hash>", "Pick specific commit"),
])

# 7. Commit Message Convention
print(f"\n   Commit Message Convention")
print(f"  {'' * 55}")
print("""  Format: <type>: <description>

  Types:
    feat     -- New feature
    fix      -- Bug fix
    docs     -- Documentation
    style    -- Formatting (no logic change)
    refactor -- Code restructure
    test     -- Adding tests
    chore    -- Build/tooling changes

  Examples:
    feat: add user authentication
    fix: resolve null pointer in payment module
    docs: update API documentation
    refactor: extract validation into utility module
""")
