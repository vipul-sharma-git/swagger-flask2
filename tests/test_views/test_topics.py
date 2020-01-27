"""Topics Views tests file"""
import unittest
import json
import mock
import flask

from views.topics import get_all, get_by_name, delete_by_name, update_by_name
from views.topics import _NAME_KEY, _CATEGORIES_KEY, _TOPIC_DELETED, _TOPIC_NAME_NA
import constants

STATUS_CODE_KEY = "status_code"
DATA_KEY = "data"


class GetAllTestCase(unittest.TestCase):
    """Get all topics tests"""

    @mock.patch("views.topics.make_response")
    @mock.patch("views.topics.Categories")
    @mock.patch("views.topics.Topics")
    def test_get_all_success(self, mock_topic, mock_categories, mock_response):
        """Get all topics success"""
        mock_data = {}
        mock_response.return_value = {
            DATA_KEY: dict(),
            STATUS_CODE_KEY: constants.SUCCESS_CODE,
        }
        res = get_all()
        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(mock_data, constants.SUCCESS_CODE)
            self.assertEqual(str(res[DATA_KEY]), flask_res.data.decode("utf-8").strip())
            self.assertEqual(res[STATUS_CODE_KEY], flask_res.status_code)

    @mock.patch("views.topics.make_response")
    @mock.patch("views.topics.Categories")
    @mock.patch("views.topics.Topics")
    def test_get_all_no_data(self, mock_topic, mock_categories, mock_response):
        """Get all topics success"""
        mock_data = {}
        mock_topic.query.all.return_value = None
        mock_categories.query.all.return_value = None
        mock_response.return_value = {
            DATA_KEY: dict(),
            STATUS_CODE_KEY: constants.SUCCESS_CODE,
        }
        res = get_all()
        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(mock_data, constants.SUCCESS_CODE)
            self.assertEqual(str(res[DATA_KEY]), flask_res.data.decode("utf-8").strip())
            self.assertEqual(res[STATUS_CODE_KEY], flask_res.status_code)

    @mock.patch("views.topics.make_response")
    @mock.patch("views.topics.Topics")
    def test_get_all_error(self, mock_obj, mock_response):
        """Get all topics with error"""
        error = "Error"
        mock_obj.query.all = None
        mock_response.return_value = {
            DATA_KEY: constants.ERROR.format(error=error),
            STATUS_CODE_KEY: constants.BAD_REQUEST,
        }
        res = get_all()
        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(
                constants.ERROR.format(error=str(error)), constants.BAD_REQUEST
            )
            self.assertEqual(res[DATA_KEY], flask_res.data.decode("utf-8"))
            self.assertEqual(res[STATUS_CODE_KEY], flask_res.status_code)


class GetByNameTestCase(unittest.TestCase):
    """Get topic by name test cases"""

    @mock.patch("views.topics.make_response")
    @mock.patch("views.topics.Categories")
    @mock.patch("views.topics.Topics")
    def test_get_by_name_exists_success(self, mock_obj, mock_categories, mock_response):
        """Get topic name exists in DB"""
        name = "python"
        mock_id = "1"
        mock_obj.query.filter_by(name=name).first().id = mock_id
        mock_categories.query.filter_by(topic_name=mock_id).return_value = [
            {_NAME_KEY: "cat1"},
            {_NAME_KEY: "cat2"},
        ]
        data = {_NAME_KEY: name, _CATEGORIES_KEY: ["cat1", "cat2"]}
        mock_response.return_value = {
            DATA_KEY: data,
            STATUS_CODE_KEY: constants.SUCCESS_CODE,
        }
        res = get_by_name(name)
        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(data, constants.SUCCESS_CODE)
            assert res[DATA_KEY] == json.loads(flask_res.data.decode("utf-8"))
            self.assertEqual(res[STATUS_CODE_KEY], flask_res.status_code)

    @mock.patch("views.topics.make_response")
    @mock.patch("views.topics.asyncio")
    @mock.patch("views.topics.Jobs")
    @mock.patch("views.topics.Topics")
    def test_get_by_name_not_exists_get_job_id_success(
            self, mock_obj, mock_job, mock_async, mock_response):
        """Get topic by name does not exists in DB"""
        name = "abcd"
        job_id = "123456abcd"
        mock_obj.query.filter_by(name=name).first.return_value = None
        mock_response.return_value = {
            DATA_KEY: job_id,
            STATUS_CODE_KEY: constants.ACCEPTED_CODE,
        }
        mock_job.get_id.return_value = True, job_id
        mock_async.run.return_value = None
        res = get_by_name(name)
        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(job_id, constants.ACCEPTED_CODE)
            self.assertEqual(res[DATA_KEY], flask_res.data.decode("utf-8"))
            self.assertEqual(res[STATUS_CODE_KEY], flask_res.status_code)

    @mock.patch("views.topics.make_response")
    @mock.patch("views.topics.Jobs")
    @mock.patch("views.topics.Topics")
    def test_get_by_name_not_exists_get_job_id_fails(
            self, mock_obj, mock_job, mock_response):
        """Get exists error while returning job id"""
        name = "abcd"
        job_error = "Job Error"
        mock_obj.query.filter_by(name=name).first.return_value = None
        mock_job.get_id.return_value = False, job_error
        mock_response.return_value = {
            DATA_KEY: constants.ERROR.format(error=job_error),
            STATUS_CODE_KEY: constants.BAD_REQUEST,
        }
        res = get_by_name(name)

        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(
                constants.ERROR.format(error=job_error), constants.BAD_REQUEST
            )
            self.assertEqual(res[DATA_KEY], flask_res.data.decode("utf-8"))
            self.assertEqual(res[STATUS_CODE_KEY], flask_res.status_code)

    @mock.patch("views.topics.make_response")
    @mock.patch("views.topics.Topics")
    def test_get_by_name_exception(self, mock_obj, mock_response):
        """Get topic name got exception"""
        name = "abcd"
        error = "None type object not callable"
        mock_obj.query.filter_by(name=name).first = None
        mock_response.return_value = {
            DATA_KEY: constants.ERROR.format(error=error),
            STATUS_CODE_KEY: constants.BAD_REQUEST,
        }
        res = get_by_name(name)

        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(
                constants.ERROR.format(error=str(error)), constants.BAD_REQUEST
            )
            self.assertEqual(res[DATA_KEY], flask_res.data.decode("utf-8"))
            self.assertEqual(res[STATUS_CODE_KEY], flask_res.status_code)


class DeleteByNameTestCase(unittest.TestCase):
    """"Delete by name test cases"""

    @mock.patch("views.topics.make_response")
    @mock.patch("views.topics.db")
    @mock.patch("views.topics.Topics")
    def test_delete_by_topic_name_success(self, mock_obj, mock_db, mock_response):
        """Delete by name success"""
        name = "python"
        mock_response.return_value = {
            DATA_KEY: _TOPIC_DELETED.format(name=name),
            STATUS_CODE_KEY: constants.NO_CONTENT_CODE,
        }
        app = flask.Flask(__name__)
        res = delete_by_name(name)
        with app.test_request_context():
            flask_res = flask.make_response(
                _TOPIC_DELETED.format(name=name), constants.NO_CONTENT_CODE
            )
            self.assertEqual(res[DATA_KEY], flask_res.data.decode("utf-8"))
            self.assertEqual(res[STATUS_CODE_KEY], flask_res.status_code)

    @mock.patch("views.topics.make_response")
    @mock.patch("views.topics.Topics")
    def test_delete_by_topic_name_not_available(self, mock_obj, mock_response):
        """Delete by topic name NA"""
        name = "python"
        mock_obj.query.filter_by(name=name).first.return_value = None
        mock_response.return_value = {
            DATA_KEY: _TOPIC_NAME_NA.format(name=name),
            STATUS_CODE_KEY: constants.NOT_FOUND,
        }
        app = flask.Flask(__name__)
        res = delete_by_name(name)
        with app.test_request_context():
            flask_res = flask.make_response(
                _TOPIC_NAME_NA.format(name=name), constants.NOT_FOUND
            )
            self.assertEqual(res[DATA_KEY], flask_res.data.decode("utf-8"))
            self.assertEqual(res[STATUS_CODE_KEY], flask_res.status_code)

    @mock.patch("views.topics.make_response")
    @mock.patch("views.topics.Topics")
    def test_delete_by_topic_name_error(self, mock_obj, mock_response):
        """While deleting got the error"""
        name = "abcd"
        error = "None type object not callable"
        mock_response.return_value = {
            DATA_KEY: constants.ERROR.format(error=error),
            STATUS_CODE_KEY: constants.BAD_REQUEST,
        }
        mock_obj.query.filter_by(name=name).first = None
        res = delete_by_name(name)
        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(
                constants.ERROR.format(error=str(error)), constants.BAD_REQUEST
            )
            self.assertEqual(res[DATA_KEY], flask_res.data.decode("utf-8"))
            self.assertEqual(res[STATUS_CODE_KEY], flask_res.status_code)


class UpdateByNameTestCase(unittest.TestCase):
    """Update by name test cases"""

    @mock.patch("views.topics.make_response")
    @mock.patch("views.topics.asyncio")
    @mock.patch("views.topics.Jobs")
    @mock.patch("views.topics.Topics")
    def test_update_by_name_success(
            self, mock_obj, mock_job, mock_async, mock_response):
        """update by name success"""
        name = "python"
        job_id = "123456abcd"
        mock_job.get_id.return_value = True, job_id
        mock_async.run.return_value = None
        mock_response.return_value = {
            DATA_KEY: job_id,
            STATUS_CODE_KEY: constants.ACCEPTED_CODE,
        }
        res = update_by_name(name)
        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(job_id, constants.ACCEPTED_CODE)
            self.assertEqual(res[DATA_KEY], flask_res.data.decode("utf-8"))
            self.assertEqual(res[STATUS_CODE_KEY], flask_res.status_code)

    @mock.patch("views.topics.make_response")
    @mock.patch("views.topics.Topics")
    def test_update_by_name_not_found_success(self, mock_obj, mock_response):
        """Update by topic name NA"""
        name = "abcd"
        mock_obj.query.filter_by(name=name).first.return_value = None
        mock_response.return_value = {
            DATA_KEY: _TOPIC_NAME_NA.format(name=name),
            STATUS_CODE_KEY: constants.NOT_FOUND,
        }
        app = flask.Flask(__name__)
        res = update_by_name(name)
        with app.test_request_context():
            flask_res = flask.make_response(
                _TOPIC_NAME_NA.format(name=name), constants.NOT_FOUND
            )
            self.assertEqual(res[DATA_KEY], flask_res.data.decode("utf-8"))
            self.assertEqual(res[STATUS_CODE_KEY], flask_res.status_code)

    @mock.patch("views.topics.make_response")
    @mock.patch("views.topics.Jobs")
    @mock.patch("views.topics.Topics")
    def test_update_by_name_get_job_id_fails(self, mock_obj, mock_job, mock_response):
        """Update by topic name error while returning task id"""
        name = "abcd"
        job_error = "Job Error"
        mock_job.get_id.return_value = False, job_error
        mock_response.return_value = {
            DATA_KEY: constants.ERROR.format(error=job_error),
            STATUS_CODE_KEY: constants.BAD_REQUEST,
        }
        res = update_by_name(name)
        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(
                constants.ERROR.format(error=job_error), constants.BAD_REQUEST
            )
            self.assertEqual(res[DATA_KEY], flask_res.data.decode("utf-8"))
            self.assertEqual(res[STATUS_CODE_KEY], flask_res.status_code)

    @mock.patch("views.topics.make_response")
    @mock.patch("views.topics.Topics")
    def test_update_by_name_exception(self, mock_obj, mock_response):
        """Update by name exception"""
        name = "abcd"
        error = "None type object not callable"
        mock_obj.query.filter_by(name=name).first = None
        mock_response.return_value = {
            DATA_KEY: constants.ERROR.format(error=error),
            STATUS_CODE_KEY: constants.BAD_REQUEST,
        }
        res = update_by_name(name)
        app = flask.Flask(__name__)
        with app.test_request_context():
            flask_res = flask.make_response(
                constants.ERROR.format(error=error), constants.BAD_REQUEST
            )
            self.assertEqual(res[DATA_KEY], flask_res.data.decode("utf-8"))
            self.assertEqual(res[STATUS_CODE_KEY], flask_res.status_code)
