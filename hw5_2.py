from flask import Flask, app
import time
cache = {}

@app.route('/data')
def get_data():
    if "data" in cache:
        return {"message": cache["data"], "source": "cache"}
    
    time.sleep(3)
    result = "This is slow data"
    cache["data"] = result
    return {"message": result, "source": "computed"}