from flask import Flask
import time

app = Flask(__name__)

cache = {}
cache_time = {}

@app.route('/data')
def get_data():
 if "data" in cache and time.time() - cache_time["data"] < 10:
    return {"message": cache["data"], "source": "cache"}
 
 time.sleep(3)
 result = "This is refreshed data"
 
 cache["data"] = result
 cache_time["data"] = time.time()
 
 return {"message": result, "source": "computed"}

app.run(host="0.0.0.0", port=5000)

