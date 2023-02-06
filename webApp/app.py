from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")

db = SQLAlchemy(app)

class esp32(db.Model):

    __tablename__ = 'motorControls'
    id = db.Column(db.Integer, primary_key = True)
    switchState = db.Column(db.String(2), nullable = True)

    # def __repr__(self):
    #     return (f"esp32('{self.switch}')")


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/on')
def on():
    return render_template("run.html")

@app.route('/btn', methods=['POST', 'GET'])
def btn():
    if request.method != 'POST':
        return redirect(url_for('index'))
    
    data = request.get_json()
    status = data['state']
    
    new_value = esp32(switchState=status)

    db.session.add(new_value)
    db.session.commit()
    
    return jsonify(success=True)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3565)