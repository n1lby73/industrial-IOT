from flask import Flask, render_template, url_for, request, redirect, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

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
    print(data['btnvalue'])
    # return "work"
    return jsonify(success=True)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3565)