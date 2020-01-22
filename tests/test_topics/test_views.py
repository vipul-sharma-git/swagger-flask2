"""Topics Views tests file"""
import unittest
import json
import mock
import flask

from topics.views import get_all, get_by_name, delete_by_name, update_by_name
from topics.views import _NAME_KEY, _CATEGORIES_KEY, _TOPIC_DELETED, _TOPIC_NAME_NA
import constants


class GetAllTestCase(unittest.TestCase):
    """Get all topics tests"""

    @mock.patch("topics.views.make_response")
    @mock.patch("topics.views.Topics")
    def test_get_all_success(self, mock_obj, mock_response):
        """Get all topics success"""
        data = {}
        mock_response.return_value = {
            "data": dict(),
            "status_code": constants.SUCCESS_CODE,
        }
        res = get_all()
        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(data, constants.SUCCESS_CODE)
            self.assertEqual(str(res["data"]), flask_res.data.decode("utf-8").strip())
            self.assertEqual(res["status_code"], flask_res.status_code)

    @mock.patch("topics.views.make_response")
    @mock.patch("topics.views.Topics")
    def test_get_all_error(self, mock_obj, mock_response):
        """Get all topics with error"""
        error = "Error"
        mock_obj.query.all = None
        bad_request = 400
        mock_response.return_value = {
            "data": constants.ERROR.format(error=error),
            "status_code": bad_request,
        }
        res = get_all()
        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(
                constants.ERROR.format(error=str(error)), 400
            )
            self.assertEqual(res["data"], flask_res.data.decode("utf-8"))
            self.assertEqual(res["status_code"], flask_res.status_code)


class GetByNameTestCase(unittest.TestCase):
    """Get topic by name test cases"""

    @mock.patch("topics.views.make_response")
    @mock.patch("topics.views.Topics")
    def test_get_by_name_exists_success(self, mock_obj, mock_response):
        """Get topic name exists in DB"""
        name = "python"
        mock_obj.query.filter_by(name=name).first().name = name
        mock_obj.query.filter_by(name=name).first().categories = "cat1,cat2"
        data = {_NAME_KEY: name, _CATEGORIES_KEY: ["cat1", "cat2"]}
        mock_response.return_value = {
            "data": data,
            "status_code": constants.SUCCESS_CODE,
        }
        res = get_by_name(name)
        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(data, constants.SUCCESS_CODE)
            assert res["data"] == json.loads(flask_res.data.decode("utf-8"))
            # self.assertEqual(res["data"], json.loads(flask_res.data.decode("utf-8")))
            self.assertEqual(res["status_code"], flask_res.status_code)

    @mock.patch("topics.views.make_response")
    @mock.patch("topics.views.asyncio")
    @mock.patch("topics.views.Jobs")
    @mock.patch("topics.views.Topics")
    def test_get_by_name_not_exists_get_job_id_success(
        self, mock_obj, mock_job, mock_async, mock_response
    ):
        """Get topic by name does not exists in DB"""
        name = "data"
        job_id = "123456abcd"
        success_code = 200
        mock_obj.query.filter_by(name=name).first.return_value = None
        mock_response.return_value = {"data": job_id, "status_code": success_code}
        mock_job.get_id.return_value = True, job_id
        mock_async.run.return_value = None
        res = get_by_name(name)
        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(job_id, success_code)
            self.assertEqual(res["data"], flask_res.data.decode("utf-8"))
            self.assertEqual(res["status_code"], flask_res.status_code)

    @mock.patch("topics.views.make_response")
    @mock.patch("topics.views.Jobs")
    @mock.patch("topics.views.Topics")
    def test_get_by_name_not_exists_get_job_id_fails(
        self, mock_obj, mock_job, mock_response
    ):
        """Get exists error while returning job id"""
        name = "data"
        job_error = "Job Error"
        bad_request = 400

        mock_obj.query.filter_by(name=name).first.return_value = None
        mock_job.get_id.return_value = False, job_error
        mock_response.return_value = {
            "data": constants.ERROR.format(error=job_error),
            "status_code": bad_request,
        }
        res = get_by_name(name)

        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(
                constants.ERROR.format(error=job_error), 400
            )
            self.assertEqual(res["data"], flask_res.data.decode("utf-8"))
            self.assertEqual(res["status_code"], flask_res.status_code)

    @mock.patch("topics.views.make_response")
    @mock.patch("topics.views.Topics")
    def test_get_by_name_exception(self, mock_obj, mock_response):
        """Get topic name got exception"""
        name = "data"
        error = "None type object not callable"
        bad_request = 400
        mock_obj.query.filter_by(name=name).first = None
        mock_response.return_value = {
            "data": constants.ERROR.format(error=error),
            "status_code": bad_request,
        }
        res = get_by_name(name)

        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(
                constants.ERROR.format(error=str(error)), 400
            )
            self.assertEqual(res["data"], flask_res.data.decode("utf-8"))
            self.assertEqual(res["status_code"], flask_res.status_code)


class DeleteByNameTestCase(unittest.TestCase):
    """"Delete by name test cases"""

    @mock.patch("topics.views.make_response")
    @mock.patch("topics.views.db")
    @mock.patch("topics.views.Topics")
    def test_delete_by_topic_name_success(self, mock_obj, mock_db, mock_response):
        """Delete by name success"""
        name = "python"
        success_code = 200
        mock_response.return_value = {
            "data": _TOPIC_DELETED.format(name=name),
            "status_code": success_code,
        }
        app = flask.Flask(__name__)
        res = delete_by_name(name)
        with app.test_request_context():
            flask_res = flask.make_response(
                _TOPIC_DELETED.format(name=name), success_code
            )
            self.assertEqual(res["data"], flask_res.data.decode("utf-8"))
            self.assertEqual(res["status_code"], flask_res.status_code)

    @mock.patch("topics.views.make_response")
    @mock.patch("topics.views.Topics")
    def test_delete_by_topic_name_not_available(self, mock_obj, mock_response):
        """Delete by topic name NA"""
        name = "data"
        not_found_status_code = 404
        mock_obj.query.filter_by(name=name).first.return_value = None
        mock_response.return_value = {
            "data": _TOPIC_NAME_NA.format(name=name),
            "status_code": not_found_status_code,
        }
        app = flask.Flask(__name__)
        res = delete_by_name(name)
        with app.test_request_context():
            flask_res = flask.make_response(
                _TOPIC_NAME_NA.format(name=name), not_found_status_code
            )
            self.assertEqual(res["data"], flask_res.data.decode("utf-8"))
            self.assertEqual(res["status_code"], flask_res.status_code)

    @mock.patch("topics.views.make_response")
    @mock.patch("topics.views.Topics")
    def test_delete_by_topic_name_error(self, mock_obj, mock_response):
        """While deleting got the error"""
        name = "data"
        error = "None type object not callable"
        bad_request = 400
        mock_response.return_value = {
            "data": constants.ERROR.format(error=error),
            "status_code": bad_request,
        }
        mock_obj.query.filter_by(name=name).first = None
        res = delete_by_name(name)
        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(
                constants.ERROR.format(error=str(error)), bad_request
            )
            self.assertEqual(res["data"], flask_res.data.decode("utf-8"))
            self.assertEqual(res["status_code"], flask_res.status_code)


class UpdateByNameTestCase(unittest.TestCase):
    """Update by name test cases"""

    @mock.patch("topics.views.make_response")
    @mock.patch("topics.views.asyncio")
    @mock.patch("topics.views.Jobs")
    @mock.patch("topics.views.Topics")
    def test_update_by_name_success(
        self, mock_obj, mock_job, mock_async, mock_response
    ):
        """update by name success"""
        name = "python"
        job_id = "123456abcd"
        success_code = 200
        mock_job.get_id.return_value = True, job_id
        mock_async.run.return_value = None
        mock_response.return_value = {"data": job_id, "status_code": success_code}
        res = update_by_name(name)
        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(job_id, success_code)
            self.assertEqual(res["data"], flask_res.data.decode("utf-8"))
            self.assertEqual(res["status_code"], flask_res.status_code)

    @mock.patch("topics.views.make_response")
    @mock.patch("topics.views.Topics")
    def test_update_by_name_not_found_success(self, mock_obj, mock_response):
        """Update by topic name NA"""
        name = "data"
        not_found_status_code = 404
        mock_obj.query.filter_by(name=name).first.return_value = None
        mock_response.return_value = {
            "data": _TOPIC_NAME_NA.format(name=name),
            "status_code": not_found_status_code,
        }
        app = flask.Flask(__name__)
        res = update_by_name(name)
        with app.test_request_context():
            flask_res = flask.make_response(
                _TOPIC_NAME_NA.format(name=name), not_found_status_code
            )
            self.assertEqual(res["data"], flask_res.data.decode("utf-8"))
            self.assertEqual(res["status_code"], flask_res.status_code)

    @mock.patch("topics.views.make_response")
    @mock.patch("topics.views.Jobs")
    @mock.patch("topics.views.Topics")
    def test_update_by_name_get_job_id_fails(self, mock_obj, mock_job, mock_response):
        """Update by topic name error while returning task id"""
        name = "data"
        bad_request = 400
        job_error = "Job Error"
        mock_job.get_id.return_value = False, job_error
        mock_response.return_value = {
            "data": constants.ERROR.format(error=job_error),
            "status_code": bad_request,
        }
        res = update_by_name(name)
        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(
                constants.ERROR.format(error=job_error), bad_request
            )
            self.assertEqual(res["data"], flask_res.data.decode("utf-8"))
            self.assertEqual(res["status_code"], flask_res.status_code)

    @mock.patch("topics.views.make_response")
    @mock.patch("topics.views.Topics")
    def test_update_by_name_exception(self, mock_obj, mock_response):
        """Update by name exception"""
        name = "data"
        bad_request = 400
        error = "None type object not callable"
        mock_obj.query.filter_by(name=name).first = None
        mock_response.return_value = {
            "data": constants.ERROR.format(error=error),
            "status_code": bad_request,
        }
        res = update_by_name(name)
        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(
                constants.ERROR.format(error=error), bad_request
            )
            self.assertEqual(res["data"], flask_res.data.decode("utf-8"))
            self.assertEqual(res["status_code"], flask_res.status_code)
