# 1. Make sure you're on main and up to date
git checkout main
git pull origin main

# 2. Create a new branch
git checkout -b add-project-files

# 3. Create/save your README.md and requirements.txt
#    (do this in VS Code, save the files)

# 4. Stage the files
git add README.md
git add requirements.txt

# 5. Commit with a clear message
git commit -m "Add README and requirements.txt"

# 6. Push your branch to GitHub
git push origin add-project-files

# 7. Go to github.com/pbiain/YOUR-REPO
#    You'll see the yellow banner → click "Compare & pull request"
#    Add a title and description
#    Assign your teammate as reviewer
#    Click "Create Pull Request"
```

**That's the full loop.** Repeat this every time you add a new feature:
```
main → new branch → work → commit → push → Pull Request → merge → back to main