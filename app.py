from flask import Flask, render_template
from database import engine, load_all_xposts_from_db,load_yesterday_xposts_from_db, load_within_week_xposts_from_db, load_within_month_xposts_from_db, load_within_year_xposts_from_db 

app = Flask(__name__)



@app.route("/")
def hello_monitor():
    allxposts = load_all_xposts_from_db
    return render_template('home.html', posts=allxposts,company_name='Somewa')

@app.route("/xpostchart")
def chart():
    return render_template('chart.html')

@app.route("/xposts")
def hello_monitor():
    dayposts = load_yesterday_xposts_from_db
    weekposts = load_within_week_xposts_from_db
    monthposts = load_within_month_xposts_from_db
    yearposts = load_within_year_xposts_from_db 
    allxposts = load_all_xposts_from_db
    return render_template('xitem.html', allxposts=allxposts, weekposts=weekposts, dayposts=dayposts, monthposts=monthposts, yearposts=yearposts, company_name='Somewa')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

