from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

# =========================
# DATABASE (IN MEMORY)
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

GLOBAL_CHAT = []
O5_CHAT = []

# =========================
# HEALTH CHECK (OPTIONAL)
# =========================
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "SCP SERVER ONLINE"})

# =========================
# LOGIN
# =========================
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    u = data.get("user")
    p = data.get("password")

    user = USERS.get(u)

    if user and user["password"] == p:
        return jsonify({
            "ok": True,
            "user": user
        })

    return jsonify({"ok": False})

# =========================
# USERS SYNC
# =========================
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(USERS)

@app.route("/users/update", methods=["POST"])
def update_user():
    data = request.json

    try:
        USERS[data["user"]] = {
            "password": data["password"],
            "clearance": int(data["clearance"]),
            "role": data["role"]
        }
        return jsonify({"ok": True})
    except:
        return jsonify({"ok": False})

# =========================
# WORLD / SITE SYSTEM
# =========================
@app.route("/get_world", methods=["GET"])
def get_world():
    return jsonify(WORLD)

@app.route("/update_site", methods=["POST"])
def update_site():
    data = request.json

    site = data.get("site")
    status = data.get("status")
    alert = data.get("alert")

    if site in WORLD["sites"]:
        WORLD["sites"][site]["status"] = status
        WORLD["sites"][site]["alert"] = alert

    return jsonify({"ok": True})

# =========================
# GLOBAL CHAT
# =========================
@app.route("/chat/send", methods=["POST"])
def chat_send():
    data = request.json

    GLOBAL_CHAT.append({
        "user": data["user"],
        "msg": data["msg"]
    })

    return jsonify({"ok": True})

@app.route("/chat/get", methods=["GET"])
def chat_get():
    return jsonify(GLOBAL_CHAT)

# =========================
# O5 ENCRYPTED CHAT (BASE64)
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
    decoded = []

    for m in O5_CHAT:
        try:
            decoded.append({
                "user": m["user"],
                "msg": base64.b64decode(m["msg"]).decode()
            })
        except:
            pass

    return jsonify(decoded)

# =========================
# RUN SERVER (RENDER SAFE)
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)