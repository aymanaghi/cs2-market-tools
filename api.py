from flask import Flask, jsonify, request
from utils.steam_api import get_top_skins

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to CS2 Market API 🐍",
        "routes": {
            "/api/top_skins": "Get top CS2 skins. Optional query: ?limit=20"
        }
    })

@app.route("/api/top_skins")
def top_skins():
    # get ?limit= from the URL (default = 10)
    limit = request.args.get("limit", default=10, type=int)

    # fetch data
    skins_df = get_top_skins(limit)
    data = skins_df.to_dict(orient="records")

    return jsonify({
        "count": len(data),
        "results": data
    })

if __name__ == "__main__":
    app.run(debug=True)
