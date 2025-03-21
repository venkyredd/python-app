from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title="My Flask App")

@app.route('/api/data')
def get_data():
    return jsonify({"message": "This is data from Flask API", "status": "success"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

