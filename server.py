from flask import Flask, request, jsonify

app = Flask(__name__)

data = {
    "Site-19": "STABLE",
    "Site-23": "STABLE"
}

@app.route("/get_sites")
def get_sites():
    return jsonify(data)

@app.route("/update_site", methods=["POST"])
def update_site():
    json_data = request.json
    site = json_data["site"]
    status = json_data["status"]
    data[site] = status
    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)