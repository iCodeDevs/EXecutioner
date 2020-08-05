'''FireJail sandbox class'''

from os import path
from src.sandbox.no_sandbox import NoSandBox

class FireJail(NoSandBox):

    '''FireJail SandBox class'''

    supported_languages = [
        'Python3',
        'C'
    ]
    sandbox_command = 'time -p \
                       firejail --net=none --quiet \
                       --private={2} --rlimit-as={0}  --timeout=00:00:{1} '

    def generate_command(self, command, file_location, time_limit, mem_limit):
        '''generate the firejail cmd command'''
        parent_folder = path.dirname(file_location)
        file_name = path.basename(file_location)
        command = command.format(file_name)
        command = self.sandbox_command.format(mem_limit*1024*1024, time_limit, parent_folder) \
                  + command
        return command

    def generate_compile_command(self, command, file_location, _, time_limit, mem_limit):
        return self.generate_command(command, file_location, time_limit, mem_limit)

    def generate_execute_command(self, command, file_location, time_limit, mem_limit):
        return self.generate_command(command, file_location, time_limit, mem_limit)
