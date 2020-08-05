from src import settings
from src.sandbox.firejail import FireJail

class Program:
    def __init__(self, pgm_obj, language, sandbox = FireJail()):
        self.language = language
        if isinstance(pgm_obj,str):
            self.code = pgm_obj
        elif hasattr(pgm_obj,'read'):
            self.code = pgm_obj.read()
            pgm_obj.close()
        
        self.settings = settings.get_language_settings(language)
        self.sandbox = sandbox
        self.compiled_program = None
        self.file_location = None

    def compile(self):
        if not self.compiled_program:
            self.compiled_program = self.sandbox.compile(self)
    
    def execute(self,inp: str):
        return self.sandbox.execute(self.compiled_program,inp)
    
    def __del__(self):
        '''Delete history and files of program in sandbox instance'''
        self.sandbox.delete(self)