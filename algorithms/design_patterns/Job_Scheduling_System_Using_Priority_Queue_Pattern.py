"""
Problem: Job Scheduling System using Priority Queue Pattern

Category:
- Design Patterns
- Priority Queue
- Task Scheduling
- Resource Management

Description:
This project implements a simple job scheduling system
using a priority queue.

Tasks are executed based on their priority rather than
the order in which they were added.

In this example:
- each job has a name and priority
- lower priority values indicate higher importance
- the scheduler always executes the highest-priority job first

This pattern is commonly used in:
- operating systems
- task schedulers
- CI/CD pipelines
- background workers
- cloud orchestration systems

Features:
- priority-based execution
- dynamic job insertion
- efficient scheduling
- predictable execution order

Time Complexity:
- Add job: O(log n)
- Execute job: O(log n)

Space Complexity:
- O(n)
"""
import unittest
import random
import heapq


class Job:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

    def __lt__(self, other):
        return (self.priority < other.priority)


class JobScheduler:
    def __init__(self):
        self.jobs = []

    def add_job(self, job):
        heapq.heappush(self.jobs, job)

    def execute_job(self):
        if not self.jobs:
            return None

        return heapq.heappop(self.jobs)

    def size(self):
        return len(self.jobs)


class TestJobScheduler(
    unittest.TestCase
):

    def test_add_job(self):
        scheduler = JobScheduler()

        scheduler.add_job(Job("Backup", 1))

        self.assertEqual(scheduler.size(), 1)

    def test_execute_highest_priority(self):
        scheduler = JobScheduler()

        scheduler.add_job(Job("Analytics", 5))

        scheduler.add_job(Job("Backup", 1))

        result = scheduler.execute_job()

        self.assertEqual(result.name, "Backup")

    def test_empty_scheduler(self):
        scheduler = JobScheduler()

        self.assertIsNone(scheduler.execute_job())

    def test_multiple_jobs(self):
        scheduler = JobScheduler()
        scheduler.add_job(
            Job("Low", 10))

        scheduler.add_job(
            Job("Medium", 5))

        scheduler.add_job(
            Job("High", 1))

        self.assertEqual(scheduler.execute_job().name, "High")

        self.assertEqual(scheduler.execute_job().name, "Medium")

        self.assertEqual(scheduler.execute_job().name, "Low")


class TestRandom(unittest.TestCase):

    def test_random_priorities(self):

        scheduler = JobScheduler()

        priorities = []

        for i in range(100):
            priority = random.randint(1, 1000)

            priorities.append(priority)

            scheduler.add_job(

                Job(f"Job{i}", priority))

        priorities.sort()

        for expected in priorities:
            job = scheduler.execute_job()

            self.assertEqual(job.priority, expected)


if __name__ == "__main__":
    unittest.main()
