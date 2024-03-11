from sqlalchemy import create_engine, Table, Column, text, String, MetaData, Integer, Computed

db_connection_string = "postgresql://fptdbqoy:G63T9sjGPWorNpmbpPGY91hXeCLBKe9-@bubble.db.elephantsql.com/fptdbqoy"

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

def load_within_lastweek_xposts_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from xposts where time > now() - interval '1 week'"))
        posts = []
        for row in result.all():
            posts.append(dict(row))
        return posts                    
    
def load_within_lastmonth_xposts_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from xposts where time > now() - interval '1 month'"))
        posts = []
        for row in result.all():
            posts.append(dict(row))
        return posts