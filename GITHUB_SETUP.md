# GitHub Setup Instructions

## Option 1: Using GitHub Web Interface (Recommended)

### Step 1: Create Repository on GitHub
1. Go to https://github.com/new
2. **Repository name**: `catalog-scraper` (or your preferred name)
3. **Description**: E-commerce catalog web scraper for Quiz 1 assignment
4. **Visibility**: Public (so instructor can access)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### Step 2: Push Your Code
After creating the repository on GitHub, you'll see a page with commands. Use these:

```bash
# Add the remote repository (replace USERNAME with your GitHub username)
git remote add origin https://github.com/MubashirKhan1122/catalog-scraper.git

# Push the main branch
git push -u origin main

# Push all other branches
git push origin dev
git push origin feature/catalog-navigation
git push origin feature/product-details
git push origin fix/url-resolution
git push origin fix/deduplication

# Or push all branches at once
git push origin --all
```

### Step 3: Verify
Go to your repository URL and verify:
- ✅ All files are present
- ✅ All branches are visible (click on the branch dropdown)
- ✅ README.md is displayed on the main page
- ✅ Commit history shows all your work

---

## Option 2: Using Command Line (If you have GitHub CLI)

If you prefer to create the repo from command line:

```bash
# Install GitHub CLI (if not installed)
brew install gh

# Login to GitHub
gh auth login

# Create repository and push
gh repo create catalog-scraper --public --source=. --remote=origin --push

# Push all branches
git push origin --all
```

---

## Repository URL

After creation, your repository will be at:
```
https://github.com/MubashirKhan1122/catalog-scraper
```

Share this URL with your instructor for submission.

---

## Troubleshooting

### If you get authentication errors:
```bash
# Use Personal Access Token (recommended)
# 1. Go to https://github.com/settings/tokens
# 2. Generate new token (classic)
# 3. Select: repo, workflow scopes
# 4. Copy the token
# 5. When pushing, use the token as password
```

### If remote already exists:
```bash
git remote remove origin
git remote add origin https://github.com/MubashirKhan1122/catalog-scraper.git
```

### To verify branches are pushed:
```bash
git branch -r  # Show remote branches
```
