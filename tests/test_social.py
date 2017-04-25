import os
import unittest

from vk_info import get_vk_fans
from fb import get_fb_fans


class TestSocial(unittest.TestCase):
    def test_vk(self):
        self.assertIsInstance(get_vk_fans('nike'), int)

    def test_fb(self):
        self.setUp()
        self.assertIsInstance(get_fb_fans('nike'), int)
