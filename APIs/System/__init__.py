import os
from pathlib import Path

from APIs.System.logger import BotItLogger
from APIs.System.settings import Settings, OperationMode, \
    DatabaseSettings, DatabaseCredentials
from APIs.System.vault import Vault
from APIs.System.git import BotItGitIssue, BotItGit


BOT_IT_PATH = Path(os.path.abspath(__file__)).parent.parent


