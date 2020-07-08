import os
from sqlalchemy import Column, String, Integer, create_engine, Date, Float
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date

DB_NAME = "CastingAgency"#os.getenv('DB_NAME')
DB_USER = "postgres"#os.getenv('DB_USER')
DB_HOST = "localhost:5432"#os.getenv('DB_HOST')
DB_PASSWORD = "root"#os.getenv('DB_PASSWORD')

database_path = 'postgres://{}:{}@{}/{}'.format(
  DB_USER,DB_PASSWORD,DB_HOST, DB_NAME)

db = SQLAlchemy()
#----------------------------------------------------------------------------#
# Database Setup 
#----------------------------------------------------------------------------#
def setup_db(app, database_uri=database_path):
    '''binds a flask application and a SQLAlchemy service'''
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_and_create_all():
    '''drops the database tables and starts fresh
    can be used to initialize a clean database
    '''
    db.drop_all()
    db.create_all()
    db_init_records()

def db_init_records():
    '''this will initialize the database with some test records.'''

    new_actor = (Actor(
        name = 'Jack',
        gender = 'Male',
        age = 25
        ))

    new_actor.insert()

    new_movie = (Movie(
        title = 'Jack first Movie',
        release_date = date.today()
        ))
    new_movie.insert()

    new_performance = Performance.insert().values(
        Movie_id = new_movie.id,
        Actor_id = new_actor.id,
        actor_fee = 500.00
    )
  
    db.session.execute(new_performance) 
    db.session.commit()

#----------------------------------------------------------------------------#
# Performance Junction Object M:M 
#----------------------------------------------------------------------------#

# Instead of creating a new Table, the documentation recommends to create a association table
Performance = db.Table(
    'Performance', 
    db.Model.metadata,
    db.Column('Movie_id', db.Integer, db.ForeignKey('movies.id'),nullable=False),
    db.Column('Actor_id', db.Integer, db.ForeignKey('actors.id'),nullable=False),
    db.Column('actor_fee', db.Float)
)

#----------------------------------------------------------------------------#
# Actors Model 
#----------------------------------------------------------------------------#

class Actor(db.Model):  
  __tablename__ = 'actors'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  gender = Column(String)
  age = Column(Integer)

  def __init__(self, name, gender, age):
    self.name = name
    self.gender = gender
    self.age = age

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name' : self.name,
      'gender': self.gender,
      'age': self.age
    }

#----------------------------------------------------------------------------#
# Movies Model 
#----------------------------------------------------------------------------#

class Movie(db.Model):  
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(Date)
  actors = db.relationship('Actor', secondary=Performance, backref=db.backref('performances', lazy='joined'))

  def __init__(self, title, release_date) :
    self.title = title
    self.release_date = release_date

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title' : self.title,
      'release_date': self.release_date
    }
