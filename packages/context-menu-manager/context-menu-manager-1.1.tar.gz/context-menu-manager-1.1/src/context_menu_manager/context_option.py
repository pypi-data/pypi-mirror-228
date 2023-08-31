from pathlib import Path
from typing import Union

from src.resources import Contexts, Permissions


class ContextOption:
	
	def __init__(
		self, name: str,
		context: Contexts | str,
		permissions: Permissions | int,
		action: str = None,
		is_shell: bool = False,
		mui_verb: str = None,
		icon: Path | str = None,
		separator_before: bool = False,
		separator_after: bool = False,
		auto_create: bool = False,
		parent = None,
	):
		if ' ' in name:
			raise Exception('OptionCommand name must not contain any spaces')
		if not is_shell and not action:
			raise Exception('Commands must receive an action')
		
		from pathlib import Path
		
		self.__name = name
		self.__action = action
		self.__parent: ContextOption = parent
		self.__permissions = permissions
		self.__context = context
		self.is_shell = is_shell
		self.__location: Path
		if self.__parent is None:
			self.__location = Path(fr'{self.__context}\\{self.__name}')
		else:
			self.__location = self.__parent.sub.joinpath(self.__name)
		self.__sub: Path = self.__location.joinpath('shell' if self.is_shell else 'command')
		self.__icon = None
		if icon:
			self.__icon = str(icon)
		self.__mui_verb = mui_verb
		self.__separator_before = separator_before
		self.__separator_after = separator_after
		self.__key = None
		self.__sub_key = None
		self.subcommands: list[ContextOption] = []
		if auto_create:
			self.create()
	
	@property
	def location(self) -> str:
		return str(self.__location)
	
	@property
	def sub(self) -> Path:
		return self.__sub
	
	def create(self, create_subcommands: bool = False):
		from winreg import CreateKey, SetValueEx, REG_SZ
		
		self.__key = CreateKey(self.__permissions, self.location)
		
		if self.__mui_verb:
			SetValueEx(self.__key, 'MUIVerb', 0, REG_SZ, self.__mui_verb)
		if self.__separator_before:
			SetValueEx(self.__key, 'SeparatorBefore', 0, REG_SZ, '')
		if self.__separator_after:
			SetValueEx(self.__key, 'SeparatorAfter', 0, REG_SZ, '')
		if self.__icon:
			SetValueEx(self.__key, 'Icon', 0, REG_SZ, self.__icon)
		if self.is_shell:
			SetValueEx(self.__key, 'subcommands', 0, REG_SZ, '')
		
		self.__sub_key = CreateKey(self.__permissions, str(self.__sub))
		
		if not self.is_shell and self.__action:
			SetValueEx(self.__sub_key, '', 0, REG_SZ, self.__action)
		
		if self.is_shell and create_subcommands:
			for command in self.subcommands:
				command.create()
	
	def add_subcommand(
		self, name: str,
		action: str,
		is_shell: bool = False,
		mui_verb: str = None,
		icon: Path | str = None,
		separator_before: bool = False,
		separator_after: bool = False
	):
		if not self.is_shell:
			raise Exception('You can\'t add subcommands to a command')
		
		new_command = ContextOption(
			name,
			self.__context,
			self.__permissions,
			action,
			is_shell,
			mui_verb,
			icon,
			separator_before,
			separator_after,
			False,
			self
		)
		self.subcommands.append(new_command)
	
	@staticmethod
	def delete(
		key: Union[int, any], key2: str
	):
		from winreg import DeleteKey, OpenKey, EnumKey
		
		if not isinstance(key, ContextOption):
			with OpenKey(key, key2) as sub_key:
				while True:
					try:
						sub_sub_key_name = EnumKey(sub_key, 0)
						ContextOption.delete(sub_key, sub_sub_key_name)
					except OSError:
						break
				DeleteKey(key, key2)
		else:
			if key.is_shell:
				for subcommand in key.subcommands:
					ContextOption.delete(subcommand, '')
			
			DeleteKey(key.__permissions, str(key.sub))
			DeleteKey(key.__permissions, key.location)
