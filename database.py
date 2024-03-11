from sqlalchemy import create_engine, Table, Column, text, String, MetaData, Integer, Computed
import os

db_connection_string = "postgresql://fptdbqoy:G63T9sjGPWorNpmbpPGY91hXeCLBKe9-@bubble.db.elephantsql.com/fptdbqoy"
#db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(db_connection_string)

def load_all_xposts_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from xposts"))
        posts = []
        for row in result.all():
            posts.append(dict(row))
        return posts 

def load_yesterday_xposts_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from xposts where time > now() - interval '1 day'"))
        posts = []
        for row in result.all():
            posts.append(dict(row))
        return posts 

def load_within_week_xposts_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from xposts where time > now() - interval '1 week'"))
        posts = []
        for row in result.all():
            posts.append(dict(row))
        return posts                    
    
def load_within_month_xposts_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from xposts where time > now() - interval '1 month'"))
        posts = []
        for row in result.all():
            posts.append(dict(row))
        return posts

def load_within_year_xposts_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from xposts where time > now() - interval '1 year'"))
        posts = []
        for row in result.all():
            posts.append(dict(row))
        return posts

def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    jobs = []
    for row in result.all():
      jobs.append(dict(row))
    return jobs    

def load_job_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(
      text("SELECT * FROM jobs WHERE id = :val"),
      val=id
    )
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return dict(rows[0])


def add_application_to_db(job_id, data):
  with engine.connect() as conn:
    query = text("INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)")

    conn.execute(query, 
                 job_id=job_id, 
                 full_name=data['full_name'],
                 email=data['email'],
                 linkedin_url=data['linkedin_url'],
                 education=data['education'],
                 work_experience=data['work_experience'],
                 resume_url=data['resume_url'])        