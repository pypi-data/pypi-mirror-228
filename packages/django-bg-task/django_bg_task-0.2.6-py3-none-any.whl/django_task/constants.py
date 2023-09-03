# -*- coding: utf-8 -*-

# pylint: disable=too-few-public-methods


class TaskStatus:
    SUCCESS = "success"
    PENDING = "pending"
    RUNNING = "running"
    FAILED = "failed"
    RETRYING = "retrying"

    choices = (
        (PENDING, "Pending"),
        (RUNNING, "Running"),
        (SUCCESS, "Success"),
        (FAILED, "Failed"),
        (RETRYING, "Retrying"),
    )
