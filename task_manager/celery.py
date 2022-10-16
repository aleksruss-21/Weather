from celery import Celery  # type: ignore


app = Celery("task_manager", include=["task_manager.tasks"])
app.config_from_object("task_manager.celeryconfig")


app.conf.beat_schedule = {
    "get_icao ": {"task": "task_manager.tasks.get_icao", "schedule": 604800.0},  # one week in seconds
    "get_weather_data": {
        "task": "task_manager.tasks.get_weather_data",
        "schedule": 1800.0,  # 30 minutes in seconds 1800
    },
}
