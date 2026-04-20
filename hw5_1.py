from flask import Flask
import time

app = Flask(__name__)

@app.route('/data')
def get_data():
    time.sleep(3) 
    return {"message": "This is slow data"}

app.run(host="0.0.0.0", port=5000)