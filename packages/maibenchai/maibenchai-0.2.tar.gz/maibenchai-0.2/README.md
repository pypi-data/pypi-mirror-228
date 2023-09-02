### maibench Python SDK

Python toolings to help run evaluations on large langauge model chains.

[![](https://img.shields.io/badge/Visit%20Us!-maibench.ai-brightgreen)](https://maibench.ai)

 ## Getting started
 First, install the package.

 `pip install maibenchai`

Next, create a completion function. This maps different inputs your LLM application response. Here's an example.

```
 from maibench import CompletionFn

 class ExampleCompletionFn(CompletionFn):
    @staticmethod
    def complete(**kwargs) -> str:
        return "This is an example response from an LLM application."
```

Next, create some text cases. These test cases should each contain the input kwargs of your completion function in additon to an expected output and a grade_fn. Supported grade functions are currently `match`, `includes`, `fuzzy_match`, `not_match`, `not_includes`, and `not_fuzzy_match`. More complex grading functions and model-based grading is coming soon.

``` 
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
]
 ```

 Create and run.

 ```
EXAMPLE_TEST_SUITE = TestSuite(name="maibench.example_test_suite", completion_fn=ExampleCompletionFn, test_cases=EXAMPLE_TEST_CASES)
results, id = EXAMPLE_TEST_SUITE.run()
```

See results at https://maibench.ai/individual-result?id=[INSERT ID]

### We hope you enjoy!

Contact support@maibench.ai with any questions.