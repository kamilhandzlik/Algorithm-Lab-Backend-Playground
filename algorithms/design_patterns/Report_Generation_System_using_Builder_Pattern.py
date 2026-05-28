"""
Problem: Report Generation System using Builder Pattern

Category:
- Design Patterns
- Builder Pattern
- Report Generation
- Object Construction

Description:
This project implements a simple report generation system
using the Builder design pattern.

The Builder Pattern separates the construction process
of a complex object from its representation.

In this example:
- ReportBuilder creates different parts of the report
- ReportDirector controls the building process
- Report represents the final generated object

This pattern is commonly used in:
- PDF generation systems
- API request builders
- SQL query builders
- configuration systems
- document generation

Features:
- step-by-step object construction
- flexible report generation
- reusable building process
- clean object creation logic

Time Complexity:
- Build report: O(n)

Space Complexity:
- O(n)
"""

import unittest
import random
import string


class Report:

    def __init__(self):

        self.title = ""
        self.content = ""
        self.footer = ""

    def generate(self):

        return (
            f"{self.title}\n"
            f"{self.content}\n"
            f"{self.footer}"
        )


class ReportBuilder:

    def __init__(self):

        self.report = Report()

    def add_title(self, title):

        self.report.title = title

    def add_content(self, content):

        self.report.content = content

    def add_footer(self, footer):

        self.report.footer = footer

    def build(self):

        return self.report


class ReportDirector:

    def __init__(self, builder):

        self.builder = builder

    def create_report(
        self,
        title,
        content,
        footer
    ):

        self.builder.add_title(title)
        self.builder.add_content(content)
        self.builder.add_footer(footer)

        return self.builder.build()


class TestBuilderPattern(unittest.TestCase):

    def test_report_generation(self):

        builder = ReportBuilder()

        director = ReportDirector(
            builder
        )

        report = director.create_report(
            "Monthly Report",
            "Sales increased",
            "Confidential"
        )

        expected = (
            "Monthly Report\n"
            "Sales increased\n"
            "Confidential"
        )

        self.assertEqual(
            report.generate(),
            expected
        )

    def test_empty_report(self):

        builder = ReportBuilder()

        report = builder.build()

        expected = "\n\n"

        self.assertEqual(
            report.generate(),
            expected
        )


class TestRandom(unittest.TestCase):

    def random_text(self):

        length = random.randint(5, 15)

        return ''.join(
            random.choice(
                string.ascii_letters
            )
            for _ in range(length)
        )

    def test_random_reports(self):

        for _ in range(30):

            title = self.random_text()
            content = self.random_text()
            footer = self.random_text()

            builder = ReportBuilder()

            director = ReportDirector(
                builder
            )

            report = director.create_report(
                title,
                content,
                footer
            )

            generated = report.generate()

            self.assertIn(
                title,
                generated
            )

            self.assertIn(
                content,
                generated
            )

            self.assertIn(
                footer,
                generated
            )


if __name__ == "__main__":

    unittest.main()