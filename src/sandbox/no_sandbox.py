from src.sandbox.base_sandbox import SandBox
from src.settings import SETTINGS
from src.errors import TimeOutError,RunTimeError,MemoryOutError, CompilationError
from uuid import uuid4
from os import path,unlink,mkdir
import subprocess
import shlex
import re
class NoSandBox(SandBox):
    supported_languages = [
        'python2',
        'python3',
        'C',
        'C++',
    ]
    error_reg = re.compile('(?s)(?P<error>.*)real (?P<real>[0-9]*\.[0-9]*)')
    def generate_compile_command(self,
                                command,
                                file_location,
                                language,
                                time_limit,
                                mem_limit):
        command = command.format(file_location)
        command = '/usr/bin/time -p ' + command
        return command

    def generate_execute_command(self, command, file_location,time_limit,mem_limit):
        command = command.format(file_location)
        command = '/usr/bin/time -p timeout {0} '.format(time_limit) + command
        return command

    
    def get_compiled_file(self, file_location, lang_settings):
        return lang_settings.get('compiledFormat','{0}').format(file_location)

    def process_error(self, err_text):
        match = self.error_reg.match(err_text)
        return match.group('error'), float(match.group('real'))

    def setupFile(self,program,lang_settings):
        workspace = SETTINGS.get('workspace','')
        if(not path.exists(workspace)):
            mkdir(workspace)
        file_name = lang_settings.get('fileFormat','{0}').format(uuid4())
        file_location = path.join(workspace,file_name)
        fileObj = open(file_location,'w')
        fileObj.write(program.code)
        fileObj.close()
        program.file_location = file_location
        return file_location

    def idError(self, error: str,time,time_limit):
        if time > time_limit:
            return TimeOutError()
        elif error.rfind('Memory')!=-1:
            return MemoryOutError()
        else:
            return RunTimeError()

    def compile(self, program, **kwargs):
        lang_settings = program.settings
        language =program.language
        file_location = self.setupFile(program,lang_settings)
        compile_command = lang_settings.get('compileCommand',None)
        if not compile_command:
            raise Exception('Cannot Compile')

        compile_command = self.generate_compile_command(compile_command,
                            file_location,
                            language,
                            100,
                            int(lang_settings['memLimit']))

        process = subprocess.run(shlex.split(compile_command),
                            encoding='utf-8',
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        output,errors = process.stdout,process.stderr
        error,time = self.process_error(errors)
        if(len(error.strip())>0):
            raise CompilationError()
        compile_file_location = self.get_compiled_file(file_location, lang_settings)
        compiled_program = self.CompiledProgram(lang_settings,compile_file_location)
        return compiled_program
    
    def execute(self, compiled_program, test_input='',**kwargs):
        lang_settings = compiled_program.lang_settings
        compiled_file_location = compiled_program.file_location
        exe_command = self.generate_execute_command(
                    lang_settings.get('executeCommand'),
                    compiled_file_location,
                    lang_settings['timeLimit'],
                    int(lang_settings['memLimit']))
        process = subprocess.run(shlex.split(exe_command),
                    input=test_input,encoding='utf-8',
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
        output,errors = process.stdout,process.stderr

        error,time = self.process_error(errors)
        if(len(error.strip())>0):
            raise self.idError(error,time,int(lang_settings['timeLimit']))

        return output
    
    def delete(self, program):
        file_location = program.file_location
        compiled_file_location =program.compiled_program.file_location
        if path.exists(file_location):
            unlink(file_location)
        if path.exists(compiled_file_location):
            unlink(compiled_file_location)


        