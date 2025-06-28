# 🛡️ Branch Protection Setup Instructions

Since GitHub Actions can't automatically configure branch protection rules, you'll need to set these up manually in the GitHub web interface.

## Step-by-Step Setup

### 1. Go to Repository Settings
- Navigate to: https://github.com/jonathanpopham/ghostie/settings/branches
- Click **"Add rule"**

### 2. Configure Master Branch Protection

**Branch name pattern:** `master`

**Protection Rules to Enable:**

✅ **Require a pull request before merging**
- ✅ Require approvals: 1
- ✅ Dismiss stale PR approvals when new commits are pushed
- ✅ Require review from code owners (optional)

✅ **Require status checks to pass before merging**
- ✅ Require branches to be up to date before merging
- **Required status checks:**
  - `quality-check / 🛡️ Quality Gate`
  - `security-scan / 🛡️ Security Scan`

✅ **Require conversation resolution before merging**

✅ **Require signed commits** (optional but recommended)

✅ **Require linear history** (keeps clean git history)

✅ **Include administrators** (applies rules to repo admins too)

✅ **Restrict pushes that create files** (prevent accidental large files)

### 3. Configure Develop Branch Protection (Optional)

**Branch name pattern:** `develop`

**Lighter Protection Rules:**

✅ **Require a pull request before merging**
- ✅ Require approvals: 1

✅ **Require status checks to pass before merging**
- **Required status checks:**
  - `quality-check / 🛡️ Quality Gate`

## 4. Set Up Required Secrets

Go to: https://github.com/jonathanpopham/ghostie/settings/secrets/actions

**Required Secrets:**

### `NPM_TOKEN`
1. Go to https://www.npmjs.com/settings/tokens
2. Create **Automation** token
3. Copy token value
4. Add as repository secret named `NPM_TOKEN`

### `GITHUB_TOKEN` 
- This is automatically provided by GitHub Actions
- No manual setup required

## 5. Workflow Trigger Summary

### On Push to Master:
1. 🧪 **Test Suite** runs
2. 📦 **Auto-publish to NPM** (if version changed)
3. 🏷️ **Create Git tag** and GitHub release

### On Pull Request:
1. 🔍 **Quality Check** runs
2. 🛡️ **Security Scan** runs  
3. 📝 **Automated PR comment** with results
4. ✅ **Required before merge**

## 6. Development Workflow

```bash
# Feature development
git checkout develop
git checkout -b feature/new-feature
# ... make changes ...
git push origin feature/new-feature

# Create PR: feature/new-feature → develop
# After review and merge to develop:

# Release to master
git checkout develop
git push origin develop
# Create PR: develop → master
# After review, merge triggers automatic npm publish
```

## 7. Version Bumping Strategy

**Before merging to master:**
1. Update `package.json` version
2. Update version in `ghostie` script
3. Follow semantic versioning:
   - **Patch** (1.2.0 → 1.2.1): Bug fixes
   - **Minor** (1.2.0 → 1.3.0): New features
   - **Major** (1.2.0 → 2.0.0): Breaking changes

## 🎯 Result

After setup, you'll have:
- ✅ **Protected master branch** requiring PR + reviews
- ✅ **Automated testing** on all PRs
- ✅ **Automatic npm publishing** on master merge
- ✅ **GitHub releases** with proper tagging
- ✅ **Security scanning** for sensitive data

The Ghost repository will be **enterprise-grade protected**! 👻🛡️