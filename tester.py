import subprocess
import shlex
import re
process = subprocess.run(shlex.split('time -p python trial.py'),
                         input='', encoding='utf-8',
                         check=False,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

output, errors = process.stdout, process.stderr
error_reg = re.compile(
    r'''(?s)(?P<error>.*)real (?P<real>[0-9]*[.][0-9]*)\nuser (?P<user>[0-9]*[.][0-9]*)\nsys (?P<sys>[0-9]*[.][0-9]*)'''
)

reg = error_reg.match(errors)