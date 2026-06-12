"""
Problem: Workflow Automation System using Interpreter Pattern

Category:
- Design Patterns
- Interpreter Pattern
- Workflow Automation
- Rule Processing

Description:
This project implements a simple workflow automation system
using the Interpreter design pattern.

The Interpreter Pattern defines a grammar and provides
an interpreter to evaluate expressions according to that grammar.

In this example:
- expressions represent workflow rules
- rules are evaluated against a context
- complex conditions can be built from simpler ones

Example Rules:
- user_is_admin AND account_is_active
- user_is_admin OR account_is_active

This pattern is commonly used in:
- rule engines
- search filters
- authorization systems
- query languages
- workflow automation

Features:
- rule evaluation
- composable expressions
- reusable logic
- flexible workflow definitions

Time Complexity:
- Expression evaluation: O(n)

Space Complexity:
- O(n)
"""

import unittest
import random
from abc import ABC, abstractmethod


class Expression(ABC):

    @abstractmethod
    def interpret(self, context):
        pass


class BooleanExpression(Expression):

    def __init__(self, key):

        self.key = key

    def interpret(self, context):

        return context.get(
            self.key,
            False
        )


class AndExpression(Expression):

    def __init__(
        self,
        left,
        right
    ):

        self.left = left
        self.right = right

    def interpret(self, context):

        return (
            self.left.interpret(context)
            and
            self.right.interpret(context)
        )


class OrExpression(Expression):

    def __init__(
        self,
        left,
        right
    ):

        self.left = left
        self.right = right

    def interpret(self, context):

        return (
            self.left.interpret(context)
            or
            self.right.interpret(context)
        )


class TestInterpreterPattern(
    unittest.TestCase
):

    def test_and_expression(self):

        expression = AndExpression(
            BooleanExpression(
                "is_admin"
            ),
            BooleanExpression(
                "is_active"
            )
        )

        context = {
            "is_admin": True,
            "is_active": True
        }

        self.assertTrue(
            expression.interpret(
                context
            )
        )

    def test_and_expression_false(self):

        expression = AndExpression(
            BooleanExpression(
                "is_admin"
            ),
            BooleanExpression(
                "is_active"
            )
        )

        context = {
            "is_admin": True,
            "is_active": False
        }

        self.assertFalse(
            expression.interpret(
                context
            )
        )

    def test_or_expression(self):

        expression = OrExpression(
            BooleanExpression(
                "is_admin"
            ),
            BooleanExpression(
                "is_active"
            )
        )

        context = {
            "is_admin": False,
            "is_active": True
        }

        self.assertTrue(
            expression.interpret(
                context
            )
        )

    def test_nested_expression(self):

        expression = AndExpression(

            OrExpression(
                BooleanExpression(
                    "is_admin"
                ),
                BooleanExpression(
                    "is_manager"
                )
            ),

            BooleanExpression(
                "is_active"
            )
        )

        context = {
            "is_admin": False,
            "is_manager": True,
            "is_active": True
        }

        self.assertTrue(
            expression.interpret(
                context
            )
        )


class TestRandom(unittest.TestCase):

    def test_random_contexts(self):

        expression = AndExpression(
            BooleanExpression(
                "flag_a"
            ),
            BooleanExpression(
                "flag_b"
            )
        )

        for _ in range(100):

            context = {
                "flag_a": random.choice(
                    [True, False]
                ),
                "flag_b": random.choice(
                    [True, False]
                )
            }

            expected = (
                context["flag_a"]
                and
                context["flag_b"]
            )

            self.assertEqual(
                expression.interpret(
                    context
                ),
                expected
            )


if __name__ == "__main__":

    unittest.main()