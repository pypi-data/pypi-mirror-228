from .init import init_command
from .log import log_command
from .commit import commit_command
from .review import review_command
from .switch_date import switch_date_command
from .migrate import migrate_command

command_group = [init_command, log_command, commit_command, review_command, switch_date_command, migrate_command]
