'''NoSandBox class

A sandbox that doesnot provide security but allows execution of commands with time limit
'''

from uuid import uuid4
from os import path, unlink, mkdir
import subprocess
import shlex
import re
from typing import TYPE_CHECKING, Union
from src.sandbox.base_sandbox import SandBox
from src.settings import Settings
from src.errors import TimeOutError, RunTimeError, MemoryOutError, CompilationError

#pylint: disable=W0611,R0401
if TYPE_CHECKING:
    from src.program import Program, TestCase, CompiledProgram
#pylint: enable=W0611,R0401


class NoSandBox(SandBox):

    '''NoSandBox sandbox class'''

    supported_languages = [
        'python2',
        'python3',
        'C',
        'C++',
    ]
    '''List of supported languages by this sandbox'''
    error_reg = re.compile(
        r'''(?s)(?P<error>.*)real (?P<real>[0-9]*[.][0-9]*)\nuser (?P<user>[0-9]*[.][0-9]*)\nsys (?P<sys>[0-9]*[.][0-9]*)'''  # pylint: disable=C0301
    )
    '''regular expression to extract error text and time'''

    def generate_compile_command(self, command, file_location, _, __, ___):
        '''generate command to compile program'''
        command = command.format(source=file_location)
        command = '/usr/bin/time -p ' + command
        return command

    def generate_execute_command(self, command, file_location, time_limit, _):
        '''generate command to execute program'''
        command = command.format(compiled_file=file_location)
        command = '/usr/bin/time -p timeout {0} '.format(time_limit) + command
        return command

    def get_compiled_file(self, file_location, lang_settings):
        '''get the file location of compiled file'''
        return lang_settings.get('compiledFormat', '{source}').format(source=file_location)

    def process_error(self, err_text):
        '''get error and real time taken'''
        match = self.error_reg.match(err_text)
        return match.group('error'), {
            'real': float(match.group('real')),
            'user': float(match.group('user')),
            'sys': float(match.group('sys')),
        }

    def setup_file(self, program, lang_settings):
        '''set up the file in file system'''
        workspace = Settings.get_workspace()
        if not path.exists(workspace):
            mkdir(workspace)
        file_name = lang_settings.get(
            'fileFormat', '{filename}').format(filename=uuid4())
        file_location = path.join(workspace, file_name)
        file_obj = open(file_location, 'w')
        file_obj.write(program.code)
        file_obj.close()
        program.file_location = file_location
        return file_location

    def identify_error(self, error: str, time: float, time_limit: int) -> Union[RunTimeError, None]:
        '''identify the error'''

        if time > time_limit:
            return TimeOutError()
        elif error.rfind('Memory') != -1:
            return MemoryOutError()
        elif len(error.strip()) > 0:
            return RunTimeError()
        else:
            return None

    def compile(self, program: 'Program', **_) -> 'CompiledProgram':
        lang_settings = program.settings
        language = program.language
        file_location = self.setup_file(program, lang_settings)
        compile_command = lang_settings.get('compileCommand', None)
        if not compile_command:
            raise Exception('Cannot Compile')

        compile_command = self.generate_compile_command(compile_command,
                                                        file_location,
                                                        language,
                                                        100,
                                                        int(lang_settings['memLimit']))

        process = subprocess.run(shlex.split(compile_command),
                                 encoding='utf-8',
                                 check=False,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        _, errors = process.stdout, process.stderr
        error, _ = self.process_error(errors)
        if len(error.strip()) > 0:
            raise CompilationError()

        from src.program import CompiledProgram  # pylint: disable=C0415

        compile_file_location = self.get_compiled_file(
            file_location, lang_settings)
        compiled_program = CompiledProgram(
            lang_settings, compile_file_location)
        return compiled_program

    def execute(self, program: 'Program', testcase: 'TestCase', **kwargs) -> None:
        compiled_program = program.compiled_program
        test_input = testcase.input
        lang_settings = compiled_program.lang_settings
        compiled_file_location = compiled_program.file_location
        exe_command = self.generate_execute_command(lang_settings.get('executeCommand'),
                                                    compiled_file_location,
                                                    lang_settings['timeLimit'],
                                                    int(lang_settings['memLimit']))
        process = subprocess.run(shlex.split(exe_command),
                                 input=test_input, encoding='utf-8',
                                 check=False,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        output, errors = process.stdout, process.stderr
        error, time = self.process_error(errors)
        max_time = max(time.get('user', 0) +
                       time.get('sys', 0), time.get('real', 0))
        testcase.error = self.identify_error(
            error, max_time, int(lang_settings['timeLimit']))
        testcase.real_output = output
        testcase.time = max_time

    def delete(self, program: 'Program', **kwargs) -> None:
        file_location = program.file_location
        if path.exists(file_location):
            unlink(file_location)
        if program.compiled_program:
            compiled_file_location = program.compiled_program.file_location
            if path.exists(compiled_file_location):
                unlink(compiled_file_location)
