from flask import Flask, request, render_template
import os
import random
import redis
import socket
import sys

app = Flask(__name__)

# Load configurations from environment or config file
app.config.from_pyfile('config_file.cfg')

if ("VOTE1VALUE" in os.environ and os.environ['VOTE1VALUE']):
    button1 = os.environ['VOTE1VALUE']
else:
    button1 = app.config['VOTE1VALUE']

if ("VOTE2VALUE" in os.environ and os.environ['VOTE2VALUE']):
    button2 = os.environ['VOTE2VALUE']
else:
    button2 = app.config['VOTE2VALUE']

if ("TITLE" in os.environ and os.environ['TITLE']):
    title = os.environ['TITLE']
else:
    title = app.config['TITLE']

if ("FIRSTNAME" in os.environ and os.environ['FIRSTNAME']):
    firstname = os.environ['FIRSTNAME']
else:
    firstname = app.config['FIRSTNAME']


if ("LASTNAME" in os.environ and os.environ['LASTNAME']):
    lastname = os.environ['LASTNAME']
else:
    lastname = app.config['LASTNAME']
    
    
# Redis configurations
redis_server = os.environ['REDIS']

# Redis Connection
try:
    if "REDIS_PWD" in os.environ:
        r = redis.StrictRedis(host=redis_server,
                        port=6379,
                        password=os.environ['REDIS_PWD'])
    else:
        r = redis.Redis(redis_server)
    r.ping()
except redis.ConnectionError:
    exit('Failed to connect to Redis, terminating.')

# Change title to host name to demo NLB
if app.config['SHOWHOST'] == "true":
    title = socket.gethostname()

# Init Redis
if not r.get(button1): r.set(button1,0)
if not r.get(button2): r.set(button2,0)
if not r.get(firstname): r.set(firstname,"alderano f")
if not r.get(lastname): r.set(lastname,"")


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':

        # Get current values
        #vote1 = r.get(button1).decode('utf-8')
        #vote2 = r.get(button2).decode('utf-8')   
        fname = r.get(firstname)
        #lname = r.get(lastname)

        # Return index with values
        #return render_template("index.html", value1=int(vote1), value2=int(vote2), button1=button1, button2=button2, title=title)
        return render_template("index.html", value1=str(fname), button1=button1, button2=button2, title=title)
       

    elif request.method == 'POST':

        if request.form['vote'] == 'reset':
            r.set(firstname,"alderano fileni")
            fname = r.get(firstname)
            return render_template("index.html", value1=str(fname), title=title)
            # Empty table and return results
            #r.set(button1,0)
            #r.set(button2,0)
            #vote1 = r.get(button1).decode('utf-8')
            #vote2 = r.get(button2).decode('utf-8')
            #return render_template("index.html", value1=int(vote1), value2=int(vote2), button1=button1, button2=button2, title=title)
            
        
        else:

            # Insert vote result into DB
            #vote = request.form['vote']
            fname = request.form['name']
            #lname = request.form['lname']
            #r.incr(vote,1)
            r.set(firstname, "kaskdlakd")
            return render_template("index.html", value1=str(fname), title=title)
            #r.set(lastname, lname)
      
            
            # Get current values
            #vote1 = r.get(button1).decode('utf-8')
            #vote2 = r.get(button2).decode('utf-8')  
                
            # Return results
            #return render_template("index.html", value1=int(vote1), value2=int(vote2), button1=button1, button2=button2, title=title)

if __name__ == "__main__":
    app.run()
