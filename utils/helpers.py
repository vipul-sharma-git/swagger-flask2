""" Helpers funtions w.r.t topics module """
import asyncio
from urllib import request
from bs4 import BeautifulSoup
from utils.jobs import Jobs
from settings import db
import constants
from models.topics import Topics

_CATEGORIES_SELECTOR = "ul.toc.chapters li a"
_HTML_PARSER = "html.parser"
_TOPICS_URL = "https://www.tutorialspoint.com/{name}/index.htm"


def parse_html(name: str) -> str:
    """
    It request the topics url and parse as well as fetch categories details w.r.t topic name
    :param name: Name of the topic
    :return: list of the categories existing w.r.t topic name
    """
    html_contents = request.urlopen(_TOPICS_URL.format(name=name))
    soup = BeautifulSoup(html_contents.read(), _HTML_PARSER)
    categories_tags = soup.select(_CATEGORIES_SELECTOR)
    if categories_tags:
        categories_list = [categories.get_text() for categories in categories_tags]
        return ",".join(categories_list)
    return ""


async def topic_operation(name: str, job_id: str, job_type: str) -> None:
    """
    It fetches categories w.r.t topic name and perform
    insert/update w.r.t job_type after that update task id details
    :param name: Name of the topic
    :param job_id: task id which will be used to update the task data to database
    :param job_type: Type of operation i.e insert or update for topics data
    :return: None
    """
    task_dict = {
        constants.TASK_STATUS_KEY: constants.FAILED,
        constants.TASK_ERROR_KEY: "",
    }
    try:
        if job_type.lower().strip() == constants.INSERT.lower().strip():
            db.session.add(Topics(name=name, categories=parse_html(name)))
        elif job_type.lower().strip() == constants.UPDATE.lower().strip():
            topic_data = Topics.query.filter_by(name=name).first()
            topic_data.categories = parse_html(name)
        db.session.commit()
        task_dict[constants.TASK_STATUS_KEY] = constants.COMPLETED
    except (KeyError, AttributeError, ValueError) as err:
        task_dict[constants.TASK_ERROR_KEY] = str(err)
    finally:
        Jobs.update_id(job_id, task_dict)


async def topic_jobs(name: str, job_id: str, operation_type: str) -> None:
    """
    update topic data
    :param name: Name of the topic
    :param job_id: Task id which will used to update task table
    :param operation_type: Type of CRUD operation to DB
    :return: None
    """
    asyncio.create_task(topic_operation(name, job_id, operation_type))
