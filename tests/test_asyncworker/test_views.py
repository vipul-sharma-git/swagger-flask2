"""asyncwoker views tests"""
import unittest
import mock
import flask
from asyncworker.views import get_status
from constants import ERROR, BAD_REQUEST, SUCCESS_CODE, COMPLETED


class JobsAllTestCase(unittest.TestCase):
    """All jobs unit tests"""

    @mock.patch("asyncworker.views.make_response")
    @mock.patch("asyncworker.views.Jobs")
    def test_get_status_success(self, mock_job, mock_response):
        """Get status success"""
        job_id = "1234abcd"
        mock_response.return_value = {
            "data": COMPLETED,
            "status_code": SUCCESS_CODE,
        }
        mock_job.status(job_id).return_value = COMPLETED
        res = get_status(job_id)
        # self.assertEqual(res.return_value, "Completed")
        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(COMPLETED, SUCCESS_CODE)
            self.assertEqual(res["data"], flask_res.data.decode("utf-8"))
            self.assertEqual(res["status_code"], flask_res.status_code)

    @mock.patch("asyncworker.views.make_response")
    @mock.patch("asyncworker.views.Jobs")
    def test_get_status_job_id_error(self, mock_job, mock_response):
        """Get status error"""
        job_id = "1234abcde"
        error = "error"
        mock_job.status = None
        mock_response.return_value = {
            "data": ERROR.format(error=str(error)),
            "status_code": BAD_REQUEST,
        }
        res = get_status(job_id)
        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(ERROR.format(error=str(error)), BAD_REQUEST)
            self.assertEqual(res["data"], flask_res.data.decode("utf-8"))
            self.assertEqual(res["status_code"], flask_res.status_code)
