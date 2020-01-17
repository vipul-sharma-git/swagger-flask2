from asyncworker.views import get_status
from extras.constants import ERROR, BAD_REQUEST
import mock
import unittest
import flask


class JobsAllTestCase(unittest.TestCase):

    @mock.patch('asyncworker.views.Jobs')
    def test_get_status_success(self, mock_job):
        job_id = "1234abcd"
        mock_job.status(job_id).return_value = "Completed"
        res = get_status(job_id)
        self.assertEqual(res.return_value, "Completed")

    @mock.patch('asyncworker.views.make_response')
    @mock.patch('asyncworker.views.Jobs')
    def test_get_status_job_id_error(self, mock_job, mock_response):
        job_id = "1234abcde"
        error = "error"
        mock_job.status = None
        mock_response.return_value = {"data": ERROR.format(error=str(error)), "status_code": BAD_REQUEST}
        res = get_status(job_id)
        app = flask.Flask(__name__)
        with app.test_request_context():
            rv = flask.make_response(ERROR.format(error=str(error)), BAD_REQUEST)
            self.assertEqual(res['data'], rv.data.decode("utf-8"))
            self.assertEqual(res['status_code'], rv.status_code)
