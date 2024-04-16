from datetime import date, datetime, timedelta
from flask import Flask, render_template, jsonify, request, request, redirect, url_for, flash
from database import engine, load_jobs_from_db, load_job_from_db, add_application_to_db
from xpost import engine, load_records_day_top_ten, load_xposts_users_onemonth_from_db, load_xposts_data_interval_from_db,load_xposts_users_interval_from_db, load_all_xposts_from_db,load_yesterday_xposts_from_db, load_within_week_xposts_from_db, load_within_month_xposts_from_db, load_within_year_xposts_from_db,load_records_from_chart_table
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route("/base")
def hello_base():
    return render_template('base.html')

@app.route('/companyprofile.html', methods=['GET', 'POST'])
def company_profile():
    return render_template('companyprofile.html')     

@app.route('/charts/daily/<period>')
def chart_xpost_daily(period):
#  print("Period: ",period)
  format = '%Y-%m-%d'
  periods = []
  number = 1
  while number < 11:
    prevDate = date.today()-timedelta(days = number)
    periods.append(prevDate.strftime(format))
    number = number + 1
  
  if period == "0" or period == "1"  or period == "1"  or period == "2" or period == "3" or period == "4" or period == "5" or period == "6" or period == "7" or period == "8" or period == "9":
     period = periods[int(period)]
  if len(period) == 3:
     period = (date.today()-timedelta(days = 1)).strftime(format)    
  try:   
    periodObj = datetime.strptime(period, '%Y-%m-%d').date()
    nextDayObj = periodObj + timedelta(days=1)    
  except Exception as e:
    print("Error Unable to convert: ",str(e))  
  #print(nextDayObj)  
  toptenposts = []
  toptenposts = load_records_day_top_ten(sinceDate=periodObj) 
  xposts = [] 
  xposts = load_records_from_chart_table(chartType='daily', sinceDate=periodObj, untilDate=nextDayObj)
  dashboardname = 'Leading Posters for '+period  
  dashboardtype = 'bar' 
  replies = []
  reposts = []
  likes = []
  views = []
  repliescon = []
  repostscon = []
  likescon = []
  viewscon = []
  for xpost in xposts:
    if xpost[2] == 'replies':
      replies = xpost    
      for i in range(len(xpost[3])):
         repliescon.append(str(xpost[3][i])+' '+str(xpost[4][i]))
    if xpost[2] == 'reposts':
      reposts = xpost 
      for i in range(len(xpost[3])):
         repostscon.append(str(xpost[3][i])+' '+str(xpost[4][i]))
    if xpost[2] == 'likes':
      likes = xpost
      for i in range(len(xpost[3])):
         likescon.append(str(xpost[3][i])+' '+str(xpost[4][i]))
    if xpost[2] == 'views':
      views = xpost  
      for i in range(len(xpost[3])):
         viewscon.append(str(xpost[3][i])+' '+str(xpost[4][i]))        
  #X Users list
  users = " ".join(str(x) for x in views[3])
  return render_template('xcharts.html', 
                         replies=replies, 
                         reposts=reposts, 
                         likes=likes,
                         views=views, 
                         period = period,
                         periods = periods,
                         users = users,
                         repliescon = repliescon,
                         repostscon = repostscon,
                         likescon = likescon,
                         viewscon =viewscon,
                         toptenposts = toptenposts,
                         dashboardname=dashboardname, 
                         dashboardtype=dashboardtype)

@app.route('/x', methods=['GET', 'POST'])
def xcall():
  format = '%Y-%m-%d'
  period = (date.today()-timedelta(days = 1)).strftime(format)
  return redirect(url_for('chart_xpost_daily', period=period))

@app.route('/test', methods=['GET', 'POST'])
def index():
 #   teacher = User.query.filter_by(email=current_user.email).first()
 #   form = MeanScore()
 #   if form.validate_on_submit():
 #       meanscore = Meanscore(
 #           term=form.term.data,
 #           math=form.math.data,
 #           english=form.english.data,
 #           science=form.science.data,
 #           ict=form.ict.data,
 #           history=form.history.data,
 #           author=current_user)
  #      db.session.add(meanscore)
  #      db.session.commit()
  #      flash('Your mean score has been recorded.')
   #     return redirect(url_for('index'))

   # term_meanscore = teacher.meanscores.all()
    terms = []
    terms = ['Mangalani']*5
    math = []
    english = []
    science = []
    ict = []
    history = []
  #  for term in term_meanscore:
  #      terms.append(term.term)
  #      math.append(term.math)
  #      english.append(term.english)
  #      science.append(term.science)
  #      ict.append(term.ict)
  #      history.append(term.history)
    return render_template(
        'index.html',
  #      form=form,
  #      title='Home',
  #      teacher=teacher,
        terms=terms,
        math=math,
        english=english,
        science=science,
        ict=ict,
        history=history)

@app.route("/")
def hello_monitor():
    allxposts = load_all_xposts_from_db
    return render_template('home.html', posts=allxposts,company_name='Somewa')

@app.route("/test2")
def hello_mangalani():
    return render_template('test2.html')

@app.route("/chartexample")
def chart_example():
    return render_template('chartexample.html')

@app.route("/charttest")
def chart_test():
    return render_template('test.html')

@app.route("/charttwitter")
def chart_x():
    return render_template('twitter.html')

@app.route("/chartbase")
def chart_base():
    return render_template('base.html')


#_field can be any of these
#  comments_count 
#  repost_count 
#  likes_count 
#  impression_count
#  followers_count
#  following_count
@app.route("/chartxpost")
def chart_xpost_interval():
   xposts = []
   dashboardname = 'Leading Likes in the past 7 days'  
   dashboardtype = 'bar' 
   _tag = 'tag'
   _field = 'likes'
   _interval = '1 week'
   _xpostusers = load_xposts_users_interval_from_db(_tag, _interval)
   print(_xpostusers)   
   for post in _xpostusers:
      xposts.append(load_xposts_data_interval_from_db(post,_field, _interval))
   return render_template('chartxpost.html', users = _xpostusers, xpostscount = xposts, dashboardname=dashboardname, dashboardtype=dashboardtype)

#@app.route("/xpostchart")
#def chart_x():
#    xpostrows = []
#    xpostdates = []
#    xpostusers = []
#    xpostrows = load_xposts_users_onemonth_from_db
#    xpostdates = list(dict.fromkeys(xpostrows['xpost_day']))
#    xpostusers = list(dict.fromkeys(xpostrows['tag']))
#    for date in xpostdates:
        

#    return render_template('xpostchart.html')


@app.route("/xposts")
def get_xposts():
    dayposts = load_yesterday_xposts_from_db
    weekposts = load_within_week_xposts_from_db
    monthposts = load_within_month_xposts_from_db
    yearposts = load_within_year_xposts_from_db 
    allxposts = load_all_xposts_from_db
    return render_template('xitem.html', allxposts=allxposts, weekposts=weekposts, dayposts=dayposts, monthposts=monthposts, yearposts=yearposts, company_name='Somewa')

@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)

@app.route("/job/<id>")
def show_job(id):
  job = load_job_from_db(id)
  
  if not job:
    return "Not Found", 404
  
  return render_template('jobpage.html', 
                         job=job)

@app.route("/api/job/<id>")
def show_job_json(id):
  job = load_job_from_db(id)
  return jsonify(job)

@app.route("/job/<id>/apply", methods=['post'])
def apply_to_job(id):
  data = request.form
  job = load_job_from_db(id)
  add_application_to_db(id, data)
  return render_template('application_submitted.html', 
                         application=data,
                         job=job)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

