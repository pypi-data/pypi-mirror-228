from typing import Awaitable, Callable


class Grader:
    @staticmethod
    def match(submission: str, expected: str) -> int:
        result = int(submission.startswith(expected))
        return result

    @staticmethod
    def includes(submission: str, expected: str) -> int:
        result = int(expected in submission)
        return result

    @staticmethod
    def fuzzy_match(submission: str, expected: str) -> int:
        result = int(submission in expected or expected in submission)
        return result

    @staticmethod
    def not_match(submission: str, expected: str) -> int:
        result = int(not submission.startswith(expected))
        return result

    @staticmethod
    def not_includes(submission: str, expected: str) -> int:
        result = int(not expected in submission)
        return result

    @staticmethod
    def not_fuzzy_match(submission: str, expected: str) -> int:
        result = int(not (submission in expected or expected in submission))
        return result

    @staticmethod
    def custom(submission: str, eval_function: Callable[[str], bool]) -> int:
        result = eval_function(submission)
        return result

    @staticmethod
    async def custom_async(submission: str, evaluation_func: Callable[[str], Awaitable[bool]]) -> int:
        result = await evaluation_func(submission)
        return result