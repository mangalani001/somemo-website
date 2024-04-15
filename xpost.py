from sqlalchemy import create_engine, Table, Column, text, String, MetaData, Integer, Computed
from database import engine


def load_xposts_users_interval_from_db(_field, _interval):
    with engine.connect() as conn:
        result = conn.execute(text("select distinct "+_field+" from xpost where xpost_day > now() - interval '"+_interval+"'"))
        tags = []
        for row in result.all():
            tags.append(row[0])            
            #tags.append(row['tag'])
        return tags

    
def load_xposts_data_interval_from_db(_tag, _field, _interval):
    with engine.connect() as conn:
        result = conn.execute(text("select "+_field+" from xpost WHERE xpost_day > now() - interval '"+_interval+"' AND tag = :val"), {'val':_tag})
       # result = conn.execute(text("select sum(likes_count) from xpost WHERE tag  = :val AND xpost_date > now() - interval '1 week'"), val=tagg)
        likes = 0
        for row in result.all():
            likes += row[0]    
        return likes
        #if result is not None:
        #    return result.
        #return 0         
    
def load_xposts_users_onemonth_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM xposts where xpost_day from xpost where xpost_date > now() - interval '1 month'"))
        posts = []
        for row in result.all():
            #posts.append(row['xpost_day'])
            posts.append(dict(row))
        return sorted(posts)     
    
def load_xposts_users_between_dates_from_db(startdate,enddate):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DISTINCT xpost_day FROM xpost where xpost_day WHERE xpost_day BETWEEN :startday AND :endday"), startday=startdate, endday=enddate)
        posts = []
        for row in result.all():
            posts.append(row['xpost_day'])
        return sorted(posts)   

def load_records_from_chart_table(chartType, sinceDate, untilDate):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM chart WHERE charttype = :ctype AND period BETWEEN :since AND :until"), {'ctype':chartType, 'since':sinceDate, 'until':untilDate})
    posts = []
    for row in result.all():
      posts.append(row)
    return posts 

def load_records_day_top_ten(sinceDate):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT tag,concat(left(xpost_content,40), '...','View in X'),url,views FROM xpost WHERE xpost_day = :since ORDER BY views DESC LIMIT 10"), {'since':sinceDate})
    posts = []
    for row in result.all():
      posts.append(row)
    return posts    

def load_all_xposts_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from xpost"))
        posts = []
        for row in result.all():
            posts.append(dict(row))
        return posts 

def load_yesterday_xposts_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from xpost where time > now() - interval '1 day'"))
        posts = []
        for row in result.all():
            posts.append(dict(row))
        return posts 

def load_within_week_xposts_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from xpost where time > now() - interval '1 week'"))
        posts = []
        for row in result.all():
            posts.append(dict(row))
        return posts                    
    
def load_within_month_xposts_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from xpost where time > now() - interval '1 month'"))
        posts = []
        for row in result.all():
            posts.append(dict(row))
        return posts

def load_within_year_xposts_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from xpost where time > now() - interval '1 year'"))
        posts = []
        for row in result.all():
            posts.append(dict(row))
        return posts    