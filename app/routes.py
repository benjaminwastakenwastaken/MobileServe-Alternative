#importing app from __init__
from app import app, db
from flask import request, redirect
from app.models import Alert,LoginForm



# creating the first page
@app.route('/')
def test():
    return "Mcdonogh Service Hours Page"

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    #if form.validate_on_submit():
        #flash('Login requested for user {}, remember_me={}'.format(
            #form.username.data, form.remember_me.data))
        #return redirect(url_for('test'))

    return render_template('login.html', title='Sign In', form=form)


# https://www.geeksforgeeks.org/python/flask-http-method/
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')

    alert = Alert(
        action =="submission",
        details==f"{username} submitted a service hour" #what the alert says
    )

    db.session.add(alert)
    db.session.commit()

    return redirect('/')

@app.route('/admin/alerts')
def admin_alerts():
    alerts = Alert.query.order_by(Alert.created_at.desc()).all()
    return render_template('admin_alerts.html', alerts=alerts)

