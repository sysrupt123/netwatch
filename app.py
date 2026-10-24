from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template
from db import (init_db, recent, category_counts, top_domains,
                totals, per_minute)

app = Flask(__name__)


def build_timeline(minutes=30):
    counts = per_minute(minutes)  # {"14:02": 5, ...}
    now = datetime.now().replace(second=0, microsecond=0)
    labels, values = [], []
    # one point per minute, filling quiet minutes with 0
    for i in range(minutes - 1, -1, -1):
        label = (now - timedelta(minutes=i)).strftime("%H:%M")
        labels.append(label)
        values.append(counts.get(label, 0))
    return {"labels": labels, "values": values}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/stats")
def stats():
    data = totals()
    data["recent"] = recent(14)
    data["categories"] = category_counts()
    data["top"] = top_domains(8)
    data["timeline"] = build_timeline(30)
    return jsonify(data)


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5001, debug=False)
