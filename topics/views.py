import asyncio

from asyncworker.tasks import Jobs
from config import db
from extras import constants
from flask import make_response
from topics.models import Topics
from topics.jobs import insert_topic_job, update_topic_job


_NAME_KEY = "name"
_CATEGORIES_KEY = "categories"
_TOPIC_NAME_NA = "Topic {name} not found."
_TOPIC_DELETED = "Topic {name} deleted."


def get_all() -> make_response or list:
   """
   :return: List of all the topics with categories
   """
   try:
      topics_data = Topics.query.all()
      return [
         {_NAME_KEY: data.name, _CATEGORIES_KEY: data.categories.split(",")} for data in topics_data
      ] if topics_data else []
   except Exception as e:
      return make_response(constants.ERROR.format(error=str(e)), str(e))


def get_by_name(name: str) -> str or dict or make_response:
   """
   If topic name is present it will return those details else will insert topic in DB asynchronosuly
   :param name: Name of the topic
   :return: Data if topic name is present in DB else task id
   """
   try:
      topic_data = Topics.query.filter_by(name=name).first()
      if topic_data:
         return {
            _NAME_KEY: topic_data.name,
            _CATEGORIES_KEY: topic_data.categories.split(",")
         }
      else:
         success, job_id = Jobs.get_id()
         if success:
            asyncio.run(insert_topic_job(name, job_id))
            return make_response(job_id, constants.SUCCESS_CODE)
         return make_response(constants.ERROR.format(error=str(job_id)), constants.BAD_REQUEST)
   except Exception as e:
      return make_response(constants.ERROR.format(error=str(e)), constants.BAD_REQUEST)


def delete_by_name(name: str) -> make_response:
   """
   Delete the topic name
   :param name:  topic name
   :return: status of the deleted topic name
   """
   try:
      topic_data = Topics.query.filter_by(name=name).first()
      if topic_data:
         db.session.delete(topic_data)
         db.session.commit()
         return make_response(_TOPIC_DELETED.format(name=name), constants.SUCCESS_CODE)
      return make_response(_TOPIC_NAME_NA.format(name=name), constants.NOT_FOUND)
   except Exception as e:
      return make_response(constants.ERROR.format(error=str(e)), constants.BAD_REQUEST)


def update_by_name(name: str) -> make_response:
   """
   update the topic name asynchronously
   :param name: topic name
   :return: task id
   """
   try:
      topic_data = Topics.query.filter_by(name=name).first()
      if topic_data:
         success, job_id = Jobs.get_id()
         if success:
            asyncio.run(update_topic_job(name, job_id))
            return make_response(job_id, constants.SUCCESS_CODE)
         return make_response(constants.ERROR.format(error=str(job_id)), constants.BAD_REQUEST)
      return make_response(_TOPIC_NAME_NA.format(name=name), constants.NOT_FOUND)
   except Exception as e:
      return make_response(constants.ERROR.format(error=str(e)), constants.BAD_REQUEST)
