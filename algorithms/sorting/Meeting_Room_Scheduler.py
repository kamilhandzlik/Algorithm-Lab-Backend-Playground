"""
Problem: Meeting Room Scheduler

Category:
- Algorithms
- Greedy
- Heap (Priority Queue)
- Scheduling

Description:
This project determines the minimum number of meeting
rooms required to schedule all meetings without overlap.

Each meeting is represented by a start time and an end time.

The algorithm sorts meetings by their start time and
uses a min-heap to keep track of the earliest ending meeting.

Whenever the earliest meeting has already finished,
its room can be reused.

This algorithm is commonly used in:
- calendar applications
- conference scheduling
- CPU task scheduling
- resource allocation
- booking systems

Features:
- greedy scheduling
- priority queue
- optimal room allocation
- scalable solution

Time Complexity:
- O(n log n)

Space Complexity:
- O(n)
"""

import heapq
import random
import unittest


def min_meeting_rooms(meetings):
    if not meetings:
        return 0

    meetings.sort()

    rooms = [meetings[0][1]]

    for start, end in meetings[1:]:
        if start >= rooms[0]:
            heapq.heappop(rooms)
        heapq.heappush(rooms, end)

    return len(rooms)


class TestMeetingRooms(unittest.TestCase):

    def test_single_room(self):
        meetings = [(1, 3), (3, 5), (5, 7)]

        self.assertEqual(min_meeting_rooms(meetings), 1)

    def test_two_rooms(self):
        meetings = [(1, 5), (2, 6), (3, 7)]
        self.assertEqual(min_meeting_rooms(meetings), 3)

    def test_empty(self):
        self.assertEqual(min_meeting_rooms([]), 0)


class TestRandom(unittest.TestCase):

    def test_random_input(self):
        for _ in range(100):
            meetings = []

            for _ in range(random.randint(1, 50)):
                start = random.randint(0, 100)
                end = random.randint(start + 1, start + 20)
                meetings.append((start, end))

            result = min_meeting_rooms(meetings)

            self.assertGreaterEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
