'''CLI access to executioner'''
import argparse
from typing import List, Dict
from itertools import zip_longest
from io import TextIOWrapper
from tabulate import tabulate
from .metric import Equal, BaseMetrics
from .sandbox.firejail import FireJail
from .program import Program
from .evaluate import TestCase, Evaluation


def setup_testcases(args: argparse.Namespace) -> List[TestCase]:
    '''Create the list of testcases from arguments'''
    inputs = []
    for inp_file in args.input:
        inputs.append(inp_file.read() if isinstance(
            inp_file, TextIOWrapper) else "")
        inp_file.close()
    outputs = []
    for output_file in args.output:
        outputs.append(output_file.read() if isinstance(
            output_file, TextIOWrapper) else "")
        output_file.close()

    testcase = [TestCase(testcase_input=inp, testcase_output=out)
                for (inp, out) in zip_longest(inputs, outputs, fillvalue="")]
    return testcase


def execute_evaluation(pgm: Program, testcases: List[TestCase], metrics=List[BaseMetrics]) -> None:
    '''Execute multiple testcases as an evaluation'''
    evaluator = Evaluation(pgm, testcases, metrics)
    evaluator.evaluate()


def execute_testcase(pgm: Program, testcase: TestCase) -> None:
    '''Execute a single testcase and print info'''
    pgm.execute(testcase)
    print(
        f"Time:{testcase.time}, Error: {testcase.error}\nOutput:\n {testcase.real_output}")


def combine_scores(testcases: List[TestCase], metrics=List[BaseMetrics]) -> Dict[str, List[int]]:
    '''Combine multiple score dictionaries'''
    scores = {str(x): [] for x in metrics}
    for testcase in testcases:
        for metric in metrics:
            scores[str(metric)].append(
                testcase.scores.get(str(metric), 'N/A'))
    return scores


def display_evaluation(testcases: List[TestCase], metrics=List[BaseMetrics]) -> None:
    '''Tabulate testcase scores'''
    print("REPORT")
    scores = combine_scores(testcases, metrics)
    print(tabulate(
        scores,
        headers="keys",
        showindex="always",
    ))


def main():
    '''Entrypoint for CLI'''
    parser = argparse.ArgumentParser(description='execute code')

    parser.add_argument("file", type=open,
                        help="The source file to be executed")
    parser.add_argument("-l", "--language", required=True,
                        help="The language of the source file")
    parser.add_argument("-s", "--sandbox", default=FireJail(),
                        help="The sandbox to be used (default: FireJail) [TODO]")
    parser.add_argument("-m", "--metrics", nargs='*', default=[Equal()],
                        help="The metrics to be used to evaluate the outputs [TODO]")
    parser.add_argument("-i", "--input", nargs='*', default=[], type=open,
                        help="The files to be used as input for program (default: None)")
    parser.add_argument("-o", "--output", nargs='*', default=[], type=open,
                        help="The files to be used as expected output for program, \
                            if output is specified, \
                            number of outputs must match number of inputs (Default: None)")
    args = parser.parse_args()

    source = args.file.read()
    args.file.close()

    testcases = setup_testcases(args)
    with Program(source, args.language, args.sandbox)as pgm:
        if len(args.output) >= 1:
            assert len(args.output) == len(args.input), \
                "if output is given, number of outputs should match number of inputs"
            execute_evaluation(pgm, testcases, args.metrics)
            display_evaluation(testcases, args.metrics)
        elif len(args.input) >= 1:
            pgm.compile()
            for testcase in testcases:
                execute_testcase(pgm, testcase)
        else:
            pgm.compile()
            execute_testcase(pgm,TestCase())


if __name__ == '__main__':
    main()
