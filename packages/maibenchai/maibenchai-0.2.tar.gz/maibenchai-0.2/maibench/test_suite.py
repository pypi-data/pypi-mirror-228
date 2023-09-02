"""
A base class for test suites.
"""
import logging
import json
import os
import sys
import time
import requests
from typing import Dict, List
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from completion_fn import CompletionFn
from grader import Grader


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
API_URL = "https://backend.maibench.com/v2"


class TestSuite:
    def __init__(self, name: str, completion_fn: CompletionFn, seed: int = 1, test_cases: List[Dict[str, str]] = None):
        self.name = name
        self.completion_fn = completion_fn
        self.seed = seed
        self.test_cases = test_cases
        self.completions = None

    @staticmethod
    def get_single_completion(completion_fn: CompletionFn, **kwargs) -> str:
        """Get a single completion."""
        start_time = time.time()
        completion = completion_fn.complete(**kwargs)
        end_time = time.time()
        logger.info(f"Completion took {end_time - start_time} seconds.")
        return completion, end_time - start_time

    @staticmethod
    def get_all_completions(completion_fn: CompletionFn, **kwargs) -> List[str]:
        """Get the completions for a sample.

        Args:
            completion_fn: The completion function to use.
            kwargs: The arguments to pass to the completion function. These should be lists of the same length.

        Example:
            >>> get_all_completions(completion_fn, input=["This is an example input.", "This is another example input."])
        """
        # Get the length of the lists in kwargs to know how many times to loop
        n = len(next(iter(kwargs.values())))

        # Initialize a list to store the completions and associated run times.
        completions = []
        run_times = []

        # Loop over each index up to n
        for i in range(n):
            # Prepare a dictionary with the single value at index i for each keyword argument
            single_kwargs = {k: v[i] for k, v in kwargs.items()}

            # Get the completion for this set of arguments and add it to the list
            completion, run_time = TestSuite.get_single_completion(completion_fn, **single_kwargs)
            completions.append(completion)
            run_times.append(run_time)

        return completions, run_times

    def run(self) -> Dict[str, float]:
        """Run all of the test suite cases and upload the results."""
        start_time = time.time()

        # Parse test cases and get the completions for each test case
        inputs = [test_case["input"] for test_case in self.test_cases]
        expected_outputs = [test_case["expected"] for test_case in self.test_cases]
        grading_fns = [test_case["grade_fn"] for test_case in self.test_cases]
        # Run the completion function on each input
        logger.info("Running completion function on %s inputs...", len(inputs))
        completions, run_times = TestSuite.get_all_completions(completion_fn=self.completion_fn, input=inputs)
        grades = self.grade_all_samples(inputs, expected_outputs, completions, grading_fns)
        average_score = sum(grades) / len(grades)

        # Prepare the results to post to the API
        results = self.test_cases.copy()
        assert len(results) == len(grades) == len(completions) == len(run_times), "All lists must be the same length."
        for i, (completion, grade, run_time) in enumerate(zip(completions, grades, run_times)):
            results[i]["grade"] = grade
            results[i]["completion"] = completion
            results[i]["run_time"] = run_time
        end_time = time.time()
        created_at = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S.%f')

        # Post the results to the API
        response = TestSuite.post_results(
            num_events=len(self.test_cases),
            score=average_score,
            events=json.dumps(results),
            created_by="test-user",
            created_at=created_at,
            execution_time=end_time - start_time,
            )
        return results, response['id']
    
    @staticmethod
    def post_results(num_events: int, score: float, events: str, created_by, created_at, execution_time) -> None:
        """Post the results to the API."""
        response = requests.post(
            f"{API_URL}/results",
            json={
                "num_events": num_events,
                "score": score,
                "events": events,
                "created_by": created_by,
                "created_at": created_at,
                "execution_time": execution_time,
                "completed": True
            },
            timeout=5000
        )
        if response.status_code != 200:
            logger.error(f"Error posting results to API: {response.text}")
            return -1
        else:
            logger.info("Results posted to API.")
            return response.json()

    @staticmethod
    def grade_all_samples(inputs: List[str], expected_outputs: List[str], completions: List[str], grading_fns: List[str]) -> Dict[str, float]:
        """Grade all samples."""
        assert len(inputs) == len(expected_outputs) == len(completions) == len(grading_fns), "All lists must be the same length."
        grades = []
        for expected_output, completion, grading_fn in zip(expected_outputs, completions, grading_fns):
            assert getattr(Grader, grading_fn), f"Grading function {grading_fn} not found in Grader class."
            grade = getattr(Grader, grading_fn)(completion, expected_output)
            grades.append(grade)

        return grades