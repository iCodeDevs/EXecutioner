'''represent a program'''
from typing import Any, Dict, List
from uuid import uuid4
from .settings import Settings
from .sandbox.base_sandbox import SandBox
from .sandbox.firejail import FireJail
from .evaluate import TestCase


class Program:

    '''Represent a program instance'''

    def __init__(self, pgm_obj: str, language: str, sandbox: SandBox = FireJail()):
        '''Create a new Program object'''

        self.uuid = uuid4()
        '''The unique id of this program'''

        self.language: str = language
        '''The language of the program'''
        self.code: str = pgm_obj
        '''The source code as a string'''
        self.settings = Settings.get_language_settings(language)
        '''The language specific settings object'''
        self.sandbox: SandBox = sandbox
        '''The sandbox to be used'''

    def compile(self) -> None:
        '''compile the program'''
        self.sandbox.compile(self)

    def execute(self, input_testcase: TestCase) -> None:
        '''execute the program'''
        self.sandbox.execute(self, input_testcase)

    def to_json_object(self) -> Dict[str, Any]:
        '''convert to JSON object'''
        return {
            "code": self.code,
            "language": self.language,
            "sand_box": self.sandbox.to_json_object(),
        }

    @staticmethod
    def from_json_object(data: Dict[str, Any]) -> 'Program':
        '''Generate Program object from JSON object'''
        pgm = Program(data["code"], data["language"])
        sandbox_json: List = data.get("sand_box")
        if not sandbox_json:
            return pgm
        sandbox = SandBox.from_json_object(sandbox_json)
        pgm.sandbox = sandbox if sandbox else pgm.sandbox
        return pgm

    def __eq__(self, o: 'Program') -> bool:
        return (self.code == o.code) and (self.language == o.language)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        del self

    def __del__(self):
        '''Delete history and files of program in sandbox instance'''
        self.sandbox.delete(self)
