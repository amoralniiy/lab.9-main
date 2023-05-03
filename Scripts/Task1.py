from flask import Flask, render_template, url_for, redirect, request
import sqlalchemy as db




def searchdd(serchText):

    select_query = db.select(experience).where(experience.columns.company == serchText)
    select_result = connection.execute((select_query))
    searchGemas =select_result.fetchall()
    if len(searchGemas) ==0:
        select_query = db.select(experience).where(experience.columns.term == serchText)
        select_result = connection.execute((select_query))
        searchGemas = select_result.fetchall()
    return searchGemas


app = Flask(__name__)


try:
    engine = db.create_engine('mysql+pymysql://root:ason121245@localhost:3306/my_database')
    connection = engine.connect()
    print("Connect DB")
except Exception as ex:
    print("ERROR Connect DB")
    print(ex)

metadata = db.MetaData()
experience = db.Table('work_experience', metadata,
                 db.Column('work_experience_id', db.Integer, primary_key=True),
                 db.Column('company', db.Text),
                 db.Column('term', db.Integer))

metadata.create_all(engine)

insertion_query = experience.insert().values([
    {"company":"Software engineer", "term":5},
    {"company":"Marketing manager", "term":7},
    {"company":"Graphic designer", "term":3},
    {"company":"Human resources coordinator", "term":2},
    {"company":"Sales representative", "term":4},
    {"company":"Project manager", "term":8},
    {"company":"Customer service representative", "term":1},
    {"company":" Financial analyst ", "term":5},
    {"company":"Product manager ", "term":6},
    {"company":"Operations manager", "term":10}

])
#connection.execute(insertion_query)

selall = db.select(experience)
selres = connection.execute(selall)
allExperience = selres.fetchall()

@app.route('/', methods =["GET", "POST"])
def index():
    sum = 0
    for i in range(len(allExperience)):
        sum  = sum + allExperience[i][2]
    if request.method == "POST":
        if request.form.get('clear') =='Clear':
            d = searchdd("s")
            return render_template('index.html', allExperience=d, len=len(d))
        elif request.form.get('all') =='All List':
            render_template('index.html' , allExperience = allExperience, len = len(allExperience))
        elif request.form.get('searchBtn') == 'Search':
            a = request.form.get("search")
            d = searchdd(a)
            return render_template('index.html' , allExperience = d, len = len(d))
    return render_template('index.html' , allExperience = allExperience, len = len(allExperience),sum = sum)

if __name__ == '__main__':
    app.run(debug=True, port=5001 )




