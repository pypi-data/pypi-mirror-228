from winreg import DeleteKey, EnumKey, HKEYType, OpenKey

from src.context_menu_manager import ContextMenu, ContextCommand
from src.context_menu_manager.resources import Command


def create_context(context: ContextMenu | ContextCommand, parent: Command = None):
	from winreg import CreateKey, SetValueEx, REG_SZ
	
	if parent:
		context.key = CreateKey(context.permission, context.location)
	
	if context.mui_verb:
		SetValueEx(context.key, 'MUIVerb', 0, REG_SZ, context.mui_verb)
	if context.separator_before:
		SetValueEx(context.key, 'SeparatorBefore', 0, REG_SZ, '')
	if context.separator_after:
		SetValueEx(context.key, 'SeparatorAfter', 0, REG_SZ, '')
	if context.icon:
		SetValueEx(context.key, 'Icon', 0, REG_SZ, context.icon)
	
	if isinstance(context, ContextMenu):
		SetValueEx(context.key, 'subcommands', 0, REG_SZ, '')
		context.sub_key = CreateKey(context.permission, str(context.sub))
		for ctx in context.subcommands:
			create_context(ctx)
	else:
		SetValueEx(context.sub_key, '', 0, REG_SZ, context.action)
	

def delete_context(key: ContextMenu | ContextCommand | HKEYType, key2: str = None) -> None:
	if not isinstance(key, Command):
		with OpenKey(key, key2) as sub_key:
			while True:
				try:
					sub_sub_key_name = EnumKey(sub_key, 0)
					delete_context(sub_key, sub_sub_key_name)
				except OSError:
					break
			DeleteKey(key, key2)
	else:
		
		if isinstance(key, ContextMenu):
			for subcommand in key.subcommands:
				delete_context(subcommand)
		
		DeleteKey(key.permission, str(key.sub))
		DeleteKey(key.permission, str(key.location))