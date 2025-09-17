# Merge Instructions

This document provides instructions for merging feature branch changes back to the main branch using two different approaches.

## Prerequisites

- Ensure all changes are committed to your feature branch
- Make sure your feature branch is up to date with the latest main branch
- Run any tests to ensure everything is working correctly

## Method 1: GitHub Pull Request (Recommended)

### Step 1: Push your feature branch
```bash
git push origin your-feature-branch-name
```

### Step 2: Create a Pull Request
1. Go to your GitHub repository in a web browser
2. Click "Compare & pull request" button (should appear after pushing)
3. Or click "New pull request" and select your feature branch
4. Fill in the PR title and description
5. Add any reviewers if needed
6. Click "Create pull request"

### Step 3: Review and Merge
1. Wait for code review (if required)
2. Address any feedback or requested changes
3. Once approved, click "Merge pull request"
4. Choose merge strategy:
   - **Create a merge commit**: Preserves branch history
   - **Squash and merge**: Combines all commits into one
   - **Rebase and merge**: Replays commits without merge commit

### Step 4: Clean up
```bash
git checkout main
git pull origin main
git branch -d your-feature-branch-name
git push origin --delete your-feature-branch-name
```

## Method 2: GitHub CLI

### Prerequisites
Install GitHub CLI if not already installed:
```bash
# macOS
brew install gh

# Or download from: https://cli.github.com/
```

### Step 1: Authenticate with GitHub
```bash
gh auth login
```

### Step 2: Push your feature branch
```bash
git push origin your-feature-branch-name
```

### Step 3: Create Pull Request via CLI
```bash
gh pr create --title "Your PR Title" --body "Description of changes"
```

### Step 4: Review and Merge
```bash
# List open PRs
gh pr list

# View specific PR details
gh pr view [PR_NUMBER]

# Merge the PR (replace [PR_NUMBER] with actual number)
gh pr merge [PR_NUMBER] --merge  # or --squash or --rebase
```

### Step 5: Clean up
```bash
git checkout main
git pull origin main
git branch -d your-feature-branch-name
git push origin --delete your-feature-branch-name
```

## Merge Strategies Explained

- **Merge commit**: Creates a merge commit, preserving the branch history
- **Squash and merge**: Combines all commits into a single commit
- **Rebase and merge**: Replays commits on top of main without a merge commit

Choose the strategy that best fits your project's workflow and history preferences.

## Best Practices

1. **Always test before merging**: Run tests and ensure code quality
2. **Write descriptive commit messages**: Make it clear what each commit does
3. **Keep PRs focused**: One feature per PR when possible
4. **Review your own code**: Check the diff before creating the PR
5. **Clean up branches**: Delete feature branches after successful merge
