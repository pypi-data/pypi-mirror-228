from winreg import HKEY_CLASSES_ROOT, HKEY_CURRENT_USER


class Contexts:
	DIRECTORIES: str = r'Directory\\shell'
	DIRECTORIES_BACKGROUND = r'Directory\\Background\\shell'
	ALL_FILES: str = r'*\\shell'
	ROOT = HKEY_CLASSES_ROOT
	CURRENT_USER = HKEY_CURRENT_USER
