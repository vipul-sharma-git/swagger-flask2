"""Asyncworker apis views"""

from flask import make_response
from utils.jobs import Jobs
import constants


def get_status(task_id):
    """
    :param task_id: task id
    :return: job details w.r.t task id
    """
    response_code, data = constants.BAD_REQUEST, ""
    try:
        job_status = Jobs.status(task_id)
        if job_status:
            data = job_status
            response_code = constants.SUCCESS_CODE
        else:
            data = constants.INVALID_TASK_ID.format(id=task_id)
            response_code = constants.NOT_FOUND
    except (KeyError, AttributeError) as err:
        data = constants.ERROR.format(error=str(err))
    finally:
        return make_response(data, response_code)
