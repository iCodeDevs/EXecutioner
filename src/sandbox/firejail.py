'''FireJail sandbox class'''

from os import path
from src.sandbox.no_sandbox import NoSandBox


class FireJail(NoSandBox):

    '''FireJail SandBox class'''

    supported_languages = [
        'Python3',
        'C'
    ]
    '''The supported languages of this sandbox'''
    sandbox_command = 'time -p \
                    firejail --net=none --quiet \
                    --private={folder} --rlimit-as={mem_limit}  timeout {time_limit} \
                    {command}'
    '''The sandbox's command to be executed'''

    def generate_command(self, command, file_location, time_limit, mem_limit):
        '''generate the firejail cmd command'''
        parent_folder = path.dirname(file_location)
        file_name = path.basename(file_location)
        command = command.format(compiled_file=file_name, source=file_name)
        command = self.sandbox_command.format(
            mem_limit=mem_limit*1024*1024,
            time_limit=time_limit,
            folder=parent_folder,
            command=command,
        )
        return command

    def generate_compile_command(self, command, file_location, _, time_limit, mem_limit):
        return self.generate_command(command, file_location, time_limit, mem_limit)

    def generate_execute_command(self, command, file_location, time_limit, mem_limit):
        return self.generate_command(command, file_location, time_limit, mem_limit)
