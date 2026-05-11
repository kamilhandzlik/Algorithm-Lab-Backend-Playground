"""
Problem: Group Anagrams
Difficulty: Medium
Category: Arrays / HashMap / Strings

Time Complexity: O(n * k log k)
k = average word length

Space Complexity: O(n)..
"""
import unittest
import random
import string

from collections import defaultdict


def group_anagrams(words):
    groups = defaultdict(list)

    for word in words:
        key = ''.join(sorted(word))

        groups[key].append(word)

    return list(groups.values())


class TestGroupAnagrams(unittest.TestCase):

    def normalize(self, result):
        return sorted(
            [sorted(group) for group in result]
        )

    def test_basic(self):
        words = ["eat", "tea", "tan", "ate", "nat", "bat"]

        expected = [
            ["eat", "tea", "ate"],
            ["tan", "nat"],
            ["bat"]
        ]

        self.assertEqual(
            self.normalize(group_anagrams(words)),
            self.normalize(expected)
        )

    def test_empty(self):
        self.assertEqual(
            group_anagrams([]),
            []
        )

    def test_single(self):
        self.assertEqual(
            group_anagrams(["abc"]),
            [["abc"]]
        )

    def test_duplicates(self):
        result = group_anagrams(["a", "a"])

        self.assertEqual(
            self.normalize(result),
            [["a", "a"]]
        )

    def test_no_anagrams(self):
        words = ["abc", "def", "ghi"]

        result = group_anagrams(words)

        self.assertEqual(
            self.normalize(result),
            [["abc"], ["def"], ["ghi"]]
        )


def brute_group_anagrams(words):
    groups = []

    used = [False] * len(words)

    for i in range(len(words)):

        if used[i]:
            continue

        current = [words[i]]
        used[i] = True

        for j in range(i + 1, len(words)):

            if not used[j]:

                if sorted(words[i]) == sorted(words[j]):
                    current.append(words[j])
                    used[j] = True

        groups.append(sorted(current))

    return sorted(groups)


class TestRandom(unittest.TestCase):

    def normalize(self, result):
        return sorted(
            [sorted(group) for group in result]
        )

    def random_word(self):
        length = random.randint(1, 5)

        return ''.join(
            random.choice(string.ascii_lowercase)
            for _ in range(length)
        )

    def test_random_cases(self):
        for _ in range(100):
            size = random.randint(0, 10)

            words = [
                self.random_word()
                for _ in range(size)
            ]

            self.assertEqual(
                self.normalize(group_anagrams(words)),
                self.normalize(brute_group_anagrams(words))
            )
