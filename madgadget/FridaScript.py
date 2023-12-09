import secrets
import string
from pathlib import Path

class FridaScript:
    def __init__(self, path: Path) -> None:
        if not path.is_file():
            raise FileNotFoundError(f"Cannot initialize Frida script, file not found: '{path.absolute()}'")
        self.path = path
        self.new_name()
    
    def new_name(self):
        self.name = f"lib{''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(5 + secrets.randbelow(12)))}.so"

    def default_gadget_config(self) -> str:
        return f'''
{{
  "interaction": {{
    "type": "script",
    "path": "{self.name}"
  }}
}}
'''