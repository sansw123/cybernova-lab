import unittest
from unittest.mock import patch

from cybernova.quiz import QUESTIONS, run_quiz


class QuizTests(unittest.TestCase):
    def test_quiz_reprompts_and_scores_answer(self):
        answers = iter(("not-a-number", str(QUESTIONS[0].answer + 1)))
        output = []
        with patch("cybernova.quiz.random.sample", return_value=[QUESTIONS[0]]):
            score = run_quiz(1, input_fn=lambda _prompt: next(answers), output_fn=output.append)
        self.assertEqual(score, (1, 1))
        self.assertTrue(any("Please enter" in line for line in output))
        self.assertIn("Correct!", output)

    def test_question_count_is_capped(self):
        chosen = list(QUESTIONS)
        answers = iter(str(question.answer + 1) for question in chosen)
        with patch("cybernova.quiz.random.sample", return_value=chosen):
            score, total = run_quiz(
                999,
                input_fn=lambda _prompt: next(answers),
                output_fn=lambda _line: None,
            )
        self.assertEqual((score, total), (len(QUESTIONS), len(QUESTIONS)))


if __name__ == "__main__":
    unittest.main()

