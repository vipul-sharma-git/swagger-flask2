from asyncworker.tasks import Jobs
from flask import make_response
from extras import constants


def get_status(id):
   """
   :param id: task id
   :return: job details w.r.t task id
   """
   try:
      job_status = Jobs.status(id)
      return job_status if job_status else make_response(constants.INVALID_TASK_ID.format(id=id), constants.NOT_FOUND)
   except Exception as e:
      return make_response(constants.ERROR.format(error=str(e)), constants.BAD_REQUEST)
