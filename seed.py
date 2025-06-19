from datetime import datetime
from dotenv import load_dotenv
from app import create_app, db
from app.models.task import Task

load_dotenv()

my_app = create_app()
with my_app.app_context():
    db.drop_all()
    db.create_all()
    task1 = Task(
        id=1,
        title='Mow the lawn',
        description='Use the gas-powered mower',
        completed_at=None  # Incomplete
    )

    task2 = Task(
        id=2,
        title='Cook Pasta',
        description='Use the stovetop',
        completed_at=datetime.now()
    )

    db.session.add_all([task1, task2])
    db.session.commit()