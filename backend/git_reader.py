from git import Repo
import os

def get_git_history(repo_path="."):
    """
    Reads recent commits from a Git repository.
    Returns commit messages and modified files.
    """

    if not os.path.exists(os.path.join(repo_path, ".git")):
        return {"error": "This folder is not a git repository."}

    repo = Repo(repo_path)
    commits = []

    for commit in repo.iter_commits('master', max_count=5):
        commits.append({
            "message": commit.message,
            "author": commit.author.name,
            "date": str(commit.committed_datetime),
            "files": list(commit.stats.files.keys())
        })

    return {"commits": commits}
