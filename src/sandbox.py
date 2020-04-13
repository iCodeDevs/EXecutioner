'''
Contain Sandbox classes for different types of sandboxes used
'''

class SandBox:
    '''SandBox base class'''
    def can_run(self, language: str):
        '''Check if the sandbox can this language'''
    def run(self, command: str, time_out: int, mem_limit: int, **kwarg):
        '''run the given language with given conditions'''

class FireJail(SandBox):
    '''FireJail SandBox class'''
    supported_languages = [
        'Python2',
        'Python3',
        'C',
        'C++'
    ]

    def can_run(self, language: str):
        '''Check if the sandbox can this language'''
        return language in self.supported_languages

    def run(self, command: str, time_out: int, mem_limit: int, **kwarg):
        '''run the given language with given conditions'''
