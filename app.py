from flask import Flask, render_template
from database import engine, load_all_xposts_from_db,load_yesterday_xposts_from_db, load_within_lastweek_xposts_from_db, load_within_lastmonth_xposts_from_db 

app = Flask(__name__)



@app.route("/")
def hello_monitor():
    xposts = load_all_xposts_from_db
    return render_template('home.html', posts=xposts,company_name='Somewa')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

