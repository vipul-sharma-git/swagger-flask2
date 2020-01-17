# ALl the asynchronous jobs are mentioned over here
import asyncio
from topics.helpers import topic_operation


async def insert_topic_job(name: str, job_id: str) -> None:
    """
    Insert topic data
    :param name: Name of the topic
    :param job_id: Task id which will used to update task table
    :return: None
    """
    asyncio.create_task(topic_operation(name, job_id, "insert"))


async def update_topic_job(name: str, job_id: str) -> None:
    """
    update topic data
    :param name: Name of the topic
    :param job_id: Task id which will used to update task table
    :return: None
    """
    asyncio.create_task(topic_operation(name, job_id, "update"))
