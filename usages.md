# Usages

## Program Class

The program class represents a program to be executed.

### Simple Usage

```python
from executioner.sandbox.firejail import FireJail
from executioner.program import Program
from executioner.evaluate import TestCase

pgm = Program("print('hello world')", 'python3', FireJail())
pgm.compile()
testcase = TestCase()
pgm.execute(testcase)
print(testcase.real_output)

```

### As ContextManager

```python
from executioner.sandbox.firejail import FireJail
from executioner.program import Program
from executioner.evaluate import TestCase
with Program("print('hello world')", 'python3', FireJail()) as pgm:
    pgm.compile()
    testcase = TestCase()
    pgm.execute(testcase)
    print(testcase.real_output)

```

## Evaluation Class

The Evaluation class is used to execute and evaluate a program on multiple testcases and metrics.

### Simple Usage

```python
from executioner.sandbox.firejail import FireJail
from executioner.program import Program
from executioner.evaluate import TestCase, Evaluation
from executioner.metric.equal import Equal
with Program('''
a = int(input())
print(a)
''', 'python3', FireJail()) as pgm:
    pgm.compile()
    evaluator = Evaluation(
        pgm,
        [TestCase(str(x), str(x)) for x in range(10)],
        [Equal()]
    )
    evaluator.evaluate()
    print(all([testcase.scores['Equal'] == 1 for testcase in evaluator.testcases]))
```
