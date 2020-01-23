"""Helper test file"""

import unittest
from parameterized import parameterized
from utils.helpers import parse_html


class HelpersTestCase(unittest.TestCase):
    """Test case for topics helpers file"""

    @parameterized.expand([("python", True), ("go", True), ("aaa", False)])
    def test_parse_html(self, topic_name, expected):
        """
        :param topic_name: Name of the topic
        :param expected: Expected results
        :return: None
        """
        self.assertEqual((len(parse_html(topic_name)) > 1), expected)
