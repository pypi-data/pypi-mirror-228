"""
Dev shell for Stackler
"""

import os
import sys
import typer
from git import Repo
from stackler import *

REPO_PATH = os.getcwd()
repo = Repo(REPO_PATH)
