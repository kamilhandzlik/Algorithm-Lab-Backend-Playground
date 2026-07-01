"""
Problem: Message Queue using Producer-Consumer Pattern

Category:
- Concurrency
- Producer-Consumer Pattern
- Queue
- Task Processing

Description:
This project implements a simple message queue using
the Producer-Consumer pattern.

The Producer-Consumer Pattern separates message creation
from message processing. Producers generate messages and
place them into a queue, while consumers retrieve and
process them independently.

In this example:
- Producer adds messages to the queue
- Consumer processes messages
- MessageQueue stores pending messages

This pattern is commonly used in:
- RabbitMQ
- Apache Kafka
- Celery
- task queues
- logging systems
- event-driven architectures

Features:
- FIFO queue
- decoupled producer and consumer
- message processing
- reusable queue implementation

Time Complexity:
- Enqueue: O(1)
- Dequeue: O(1)

Space Complexity:
- O(n)
"""

import random
import string
import unittest
from collections import deque


class MessageQueue:

    def __init__(self):
        self.queue = deque()

    def enqueue(self, message):
        self.queue.append(message)

    def dequeue(self):

        if self.is_empty():
            return None

        return self.queue.popleft()

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)


class Producer:

    def __init__(self, queue):
        self.queue = queue

    def produce(self, message):
        self.queue.enqueue(message)


class Consumer:

    def __init__(self, queue):
        self.queue = queue

    def consume(self):
        return self.queue.dequeue()


class TestProducerConsumerPattern(unittest.TestCase):

    def test_enqueue_message(self):

        queue = MessageQueue()

        producer = Producer(queue)

        producer.produce("Hello")

        self.assertEqual(queue.size(), 1)

    def test_dequeue_message(self):

        queue = MessageQueue()

        producer = Producer(queue)
        consumer = Consumer(queue)

        producer.produce("Hello")

        self.assertEqual(
            consumer.consume(),
            "Hello"
        )

    def test_fifo_order(self):

        queue = MessageQueue()

        producer = Producer(queue)
        consumer = Consumer(queue)

        producer.produce("A")
        producer.produce("B")
        producer.produce("C")

        self.assertEqual(consumer.consume(), "A")
        self.assertEqual(consumer.consume(), "B")
        self.assertEqual(consumer.consume(), "C")

    def test_empty_queue(self):

        queue = MessageQueue()

        consumer = Consumer(queue)

        self.assertIsNone(
            consumer.consume()
        )


class TestRandom(unittest.TestCase):

    def random_message(self):

        length = random.randint(5, 15)

        return "".join(
            random.choice(string.ascii_letters)
            for _ in range(length)
        )

    def test_random_messages(self):

        queue = MessageQueue()

        producer = Producer(queue)
        consumer = Consumer(queue)

        messages = []

        for _ in range(100):

            message = self.random_message()

            messages.append(message)

            producer.produce(message)

        received = []

        while not queue.is_empty():

            received.append(
                consumer.consume()
            )

        self.assertEqual(
            messages,
            received
        )


if __name__ == "__main__":
    unittest.main()