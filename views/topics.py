"""Topics views"""
import asyncio
from flask import make_response

import constants
from utils.jobs import Jobs
from utils.helpers import topic_jobs
from settings import db
from models.topics import Topics, Categories


_NAME_KEY = "name"
_CATEGORIES_KEY = "categories"
_DATA_KEY = "data"
_TOPIC_NAME_NA = "Topic {name} not found."
_TOPIC_DELETED = "Topic {name} deleted."


def get_all() -> make_response or list:
    """
    :return: List of all the topics with categories
    """
    response_code, data = constants.BAD_REQUEST, ""
    try:
        topics_data = Topics.query.all()
        categories_data = Categories.query.all()
        if categories_data and topics_data:
            topic_dict = {data.id: data.name for data in topics_data}
            topics_with_categories = {}
            for cat in categories_data:
                topics_with_categories.setdefault(
                    topic_dict[cat.topic_name], []
                ).append(cat.name)
            data = {_DATA_KEY: topics_with_categories if topics_with_categories else {}}
        else:
            data = {_DATA_KEY: {}}
        response_code = constants.SUCCESS_CODE
    except Exception as err:
        data = constants.ERROR.format(error=str(err))
    finally:
        return make_response(data, response_code)


def get_by_name(name: str) -> str or dict or make_response:
    """
    If topic name is present it will return those
    details else will insert topic in DB asynchronosuly
    :param name: Name of the topic
    :return: Data if topic name is present in DB else task id
    """
    response_code, data = constants.BAD_REQUEST, ""
    try:
        topic_exists = Topics.query.filter_by(name=name).first()
        if topic_exists:
            categories_data = Categories.query.filter_by(topic_name=topic_exists.id)
            data = (
                {
                    _NAME_KEY: name,
                    _CATEGORIES_KEY: [cat.name for cat in categories_data],
                }
                if list(categories_data)
                else {}
            )
            response_code = constants.SUCCESS_CODE
        else:
            success, job_id = Jobs.get_id()
            if success:
                asyncio.run(topic_jobs(name, job_id, constants.INSERT))
                response_code = constants.ACCEPTED_CODE
                data = job_id
            else:
                data = constants.ERROR.format(error=str(job_id))
    except Exception as err:
        data = constants.ERROR.format(error=str(err))
    finally:
        return make_response(data, response_code)


def delete_by_name(name: str) -> make_response:
    """
    Delete the topic name
    :param name:  topic name
    :return: status of the deleted topic name
    """
    response_code, data = constants.BAD_REQUEST, ""
    try:
        topic_data = Topics.query.filter_by(name=name).first()
        if topic_data:
            db.session.delete(topic_data)
            db.session.commit()
            data = _TOPIC_DELETED.format(name=name)
            response_code = constants.NO_CONTENT_CODE
        else:
            data = _TOPIC_NAME_NA.format(name=name)
            response_code = constants.NOT_FOUND
    except Exception as err:
        data = constants.ERROR.format(error=str(err))
    finally:
        return make_response(data, response_code)


def update_by_name(name: str) -> make_response:
    """
    update the topic name asynchronously
    :param name: topic name
    :return: task id
    """
    response_code, data = constants.BAD_REQUEST, ""
    try:
        topic_data = Topics.query.filter_by(name=name).first()
        if topic_data:
            success, job_id = Jobs.get_id()
            if success:
                asyncio.run(topic_jobs(name, job_id, constants.UPDATE))
                data = job_id
                response_code = constants.ACCEPTED_CODE
            else:
                data = constants.ERROR.format(error=str(job_id))
        else:
            data = _TOPIC_NAME_NA.format(name=name)
            response_code = constants.NOT_FOUND
    except Exception as err:
        data = constants.ERROR.format(error=str(err))
    finally:
        return make_response(data, response_code)
