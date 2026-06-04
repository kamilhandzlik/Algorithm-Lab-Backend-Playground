"""
Problem: Image Processing System using Flyweight Pattern

Category:
- Design Patterns
- Flyweight Pattern
- Memory Optimization
- Resource Management

Description:
This project implements a simple image processing system
using the Flyweight design pattern.

The Flyweight Pattern minimizes memory usage by sharing
common object data instead of creating duplicate instances.

In this example:
- images with the same file name are reused
- only one object exists for each unique image
- repeated requests return the same instance

This pattern is commonly used in:
- game engines
- graphics editors
- caching systems
- map rendering
- icon libraries

Features:
- object reuse
- memory optimization
- shared resources
- instance caching

Time Complexity:
- Get image: O(1)

Space Complexity:
- O(unique_images)
"""

import unittest
import random
import string


class Image:

    def __init__(self, filename):

        self.filename = filename

    def render(self):

        return f"Rendering {self.filename}"


class ImageFactory:

    _images = {}

    @classmethod
    def get_image(cls, filename):

        if filename not in cls._images:

            cls._images[filename] = Image(
                filename
            )

        return cls._images[filename]

    @classmethod
    def cache_size(cls):

        return len(cls._images)

    @classmethod
    def clear_cache(cls):

        cls._images.clear()


class TestFlyweightPattern(unittest.TestCase):

    def setUp(self):

        ImageFactory.clear_cache()

    def test_same_instance(self):

        image1 = ImageFactory.get_image(
            "hero.png"
        )

        image2 = ImageFactory.get_image(
            "hero.png"
        )

        self.assertIs(
            image1,
            image2
        )

    def test_different_images(self):

        image1 = ImageFactory.get_image(
            "hero.png"
        )

        image2 = ImageFactory.get_image(
            "enemy.png"
        )

        self.assertIsNot(
            image1,
            image2
        )

    def test_cache_size(self):

        ImageFactory.get_image(
            "a.png"
        )

        ImageFactory.get_image(
            "b.png"
        )

        ImageFactory.get_image(
            "a.png"
        )

        self.assertEqual(
            ImageFactory.cache_size(),
            2
        )

    def test_render(self):

        image = ImageFactory.get_image(
            "map.png"
        )

        self.assertEqual(
            image.render(),
            "Rendering map.png"
        )


class TestRandom(unittest.TestCase):

    def setUp(self):

        ImageFactory.clear_cache()

    def random_filename(self):

        names = [
            "hero",
            "enemy",
            "tree",
            "rock",
            "house"
        ]

        return (
            random.choice(names)
            + ".png"
        )

    def test_random_image_requests(self):

        created = set()

        for _ in range(100):

            filename = self.random_filename()

            created.add(filename)

            ImageFactory.get_image(
                filename
            )

        self.assertEqual(
            ImageFactory.cache_size(),
            len(created)
        )


if __name__ == "__main__":

    unittest.main()