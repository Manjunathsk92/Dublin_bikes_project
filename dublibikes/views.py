from flask import render_template
from dublinbikes import dublinbikes

@app.route('/')
def index():
    returnDict={}
    returnDict['user']='Anjali'
    return render_template("index.html",**returnDict)
