# -*- coding: utf-8 -*-

import celery
from drf_misc.core.api_exceptions import BadRequest

from .constants import TaskStatus
from .models import Task
from .services import TaskService
from .settings import logger

# pylint: disable=no-member,import-error,too-many-arguments


class TaskHandler(celery.Task):
    def run(self, *args, **kwargs):
        logger.info("Running: %s with args: %s, kwargs: %s", self.name, args, kwargs)

    def before_start(self, task_id, args, kwargs):
        logger.info("Before started: %s with args: %s, kwargs: %s", task_id, args, kwargs)
        if not kwargs.get("identifiers"):
            raise BadRequest({"message": "identifiers is required"})
        if not Task.objects.filter(id=task_id).exists():
            data = {
                "identifiers": kwargs.get("identifiers"),
                "id": task_id,
                "name": self.name,
                "status": TaskStatus.RUNNING,
                "args": self.request.args,
                "kwargs": self.request.kwargs,
                "retries": self.request.retries,
                "expires": self.request.expires,
                "root_id": self.request.root_id,
                "parent_id": self.request.parent_id,
            }
            TaskService().create(data=data)

    def on_success(self, retval, task_id, args, kwargs):
        logger.info("On Success: %s with args: %s, kwargs: %s", task_id, args, kwargs)
        TaskService(task_id).update(
            {
                "status": TaskStatus.SUCCESS,
                "return_value": retval,
            }
        )

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info("On Failure: %s with args: %s, kwargs: %s", task_id, args, kwargs)
        TaskService(task_id).update(
            {
                "status": TaskStatus.FAILED,
                "failed_reason": str(exc),
            }
        )

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger.info("On Retry: %s with args: %s, kwargs: %s", task_id, args, kwargs)
        task_instance = Task.objects.filter(id=task_id).first()
        TaskService(task_id).update(
            {
                "status": TaskStatus.RETRYING,
                "counter": task_instance.counter + 1,
            }
        )

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        logger.info("After return: %s with args: %s, kwargs: %s", task_id, args, kwargs)
