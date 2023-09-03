from pathlib import Path

from src.context_menu_manager.resources import Command
from src.context_menu_manager import Contexts, Permissions


class ContextCommand(Command):
	
	def __init__(
		self, name: str,
		action: str,
		context: Contexts | str,
		permissions: Permissions | int,
		mui_verb: str = None,
		icon: Path | str = None,
		separator_before: bool = False,
		separator_after: bool = False,
		parent = None
	):
		super().__init__(
			name,
			context,
			permissions,
			mui_verb,
			icon,
			separator_before,
			separator_after,
			parent
		)
		
		self.action = action
