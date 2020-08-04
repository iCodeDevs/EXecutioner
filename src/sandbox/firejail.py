from src.sandbox.no_sandbox import NoSandBox

class FireJail(NoSandBox):
    '''FireJail SandBox class'''
    supported_languages = [
        'Python2',
        'Python3',
        'C',
        'C++'
    ]
    sandbox_command = 'time -p firejail --net=none --quiet --private --rlimit-as={0}  --timeout=00:00:{1} '
    def generate_compile_command(self,
                                command,
                                file_location,
                                language,
                                time_limit,
                                mem_limit):
        command = command.format(file_location)
        command = self.sandbox_command.format(mem_limit*1024*1024,time_limit) + command
        return command
    
    def generate_execute_command(self, command, file_location,time_limit,mem_limit):
        command = command.format(file_location)
        command = self.sandbox_command.format(mem_limit*1024*1024,time_limit) + command
        return command
