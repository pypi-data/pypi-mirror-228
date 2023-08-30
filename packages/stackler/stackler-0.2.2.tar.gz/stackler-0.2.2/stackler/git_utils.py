"""Git utils for Stackler"""

import os

from typing import Optional, List
from git import Commit, GitCommandError, Repo, BadName
from git.refs import Head

REPO_PATH = os.getcwd()
BASE_BRANCH = "develop"
REMOTE = "origin"


def get_short_hash(cmt: Commit):
    """
    Returns the short unique hash
    """
    repo = Repo(REPO_PATH)
    return repo.git.rev_parse(cmt, short=True)


def is_unstaged():
    """
    Returns if there's unstaged files
    """
    repo = Repo(REPO_PATH)
    return len(repo.untracked_files) > 0


def is_detached():
    """
    Returns if the head is detached.
    """
    repo = Repo(REPO_PATH)
    return repo.head.is_detached


def is_dirty():
    """
    Returns if the changeset is not empty.
    """
    repo = Repo(REPO_PATH)
    return repo.is_dirty()


def get_commit_safe(sha: str) -> Optional[Commit]:
    """
    Gets the commit; exits gracefully if the commit is not found.
    """
    repo = Repo(REPO_PATH)
    try:
        return repo.commit(sha)
    except (GitCommandError, BadName):
        return None


def is_commit_in_stack(sha: str, tip: str = None, base: str = BASE_BRANCH, remote=REMOTE):
    """
    Returns if the commit is not in the range specified.
    """
    repo = Repo(REPO_PATH)
    commits = list(repo.iter_commits(f"{remote}/{base}^..{tip}"))
    target_commit = get_commit_safe(sha)
    if not target_commit:
        return False
    return target_commit in commits


def get_base_commit(base_branch: str = BASE_BRANCH) -> Optional[Commit]:
    """
    Returns the base commit of the current branch located on base_branch

    Args:
        base_branch (str): the object name for the base_branch
    """
    repo = Repo(REPO_PATH)
    res = repo.merge_base(base_branch, repo.head)
    return res[0] if res else None


def get_branches_for_commit(cmt: Commit, remote: str) -> List[Head]:
    """
    Returns all the tags given a commit, including remote ones
    """
    repo = Repo(REPO_PATH)
    local_branches = repo.branches
    remote_branches = repo.remote(remote).refs
    return [b for b in local_branches + remote_branches if b.commit == cmt]
