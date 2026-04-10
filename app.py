from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

# =========================
# DATABASE
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
    }
}

GLOBAL_CHAT = []
O5_CHAT = []

from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

# =========================
# PERSISTENT SAFE USERS
# =========================
USERS = {
    "raydin": {
        "password": "0N3f0r4ll",
        "clearance": 5,
        "role": "O5"
    }
}

# =========================
# SAFE LOGIN (FIXED)
# =========================
@app.route("/login", methods=["POST"])
def login():
    data = request.json or {}

    u = data.get("user", "")
    p = data.get("password", "")

    user = USERS.get(u)

    if not user:
        return jsonify({"ok": False, "error": "USER_NOT_FOUND"})

    if user["password"] != p:
        return jsonify({"ok": False, "error": "WRONG_PASSWORD"})

    return jsonify({
        "ok": True,
        "user": {
            "username": u,          # ✅ THIS WAS MISSING
            "role": user["role"],
            "clearance": user["clearance"]
        }
    })
# =========================
# USERS SYNC (SAFE)
# =========================
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(USERS)

@app.route("/users/update", methods=["POST"])
def update_user():
    data = request.json or {}

    try:
        USERS[data["user"]] = {
            "password": data["password"],
            "clearance": int(data["clearance"]),
            "role": data["role"]
        }
        return jsonify({"ok": True})
    except:
        return jsonify({"ok": False, "error": "BAD_DATA"})

# =========================
# KEEP SERVER ALIVE RESPONSE
# =========================
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ONLINE"})

# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
# =========================
# WORLD
# =========================
@app.route("/get_world", methods=["GET"])
def get_world():
    return jsonify(WORLD)

@app.route("/update_site", methods=["POST"])
def update_site():
    data = request.json
    site = data["site"]

    WORLD["sites"][site] = {
        "status": data["status"],
        "alert": data["alert"]
    }

    return jsonify({"ok": True})

# =========================
# GLOBAL CHAT
# =========================
@app.route("/chat/send", methods=["POST"])
def send_chat():
    data = request.json
    GLOBAL_CHAT.append({
        "user": data["user"],
        "msg": data["msg"]
    })
    return jsonify({"ok": True})

@app.route("/chat/get", methods=["GET"])
def get_chat():
    return jsonify(GLOBAL_CHAT)

# =========================
# O5 ENCRYPTED CHAT
# (simple base64 "encryption")
# =========================
@app.route("/o5/send", methods=["POST"])
def o5_send():
    data = request.json

    encoded = base64.b64encode(data["msg"].encode()).decode()

    O5_CHAT.append({
        "user": data["user"],
        "msg": encoded
    })

    return jsonify({"ok": True})

@app.route("/o5/get", methods=["GET"])
def o5_get():
    decoded = [
        {"user": m["user"], "msg": base64.b64decode(m["msg"]).decode()}
        for m in O5_CHAT
    ]
    return jsonify(decoded)

# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)