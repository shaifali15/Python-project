from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"

@app.route('/', methods=['GET', 'POST'])
def greet():
    if request.method == 'POST':
        name = request.form['name']
        try:
            new_user = User(username=name)
            db.session.add(new_user)
            db.session.commit()
            return f'Hello, {name}! Your data has been stored in the database.'
        except IntegrityError:
            db.session.rollback()
            return f'The username "{name}" already exists. Please choose a different username.'
    
    users = User.query.all()
    return render_template('greet_form.html', users=users)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
