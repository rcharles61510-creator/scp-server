from flask import Flask, request, jsonify

app = Flask(__name__)

# =========================
# GLOBAL STATE (MULTIPLAYER WORLD)
# =========================
users = {
    "raydin": {"password": "0N3f0r4ll", "clearance": 5}
}

sites = {
    "Site-19": {"status": "STABLE", "alert": "GREEN"},
    "Site-23": {"status": "STABLE", "alert": "GREEN"},
    "Site-81": {"status": "STABLE", "alert": "GREEN"}
}

mtf_deployments = {}

# =========================
# LOGIN SYSTEM
# =========================
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = data["user"]
    pw = data["password"]

    if user in users and users[user]["password"] == pw:
        return jsonify({
            "success": True,
            "clearance": users[user]["clearance"]
        })

    return jsonify({"success": False})

# =========================
# GET WORLD STATE
# =========================
@app.route("/get_world")
def get_world():
    return jsonify({
        "sites": sites,
        "mtf": mtf_deployments
    })

# =========================
# UPDATE SITE STATUS
# =========================
@app.route("/update_site", methods=["POST"])
def update_site():
    data = request.json

    site = data["site"]
    status = data["status"]
    alert = data.get("alert", "GREEN")

    sites[site]["status"] = status
    sites[site]["alert"] = alert

    return {"ok": True}

# =========================
# MTF DEPLOYMENT SYNC
# =========================
@app.route("/deploy_mtf", methods=["POST"])
def deploy_mtf():
    data = request.json

    mtf = data["mtf"]
    site = data["site"]

    mtf_deployments[mtf] = site

    return {"ok": True}

# =========================
# ADD USER (ADMIN FEATURE LATER)
# =========================
@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json

    user = data["user"]
    password = data["password"]
    clearance = data["clearance"]

    users[user] = {
        "password": password,
        "clearance": clearance
    }

    return {"ok": True}

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)