'''NoSandBox class

A sandbox that doesnot provide security but allows execution of commands with time limit
'''
from os import path, unlink, mkdir
import subprocess
import shlex
import re
from typing import TYPE_CHECKING, Dict, Union
from executioner.settings import Settings
from executioner.errors import (
    TimeOutError,
    RunTimeError,
    MemoryOutError,
    CompilationError,
)
from .base_sandbox import SandBox

#pylint: disable=W0611,R0401
if TYPE_CHECKING:
    from executioner.program import Program, TestCase
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

    def __init__(self):
        '''initialize object variables'''
        self.file_location: str = ''
        '''The file location of the current program'''
        self.compile_file_location: str = ''
        '''The compiled file location of the current program'''

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

    def get_compiled_file(self, lang_settings):
        '''get the file location of compiled file'''
        return lang_settings.get('compiledFormat', '{source}').format(source=self.file_location)

    def process_error(self, err_text):
        '''get error and real time taken'''
        match = self.error_reg.match(err_text)
        return match.group('error'), {
            'real': float(match.group('real')),
            'user': float(match.group('user')),
            'sys': float(match.group('sys')),
        }

    def setup_file(self, program: 'Program', lang_settings: Dict[str, str]) -> None:
        '''set up the file in file system'''
        workspace = Settings.get_workspace()
        if not path.exists(workspace):
            mkdir(workspace)
        file_name = lang_settings.get(
            'fileFormat', '{filename}').format(filename=program.uuid)
        self.file_location = path.join(workspace, file_name)
        with open(self.file_location, 'w') as file_obj:
            file_obj.write(program.code)

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

    def compile(self, program: 'Program', **_) -> None:
        lang_settings = program.settings
        language = program.language
        self.setup_file(program, lang_settings)
        compile_command = lang_settings.get('compileCommand', None)
        assert compile_command, f"compile command for {program.language} is not found!"

        compile_command = self.generate_compile_command(compile_command,
                                                        self.file_location,
                                                        language,
                                                        100,
                                                        int(lang_settings['memLimit'])
                                                        )

        process = subprocess.run(shlex.split(compile_command),
                                 encoding='utf-8',
                                 check=False,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE
                                 )
        _, errors = process.stdout, process.stderr
        error, _ = self.process_error(errors)
        if len(error.strip()) > 0:
            raise CompilationError()

        self.compile_file_location = self.get_compiled_file(lang_settings)

    def execute(self, program: 'Program', testcase: 'TestCase', **kwargs) -> None:
        assert self.compile_file_location, f'program {program.uuid} not compiled'
        test_input = testcase.input
        lang_settings = program.settings
        compiled_file_location = self.compile_file_location
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
        diposibles = program.settings.get('disposible')
        for item in diposibles:
            folder, file_name = path.split(self.file_location)
            item = item.format(source_name=path.splitext(file_name)[0])
            item = path.join(folder, item)
            if path.exists(item):
                unlink(item)
