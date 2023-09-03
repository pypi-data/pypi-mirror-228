from pathlib import Path

from src.context_menu_manager.resources.classes import Command
from src.context_menu_manager import ContextCommand, Contexts, Permissions


class ContextMenu(Command):
	
	def __init__(
		self, name: str,
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
		
		self.subcommands: list[ContextMenu | ContextCommand | Command] = []
	
	def add_subcommand(self, command: Command):
		
		command.relocate(self.sub)
		
		self.subcommands.append(command)
