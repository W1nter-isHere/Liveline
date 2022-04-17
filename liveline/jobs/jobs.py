from liveline.app import scheduler
from liveline.database import database

@scheduler.task('interval', id='close_rooms', seconds=61)
def job1():
    database.clean_rooms()