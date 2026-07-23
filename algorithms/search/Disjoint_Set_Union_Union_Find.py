"""
Problem: Disjoint Set Union (Union-Find)

Category:
- Algorithms
- Graph Algorithms
- Disjoint Set Union
- Data Structures

Description:
This project implements the Disjoint Set Union (DSU),
also known as Union-Find.

The data structure efficiently manages a collection
of disjoint sets and supports two fundamental operations:

- find(): determines the representative of a set
- union(): merges two different sets

The implementation uses Path Compression and Union by Rank,
providing nearly constant time complexity for operations.

This algorithm is commonly used in:
- Kruskal's Minimum Spanning Tree
- cycle detection
- network connectivity
- social networks
- image segmentation
- clustering

Features:
- path compression
- union by rank
- efficient connectivity queries
- scalable implementation

Time Complexity:
- find(): O(α(n))
- union(): O(α(n))

Space Complexity:
- O(n)
"""

import random
import unittest


class DisjointSet:

    def __init__(self, size):

        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, node):

        if self.parent[node] != node:
            self.parent[node] = self.find(
                self.parent[node]
            )

        return self.parent[node]

    def union(self, first, second):

        root_first = self.find(first)
        root_second = self.find(second)

        if root_first == root_second:
            return False

        if self.rank[root_first] < self.rank[root_second]:
            self.parent[root_first] = root_second

        elif self.rank[root_first] > self.rank[root_second]:
            self.parent[root_second] = root_first

        else:
            self.parent[root_second] = root_first
            self.rank[root_first] += 1

        return True

    def connected(self, first, second):
        return self.find(first) == self.find(second)


class TestDisjointSet(unittest.TestCase):

    def test_union(self):
        dsu = DisjointSet(5)

        dsu.union(0, 1)

        self.assertTrue(dsu.connected(0, 1))

    def test_not_connected(self):
        dsu = DisjointSet(5)

        self.assertFalse(dsu.connected(0, 4))

    def test_multiple_unions(self):
        dsu = DisjointSet(6)

        dsu.union(0, 1)
        dsu.union(1, 2)
        dsu.union(2, 3)

        self.assertTrue(dsu.connected(0, 3))

    def test_same_set(self):
        dsu = DisjointSet(4)

        dsu.union(0, 1)

        self.assertFalse(dsu.union(0, 1))


class TestRandom(unittest.TestCase):

    def test_random_operations(self):
        size = 50

        dsu = DisjointSet(size)

        for _ in range(200):
            first = random.randint(0, size - 1)

            second = random.randint(0, size - 1)

            dsu.union(first, second)

            self.assertTrue(dsu.connected(first, second))


if __name__ == "__main__":
    unittest.main()
