# Publish CyberNova Lab on GitHub as `sansw123`

This guide assumes you are new to Git and using Windows. Commands are the same in PowerShell, Git Bash, macOS, and Linux except where noted.

## 1. Personalise the project first

The repository links have already been personalised for `https://github.com/sansw123`. You may optionally replace the public author name `sansw123` with your real or preferred name.

| Search for | Optional replacement |
|---|---|
| `sansw123` in the Author section | your real or preferred public name |
| no LinkedIn line is included | add it later only if you want it public |

The author name appears in `README.md`, `pyproject.toml`, and `LICENSE`. In VS Code, press **Ctrl+Shift+F** to search the whole project if you want to change it.

Do not put your phone number, home address, passwords, API keys, college ID, or other private information in a public repository.

## 2. Install the two tools

1. Create a free account at [github.com](https://github.com/).
2. Install [Git](https://git-scm.com/downloads).
3. Optional but friendly for beginners: install [VS Code](https://code.visualstudio.com/).
4. Restart PowerShell and check Git:

```powershell
git --version
```

## 3. Connect commits to your contribution graph

Use the same email that is verified in **GitHub → Settings → Emails**:

```powershell
git config --global user.name "sansw123"
git config --global user.email "YOUR-VERIFIED-EMAIL"
git config --global init.defaultBranch main
```

If you prefer email privacy, GitHub Settings shows a `noreply` email you can use instead.

## 4. Test the project before publishing

Open PowerShell inside the `cybernova-lab` folder. A quick way is to open the folder in File Explorer, click the address bar, type `powershell`, and press Enter.

```powershell
# First confirm the zero-install launcher works
python run.py

# Then prepare the reusable command and run tests
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m unittest discover -s tests -v
cybernova
```

If PowerShell blocks activation, you may use the virtual environment directly:

```powershell
.venv\Scripts\python.exe -m pip install -e .
.venv\Scripts\python.exe -m cybernova
```

The tests should say `OK`.

## 5. Create your local Git history

Still inside the project folder:

```powershell
git init -b main
git add .
git status
git commit -m "feat: launch CyberNova Lab v1.0"
```

Read the `git status` list before committing. It should not contain `.venv`, passwords, private notes, or `.cybernova-progress.json`.

## 6. Create the empty GitHub repository

1. Sign in to GitHub.
2. Click the **+** menu in the top-right and choose **New repository**.
3. Repository name: `cybernova-lab`.
4. Description: `A beginner-friendly cybersecurity learning toolkit built with Python.`
5. Choose **Public** so it appears as portfolio work.
6. Do **not** add a README, `.gitignore`, or license on GitHub—the project already has them.
7. Click **Create repository**.

## 7. Push your code

GitHub shows a repository URL. For your account, run:

```powershell
git remote add origin https://github.com/sansw123/cybernova-lab.git
git remote -v
git push -u origin main
```

A browser sign-in window may open. Complete it with your GitHub account. GitHub does not accept your account password as a Git command-line password.

Refresh the GitHub page. The banner, README, files, and first green contribution should appear. A contribution can take some time to show.

## 8. Decorate the repository page

On the right side of the repository page:

1. Click the gear beside **About**.
2. Add the description from step 6.
3. Add topics: `cybersecurity`, `python`, `education`, `cli`, `beginner-project`, `sha256`, `file-integrity`.
4. Enable **Issues** in **Settings → General → Features**.
5. Enable **Private vulnerability reporting** in **Settings → Security → Code security** if available.
6. Pin the repository: open your GitHub profile, choose **Customize your pins**, and select `cybernova-lab`.

Your Actions tab will run the tests automatically. A green check beside a commit means the automated checks passed.

## 9. Make honest contributions over time

Do not create meaningless commits just to colour the contribution graph. Build a visible learning story:

```powershell
git switch -c feature/quiz-difficulty
# edit code, documentation, and tests
python -m unittest discover -s tests -v
git add .
git commit -m "feat: add quiz difficulty levels"
git push -u origin feature/quiz-difficulty
```

GitHub will offer a **Compare & pull request** button. Open the pull request, describe what you learned, check that tests pass, and merge it into `main`. Then update your computer:

```powershell
git switch main
git pull
```

Good future contributions include:

- adding one quiz question with a trusted reference;
- improving an explanation or test;
- fixing a typo through a pull request;
- implementing one roadmap checkbox;
- reporting and fixing a real bug;
- contributing documentation to another beginner-friendly project.

## Common problems

### `git` is not recognised

Install Git, close all terminals, and open a new PowerShell window.

### `python` is not recognised

Install Python from python.org and select **Add Python to PATH** during installation. On Windows, try `py` instead of `python`.

### `remote origin already exists`

Check it first:

```powershell
git remote -v
```

If it points to the wrong repository:

```powershell
git remote set-url origin https://github.com/sansw123/cybernova-lab.git
```

### My commits do not appear in the contribution graph

Check that the commit email belongs to your GitHub account:

```powershell
git config user.email
git log -1 --format="%an <%ae>"
```

Contributions normally count after commits reach the default branch (`main`). Commits left only on an unmerged branch or fork do not count.

### I accidentally committed a secret

Making a new commit that deletes it is not enough because Git keeps history. Revoke or rotate the secret immediately, make the repository private, and follow GitHub's sensitive-data removal guidance.

## Your next milestone

After publishing, open an issue titled `Add quiz difficulty levels`, label it `enhancement` and `good first issue`, and solve it on a new branch. That gives you a real issue → branch → commit → pull request → review → merge story to discuss in an interview.
