# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

employee_meetings = db.Table(
    "employee_meetings",
    metadata,
    db.Column("employee_id",db.Integer, db.ForeignKey("employees.id"),primary_key=True),
    db.Column("meeting_id",db.Integer,db.ForeignKey("meetings.id"),primary_key=True)

)


class Assignment(db.Model):
    ___tablename__ = "assignments"
    id = db.Column(db.Integer, primary_key = True)
    role = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    employee_id = db.Column(db.Integer,db.ForeignKey("employees.id"))
    project_id = db.Column(db.Integer,db.ForeignKey("projects.id"))

    employee = db.relationship("Employee", back_populates = "assignments")
    project = db.relationship("Project",back_populates = "assignments")

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    hire_date = db.Column(db.Date)
    meetings = db.relationship("Meeting",secondary="employee_meetings",back_populates = "employees")
    assignments = db.relationship("Assignment", back_populates = "employee", cascade = "all, delete-orphan")
    projects = association_proxy("assignments","project",creator=lambda proj_obj:Assignment(project = proj_obj))


    def __repr__(self):
        return f'<Employee {self.id}, {self.name}, {self.hire_date}>'


class Meeting(db.Model):
    __tablename__ = 'meetings'

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    scheduled_time = db.Column(db.DateTime)
    location = db.Column(db.String)
    employees = db.relationship("Employee",secondary="employee_meetings",back_populates = "meetings")

    def __repr__(self):
        return f'<Meeting {self.id}, {self.topic}, {self.scheduled_time}, {self.location}>'


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    budget = db.Column(db.Integer)
    assignments = db.relationship("Assignment", back_populates = "project", cascade = "all, delete-orphan")
    employees = association_proxy("assignments","employee",creator=lambda emp_obj:Assignment(employee = emp_obj))

    def __repr__(self):
        return f'<Review {self.id}, {self.title}, {self.budget}>'
