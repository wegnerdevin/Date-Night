from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "data.json")

DEFAULT_DATA = {
    "ideas": {
        "cozy": [
            {"id": "c1", "text": "Movie marathon with blanket forts", "emoji": "🍿"},
            {"id": "c2", "text": "Video game night — you pick", "emoji": "🎮"},
            {"id": "c3", "text": "Bake something new together", "emoji": "🧁"},
            {"id": "c4", "text": "Card games & snacks", "emoji": "🃏"},
            {"id": "c5", "text": "Read the same book aloud", "emoji": "📚"},
            {"id": "c6", "text": "Paint-at-home night", "emoji": "🎨"},
        ],
        "medium": [
            {"id": "m1", "text": "Cook a cuisine you've never tried", "emoji": "🌮"},
            {"id": "m2", "text": "Bowling or mini golf", "emoji": "🎳"},
            {"id": "m3", "text": "Sunrise or sunset picnic", "emoji": "🌅"},
            {"id": "m4", "text": "Live music or open mic night", "emoji": "🎶"},
            {"id": "m5", "text": "Escape room challenge", "emoji": "🧩"},
            {"id": "m6", "text": "Thrift store treasure hunt", "emoji": "🛍️"},
        ],
        "adventure": [
            {"id": "a1", "text": "Rock climbing or bouldering gym", "emoji": "🧗"},
            {"id": "a2", "text": "Bike a trail you've never done", "emoji": "🚴"},
            {"id": "a3", "text": "Amusement park day trip", "emoji": "🎢"},
            {"id": "a4", "text": "Spontaneous camping night", "emoji": "🏕️"},
            {"id": "a5", "text": "Improv or comedy show", "emoji": "🎭"},
            {"id": "a6", "text": "Road trip — no destination set", "emoji": "🌊"},
        ],
    },
    "streak": [False] * 8,
    "next_id": 100,
}


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return json.loads(json.dumps(DEFAULT_DATA))


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/data")
def get_data():
    return jsonify(load_data())


@app.route("/api/add", methods=["POST"])
def add_idea():
    body = request.json
    level = body.get("level")
    text = body.get("text", "").strip()
    emoji = body.get("emoji", "⭐")
    if not text or level not in ("cozy", "medium", "adventure"):
        return jsonify({"error": "invalid"}), 400
    data = load_data()
    new_id = str(data["next_id"])
    data["next_id"] += 1
    data["ideas"][level].append({"id": new_id, "text": text, "emoji": emoji})
    save_data(data)
    return jsonify({"ok": True, "id": new_id})


@app.route("/api/remove", methods=["POST"])
def remove_idea():
    body = request.json
    idea_id = body.get("id")
    data = load_data()
    for level in ("cozy", "medium", "adventure"):
        data["ideas"][level] = [i for i in data["ideas"][level] if i["id"] != idea_id]
    save_data(data)
    return jsonify({"ok": True})


@app.route("/api/streak", methods=["POST"])
def update_streak():
    body = request.json
    streak = body.get("streak")
    if not isinstance(streak, list) or len(streak) != 8:
        return jsonify({"error": "invalid"}), 400
    data = load_data()
    data["streak"] = streak
    save_data(data)
    return jsonify({"ok": True})


if __name__ == "__main__":
    import sys
    os.makedirs("data", exist_ok=True)
    host = "0.0.0.0" if "--host" in sys.argv else "127.0.0.1"
    if host == "0.0.0.0":
        print("\n✨ Date Night app running — share on your local network!")
        print("   Find your IP with: ipconfig (Windows) or ifconfig (Mac/Linux)")
        print("   Then visit: http://<your-ip>:5000\n")
    else:
        print("\n✨ Date Night app running at http://localhost:5000\n")
    app.run(debug=True, host=host, port=5000)
