from flask import Flask, render_template, jsonify, request
from database import engine, load_all_xposts_from_db,load_yesterday_xposts_from_db, load_within_week_xposts_from_db, load_within_month_xposts_from_db, load_within_year_xposts_from_db, load_jobs_from_db, load_job_from_db, add_application_to_db 

app = Flask(__name__)


@app.route("/")
def hello_monitor():
    allxposts = load_all_xposts_from_db
    return render_template('home.html', posts=allxposts,company_name='Somewa')

@app.route("/xpostchart")
def chart():
    return render_template('xpostchart.html')

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

