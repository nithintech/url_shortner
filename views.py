from flask import render_template, flash, redirect
from app import app
from forms import urlfield
import sqlite3
from random import choice
from string import letters,digits
@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
def index():
    form=urlfield()
    c=sqlite3.connect('test.db')
    try:
    	c.execute("CREATE TABLE SHORTNER(SHORT TEXT,URL TEXT)")
    except:
	None
    if form.validate_on_submit():
		c=sqlite3.connect('test.db')
		s="SELECT SHORT FROM SHORTNER WHERE URL==\"%s\""%(form.url.data)
		l=c.execute(s)
		con=False
		for v in l:
			con=True
			sk=c.execute("SELECT SHORT FROM SHORTNER WHERE URL==\"%s\""%(form.url.data))
			return render_template("index.html",form=form,posts=c.execute("SELECT SHORT,URL FROM SHORTNER"),out=sk)
		if con==False:
			k=letters+digits+"+=-#"
			while True:
				key=choice(k)+choice(k)+choice(k)+choice(k)
				con=False
				sh=c.execute("SELECT URL FROM SHORTNER WHERE SHORT==\"%s\""%(key))
				for s in sh:
					con=True
				if con==False:
					break
			c.execute("INSERT INTO SHORTNER VALUES(\"%s\",\"%s\")"%(key,form.url.data))
			c.commit()
			return render_template("index.html",form=form,posts=c.execute("SELECT SHORT,URL FROM SHORTNER"),out=c.execute("SELECT SHORT FROM SHORTNER WHERE URL==\"%s\""%(form.url.data)))
    return render_template("index.html",form=form,posts=c.execute("SELECT SHORT,URL FROM SHORTNER"))
@app.route('/<url>',methods=['GET','POST'])
def redirection(url):
	c=sqlite3.connect('test.db')
	a="SELECT URL FROM SHORTNER WHERE SHORT==\"%s\""%(url)
	a=c.execute(a)
	for k in a:
		k=k[0]
		if 'https://' in k or 'http://' in k:
			return redirect(k)
		else:
			return redirect('http://'+k)
