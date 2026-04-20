import requests
from flask import Flask, request, jsonify
import json
app = Flask(__name__)
DATA_FILE = 'data.json'
def fetch():
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/posts', timeout=5)
        response.raise_for_status()
        posts = response.json()
        filtered = []
        for p in posts:
            if p['userId'] == 1:
                filtered.append(p)
        posts = filtered
        return posts
    except Exception as e:
        print("Error fetching data:", e)
        return []
def fetch_contries():
    try: 
        url = "https://countries.trevorblades.com/"
        query = """
        query {
        countries {
            name
            capital
            currency
        }
        }
        """
        res = requests.post(url, json={'query': query}, timeout=5)
        res.raise_for_status()
        countries = res.json()["data"]["countries"][:5]
        return countries
    except Exception as e: 
        print("Error fetching countries:", e)
        return []
def process_posts(posts):
    for post in posts:
        l = len(post.get('body', ''))
        post['body_length'] = l
        if l < 50:
            category = 'short'
        elif l < 150:
            category = 'medium'
        else:
            category = 'long'
        post['category'] = category
    return posts
def combine_data(posts, countries):
    return {
        "posts": posts,
        "countries": countries
    }
def save_to_file(data):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print("Error saving data:", e)
def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            return data
    except Exception as e:
        return {"posts": [], "countries": []}
    
@app.route('/posts', methods=['GET'])
def get_posts():
    data = load_data()
    posts = data.get('posts', [])
    category = request.args.get('category')
    if category:
        posts = [p for p in posts if p.get('category') == category]
    return jsonify(posts)

@app.route('/stats', methods=['GET'])
def get_stats():
    data = load_data()
    posts = data.get('posts', [])
    total = len(posts)
    if total == 0:
        return jsonify({"total_posts": 0, "average_length": 0, "long_posts": 0})
    average_length = sum(p.get('body_length', 0) for p in posts) / total
    long_posts = sum(1 for p in posts if p.get('category') == 'long')
    return jsonify({
        "total_posts": total,
        "average_length": average_length,
        "long_posts": long_posts
    })
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        new_data = request.json
        print("Webhook received:", new_data)

        data = load_data()

        if "webhook_events" not in data:
            data["webhook_events"] = []

        data["webhook_events"].append(new_data)

        save_to_file(data)

        return jsonify({"status": "received"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400




def run_pipeline():
    print("Running pipeline...")

    posts = fetch()
    countries = fetch_contries()

    posts = process_posts(posts)

    combined = combine_data(posts, countries)

    save_to_file(combined)

    print("Pipeline completed!")



API_KEY = "secret123"

@app.before_request
def check_api_key():
    if request.path.startswith("/posts") or request.path.startswith("/stats"):
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        

if __name__ == "__main__":
    run_pipeline()  
    app.run(debug=True)