"""
Problem: Task Queue System using Producer-Consumer Pattern

Category:
- Design Patterns
- Producer-Consumer Pattern
- Queue Processing
- Multithreading Concepts

Description:
This project implements a simple task queue system using
the Producer-Consumer design pattern.

The producer adds tasks to the queue while the consumer
processes them in FIFO order.

This pattern is commonly used in:
- background job systems
- message brokers
- task schedulers
- async processing
- distributed systems

Features:
- task queue management
- producer-consumer workflow
- FIFO processing
- simple task execution simulation

Time Complexity:
- Add task: O(1)
- Process task: O(1)

Space Complexity:
- O(n)
"""

import unittest
import random
import string
from collections import deque


class TaskQueue:

    def __init__(self):

        self.queue = deque()

    def add_task(self, task):

        self.queue.append(task)

    def process_task(self):

        if not self.queue:
            return None

        return self.queue.popleft()

    def size(self):

        return len(self.queue)


class TestTaskQueue(unittest.TestCase):

    def test_add_task(self):

        queue = TaskQueue()

        queue.add_task("send email")

        self.assertEqual(
            queue.size(),
            1
        )

    def test_process_task(self):

        queue = TaskQueue()

        queue.add_task("task1")

        self.assertEqual(
            queue.process_task(),
            "task1"
        )

    def test_fifo_order(self):

        queue = TaskQueue()

        queue.add_task("task1")
        queue.add_task("task2")

        self.assertEqual(
            queue.process_task(),
            "task1"
        )

        self.assertEqual(
            queue.process_task(),
            "task2"
        )

    def test_empty_queue(self):

        queue = TaskQueue()

        self.assertIsNone(
            queue.process_task()
        )


class TestRandom(unittest.TestCase):

    def random_task(self):

        length = random.randint(5, 10)

        return ''.join(
            random.choice(string.ascii_letters)
            for _ in range(length)
        )

    def test_random_tasks(self):

        queue = TaskQueue()

        tasks = []

        for _ in range(50):

            task = self.random_task()

            tasks.append(task)

            queue.add_task(task)

        processed = []

        while queue.size() > 0:

            processed.append(
                queue.process_task()
            )

        self.assertEqual(
            tasks,
            processed
        )


if __name__ == "__main__":

    unittest.main()