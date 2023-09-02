import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from completion_fn import CompletionFn
from test_suite import TestSuite

# Set verbose logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ExampleCompletionFn(CompletionFn):

    @staticmethod
    def complete(**kwargs) -> str:
        return "This is an example response from an LLM application."
    
EXAMPLE_TEST_CASES = [
    {
        "input": "This is an example input.",
        "expected": "This is an example response from an LLM application.",
        "grade_fn": "match",
    },
    {
        "input": "This is an example input 2.",
        "expected": "This is an example response from an LLM application.",
        "grade_fn": "match",
    },
    {
        "input": "This is an example input 3.",
        "expected": "This is an incorrect example response from an LLM application.",
        "grade_fn": "match",
    },
    {
        "input": "This is an example input 4.",
        "expected": "This is an example response from an LLM application.",
        "grade_fn": "not_fuzzy_match",
    }
]

def main():
    # Run the example test suite
    EXAMPLE_TEST_SUITE = TestSuite(name="maibench.example_test_suite", completion_fn=ExampleCompletionFn, test_cases=EXAMPLE_TEST_CASES)
    results = EXAMPLE_TEST_SUITE.run()
    print(results)

if __name__ == "__main__":
    main()