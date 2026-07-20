"""
Problem: Least Recently Used (LRU) Cache

Category:
- Algorithms
- Hash Table
- Doubly Linked List
- Cache

Description:
This project implements an LRU (Least Recently Used)
cache.

The cache stores a limited number of key-value pairs.
Whenever the capacity is exceeded, the least recently
used item is removed automatically.

The implementation combines a hash table for O(1)
lookups and a doubly linked list for O(1) insertion,
removal and updating of recently accessed items.

This algorithm is commonly used in:
- Redis
- web browsers
- operating systems
- database engines
- CDN caches

Features:
- O(1) lookup
- O(1) insertion
- O(1) eviction
- automatic cache replacement

Time Complexity:
- get(): O(1)
- put(): O(1)

Space Complexity:
- O(capacity)
"""

import random
import unittest


class Node:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:

    def __init__(self, capacity):

        self.capacity = capacity
        self.cache = {}

        self.head = Node(0, 0)
        self.tail = Node(0, 0)

        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):

        previous = node.prev
        following = node.next

        previous.next = following
        following.prev = previous

    def _insert(self, node):

        previous = self.tail.prev

        previous.next = node
        node.prev = previous

        node.next = self.tail
        self.tail.prev = node

    def get(self, key):

        if key not in self.cache:
            return -1

        node = self.cache[key]

        self._remove(node)
        self._insert(node)

        return node.value

    def put(self, key, value):

        if key in self.cache:
            self._remove(self.cache[key])

        node = Node(key, value)

        self.cache[key] = node

        self._insert(node)

        if len(self.cache) > self.capacity:
            lru = self.head.next

            self._remove(lru)

            del self.cache[lru.key]


class TestLRUCache(unittest.TestCase):

    def test_put_and_get(self):
        cache = LRUCache(2)

        cache.put(1, "A")

        self.assertEqual(cache.get(1), "A")

    def test_eviction(self):
        cache = LRUCache(2)

        cache.put(1, "A")
        cache.put(2, "B")
        cache.put(3, "C")

        self.assertEqual(cache.get(1), -1)

    def test_recently_used(self):
        cache = LRUCache(2)

        cache.put(1, "A")
        cache.put(2, "B")

        cache.get(1)

        cache.put(3, "C")

        self.assertEqual(cache.get(2), -1)

    def test_update_value(self):
        cache = LRUCache(2)

        cache.put(1, "A")
        cache.put(1, "B")

        self.assertEqual(cache.get(1), "B")


class TestRandom(unittest.TestCase):

    def test_random_operations(self):

        cache = LRUCache(5)

        keys = list(range(10))

        for _ in range(100):

            key = random.choice(keys)

            if random.choice([True, False]):

                cache.put(key, random.randint(1, 1000))

            else:

                result = cache.get(key)

                self.assertTrue(result == -1 or isinstance(result, int))


if __name__ == "__main__":
    unittest.main()
