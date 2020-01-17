from parameterized import parameterized
from topics.helpers import parse_html
import unittest


class HelpersTestCase(unittest.TestCase):

    @parameterized.expand([("python", True), ("go", True), ("aaa", False)])
    def test_parse_html(self, topic_name, expected):
        self.assertEqual((len(parse_html(topic_name)) > 1), expected)
