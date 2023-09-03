from pathlib import Path
from winreg import HKEYType

from .contexts import Contexts
from .permissions import Permissions


# noinspection PyPropertyDefinition
class Command:
	
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
		if ' ' in name:
			raise Exception('Name must not contain any spaces')
		
		self.name = name
		self.action = context
		self.parent = parent
		self.permission = permissions
		self.context = context
		if self.parent is None:
			self.location = Path(fr'{self.context}\\{self.name}')
		else:
			self.location = self.parent.sub.joinpath(self.name)
		self.sub: Path | None = None
		self.icon = str(icon) if icon else icon
		self.mui_verb = mui_verb
		self.separator_before = separator_before
		self.separator_after = separator_after
		self.key: HKEYType | None = None
		self.sub_key: HKEYType | None = None
	
	def relocate(self, location: Path):
		self.location = location.joinpath(self.name)
		# noinspection PyAttributeOutsideInit
		self.sub = self.location.joinpath(self.sub.name)
