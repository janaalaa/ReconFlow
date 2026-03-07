from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'reconflow.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/claim', methods=['POST'])
def claim():
    data = request.json
    user = data.get('user')
    asset = data.get('asset')
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT assigned_to FROM assets WHERE asset_value=?", (asset,))
    row = c.fetchone()

    if row:
        if row['assigned_to']:
            return jsonify({"status": "error", "message": f"❌ Asset already claimed by {row['assigned_to']}!"}), 400
        else:
            c.execute("UPDATE assets SET assigned_to=?, status='In Progress' WHERE asset_value=?", (user, asset))
    else:
        c.execute("INSERT INTO assets (target_domain, asset_value, status, assigned_to) VALUES ('Manual', ?, 'In Progress', ?)", (asset, user))

    c.execute("INSERT INTO activity_logs (user, action, asset) VALUES (?, 'CLAIM', ?)", (user, asset))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": f"🎯 {asset} successfully claimed by {user}!"})

# الجزء الجديد: فك الحجز (Release)
@app.route('/release', methods=['POST'])
def release():
    data = request.json
    user = data.get('user')
    asset = data.get('asset')
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT assigned_to FROM assets WHERE asset_value=?", (asset,))
    row = c.fetchone()

    if not row or row['assigned_to'] != user:
        return jsonify({"status": "error", "message": "❌ You can only release assets you claimed!"}), 403

    c.execute("UPDATE assets SET assigned_to=NULL, status='Clean' WHERE asset_value=?", (asset,))
    c.execute("INSERT INTO activity_logs (user, action, asset) VALUES (?, 'RELEASE', ?)", (user, asset))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": f"🔓 {asset} has been released by {user}."})

@app.route('/dashboard')
def dashboard():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM assets ORDER BY date_added DESC")
    assets_data = c.fetchall()
    conn.close()
    return render_template('dashboard.html', assets=assets_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
