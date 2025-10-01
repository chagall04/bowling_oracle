# GitHub Setup Guide

This guide will help you push your Bowling Score Tracker application to GitHub.

## Prerequisites

1. A GitHub account (create one at [github.com](https://github.com) if needed)
2. Git installed on your computer (already done ✓)

## Steps to Push to GitHub

### 1. Create a New Repository on GitHub

1. Go to [github.com](https://github.com) and log in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill in the details:
   - **Repository name**: `bowling_oracle` (or your preferred name)
   - **Description**: "A comprehensive multi-player bowling score tracking application with PyQt5 GUI and SQLite database"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

### 2. Link Your Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these commands in your project directory:

```bash
git remote add origin https://github.com/YOUR_USERNAME/bowling_oracle.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### Alternative: Using SSH (Recommended for frequent pushes)

If you have SSH keys set up with GitHub:

```bash
git remote add origin git@github.com:YOUR_USERNAME/bowling_oracle.git
git branch -M main
git push -u origin main
```

### 3. Verify the Upload

1. Refresh your GitHub repository page
2. You should see all your project files
3. The README.md will be displayed on the repository homepage

## Future Updates

After the initial push, you can update your repository with:

```bash
# Stage your changes
git add .

# Commit your changes
git commit -m "Description of your changes"

# Push to GitHub
git push
```

## Repository Features to Enable

### 1. Add Topics
On your repository page, click the gear icon next to "About" and add topics:
- `python`
- `pyqt5`
- `sqlite`
- `bowling`
- `score-tracker`
- `desktop-application`
- `matplotlib`

### 2. Create Releases
When you reach stable versions, create releases:
1. Go to "Releases" on your repository
2. Click "Create a new release"
3. Tag version (e.g., v1.0.0)
4. Add release notes

### 3. Add a License
Consider adding a license file (e.g., MIT License):
1. Click "Add file" → "Create new file"
2. Name it `LICENSE`
3. GitHub will offer license templates
4. Choose and commit

### 4. Enable Issues and Discussions
Use GitHub Issues to track bugs and feature requests.

## Updating the README

After pushing to GitHub, you should update the clone URL in the README.md:

```bash
git clone https://github.com/YOUR_USERNAME/bowling_oracle.git
```

Replace `yourusername` with your actual GitHub username.

## Collaborating

If others want to contribute:

1. They can fork your repository
2. Make changes in their fork
3. Submit a Pull Request to your repository
4. You can review and merge their changes

## GitHub Repository Best Practices

### Create a .github Directory

Add workflow files, issue templates, and more:

```
.github/
├── workflows/
│   └── python-app.yml (for CI/CD)
├── ISSUE_TEMPLATE/
└── PULL_REQUEST_TEMPLATE.md
```

### Add Screenshots

Create a `screenshots/` directory and add images of your application to showcase in the README.

### Create Documentation

Consider adding a `docs/` directory with detailed documentation:
- User guide
- Developer guide
- API documentation
- Architecture diagrams

## Keeping Your Repository Secure

1. **Never commit sensitive data** (passwords, API keys, etc.)
2. **Use .gitignore** properly (already configured)
3. **Review commits** before pushing
4. **Enable branch protection** for main branch (in repository settings)

## Getting Your Project Noticed

1. **Write a good README** (already done ✓)
2. **Add screenshots/GIFs** showing the application in action
3. **Share on social media** (Twitter, Reddit, LinkedIn)
4. **Add to Awesome lists** (search for "awesome python" lists)
5. **Write a blog post** about your project
6. **Present at local meetups** or conferences

## Continuous Integration (Optional)

Consider setting up GitHub Actions for automated testing:

```yaml
# .github/workflows/python-app.yml
name: Python application

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
```

## Support and Community

Consider adding:
- **CONTRIBUTING.md** - Guidelines for contributors
- **CODE_OF_CONDUCT.md** - Community standards
- **CHANGELOG.md** - Version history

---

## Quick Reference Commands

```bash
# Check repository status
git status

# View commit history
git log --oneline

# Create a new branch
git checkout -b feature-name

# View remote repositories
git remote -v

# Pull latest changes
git pull

# Push changes
git push

# Undo last commit (keep changes)
git reset --soft HEAD~1

# View differences
git diff
```

---

**Congratulations! Your Bowling Score Tracker is now ready for GitHub! 🎳**

