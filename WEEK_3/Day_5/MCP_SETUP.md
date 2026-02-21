# My MCP Setup Journey

## Where the config lives
- Cursor reads from: `C:\Users\pbiai\.cursor\mcp.json`
- (Not from AppData — that was a key lesson learned the hard way)

## What I set up

### GitHub
Gives Cursor access to my GitHub repositories, issues, and files.
26 tools available. Needs a Personal Access Token from github.com/settings/tokens with `repo` scope.

### Filesystem
Lets Cursor read and write files in my Documents folder.
14 tools available. Only has access to `C:\Users\pbiai\Documents` — nothing else.

---

## How long each phase actually took (and where I got stuck)

**Installing Node.js — ~10 minutes**
Straightforward once I knew I needed it. Didn't realize npx depends on it.

**Creating the GitHub token — ~5 minutes**
Easy. Just needed to know where to go on GitHub.

**Finding the right config file location — ~30 minutes** ⚠️
This is where most time was lost. The docs say `%APPDATA%\Cursor\mcp.json` but Cursor was actually reading from `C:\Users\pbiai\.cursor\mcp.json`. I kept editing the wrong file without realizing it.

**Copying an incomplete config file multiple times — ~20 minutes** ⚠️
When adding the filesystem server, I kept copying from the AppData file (which only had GitHub) over the correct file. I was copying blindly without checking what was actually inside. Next time: always verify the contents of a file before copying it with `type filename`.

**Getting filesystem server to appear in Tools & MCP — ~15 minutes**
Once I edited the correct file directly, it worked immediately on restart.

**Testing both servers — ~5 minutes**
Both worked first try once the config was right.

---

## ⚠️ Security Incident — Token Leak (this actually happened to me)

During setup, a copy of `mcp.json` was accidentally created inside the `WEEK_3` project folder (inside a hidden `.cursor` folder). Because it was hidden, I had no idea it was there when I ran `git add .` and pushed to GitHub.

GitHub's push protection caught it and blocked the push, but the token had already been committed to Git history. I had to:
1. Delete the exposed token immediately on github.com/settings/tokens
2. Rewrite the entire Git history using `git filter-repo` to remove the file from all commits
3. Create a brand new token and update `mcp.json` with it

The correct `mcp.json` lives at `C:\Users\pbiai\.cursor\mcp.json` — in the home folder, completely outside any Git repo. It should never be inside a project folder that gets pushed to GitHub.

---

## What I'd do differently next time

- Before copying any file, check what's inside it first
- Go straight to editing `C:\Users\pbiai\.cursor\mcp.json` — skip AppData entirely
- After any config change, run `type .cursor\mcp.json` to confirm the file looks right before restarting
- Always add config files with credentials to `.gitignore` BEFORE creating them
- Never run `git add .` blindly — always check `git status` first

## Useful commands to remember
```powershell
# Check what's in your config
type C:\Users\pbiai\.cursor\mcp.json

# Test a server manually
npx -y @modelcontextprotocol/server-filesystem C:\Users\pbiai\Documents

# Check Node is installed
node --version
npm --version

# Always check what you're committing before pushing
git status
```
