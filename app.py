from flask import Flask, request, jsonify

app = Flask(__name__)

# =========================
# GLOBAL DATABASE (IN MEMORY)
# =========================
USERS = {
    "raydin": {
        "password": "0N3f0r4ll",
        "clearance": 5,
        "role": "O5"
    }
}

WORLD = {
    "sites": {
        "Site-19": {"status": "STABLE", "alert": "GREEN"},
        "Site-23": {"status": "STABLE", "alert": "GREEN"},
        "Site-81": {"status": "STABLE", "alert": "GREEN"}
    }
}

# =========================
# GET USERS (SYNC ALL DEVICES)
# =========================
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(USERS)

# =========================
# ADD / UPDATE USER (O5 ONLY CONTROL)
# =========================
@app.route("/users/update", methods=["POST"])
def update_user():
    data = request.json

    user = data["user"]
    USERS[user] = {
        "password": data["password"],
        "clearance": int(data["clearance"]),
        "role": data["role"]
    }

    return jsonify({"status": "ok", "users": USERS})

# =========================
# LOGIN CHECK (OPTIONAL)
# =========================
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    u = data["user"]
    p = data["password"]

    if u in USERS and USERS[u]["password"] == p:
        return jsonify({"ok": True, "user": USERS[u]})

    return jsonify({"ok": False})

# =========================
# WORLD STATE SYNC (SITES)
# =========================
@app.route("/get_world", methods=["GET"])
def get_world():
    return jsonify(WORLD)

@app.route("/update_site", methods=["POST"])
def update_site():
    data = request.json
    site = data["site"]

    WORLD["sites"][site]["status"] = data["status"]
    WORLD["sites"][site]["alert"] = data["alert"]

    return jsonify({"status": "updated", "world": WORLD})

# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)