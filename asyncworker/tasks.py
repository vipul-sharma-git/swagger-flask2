import uuid
from asyncworker.models import Task
from config import db
from extras import constants


class Jobs:
    @classmethod
    def get_id(cls):
        """
        :return: True  if job id else error
        """
        try:
            return True, cls.insert_id()
        except Exception as e:
            return False, str(e)

    @staticmethod
    def insert_id():
        """
        Insert the job id to  tasks table
        :return: task id
        """
        task_id = uuid.uuid4().hex
        db.session.add(Task(task_id=task_id, task_status=constants.INPROGRESS, task_error=''))
        db.session.commit()
        return task_id

    @staticmethod
    def update_id(task_id, data):
        """
        Update tha data w.r.t task id
        :param task_id:  uniquer identifier for all the tasks
        :param data: data to update in tasks w.r.t task id
        :return: None
        """
        task_data = Task.query.filter_by(task_id=task_id).first()
        if not task_data:
            raise Exception
        task_data.task_status = data[constants.TASK_STATUS_KEY]
        task_data.task_error = data[constants.TASK_ERROR_KEY]
        db.session.commit()

    @staticmethod
    def status(task_id):
        """
        :param task_id: uniquer identifier for all the tasks
        :return: task status field details
        """
        task_data = Task.query.filter_by(task_id=task_id).first()
        return task_data.task_status if task_data else ''
