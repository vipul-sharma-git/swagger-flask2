import mock
import unittest
from asyncworker.tasks import Jobs


class TasksAllTestCase(unittest.TestCase):

    @mock.patch('asyncworker.tasks.Jobs.insert_id')
    def test_get_id_success(self, mock_insert):
        job_id = "12344abcc"
        mock_insert.return_value = job_id
        success, res = Jobs.get_id()
        self.assertEqual(success, True)
        self.assertEqual(res, job_id)
