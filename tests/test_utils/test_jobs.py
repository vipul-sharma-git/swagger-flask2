"""Tasks tests """
import unittest
import mock
from utils.jobs import Jobs


class TasksAllTestCase(unittest.TestCase):
    """Tasks unit tests"""

    @mock.patch("utils.jobs.Jobs.insert_id")
    def test_get_id_success(self, mock_insert):
        """Get id success"""
        job_id = "12344abcc"
        mock_insert.return_value = job_id
        success, res = Jobs.get_id()
        self.assertEqual(success, True)
        self.assertEqual(res, job_id)
