"""
AI导航站 - Flask 后端API
支持: 前端数据查询 + 管理员CRUD + JWT认证
"""
import os, sqlite3, hashlib, uuid, functools, json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder=None)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'nav.db')
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')

SECRET_KEY = hashlib.sha256(f"ai-nav-secret-{uuid.uuid4()}".encode()).hexdigest()
TOKENS = {}  # simple in-memory token store

# ─── Database helpers ───────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def row_to_dict(row):
    if row is None:
        return None
    return dict(row)

# ─── Auth ───────────────────────────────────────────────────────────

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token():
    return hashlib.sha256(uuid.uuid4().bytes).hexdigest()

def require_auth(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if token not in TOKENS:
            return jsonify({"error": "未登录或登录已过期"}), 401
        return fn(*args, **kwargs)
    return wrapper

# ─── Public API ─────────────────────────────────────────────────────

@app.route('/api/categories')
def get_categories():
    """获取所有分类及其站点"""
    db = get_db()
    cats = db.execute("SELECT * FROM categories ORDER BY sort_order").fetchall()
    result = []
    for cat in cats:
        sites = db.execute(
            "SELECT * FROM sites WHERE category_id=? ORDER BY sort_order",
            (cat['id'],)
        ).fetchall()
        result.append({
            "id": cat['id'],
            "name": cat['name'],
            "icon": cat['icon'],
            "sort_order": cat['sort_order'],
            "sites": [row_to_dict(s) for s in sites],
            "count": len(sites)
        })
    db.close()
    return jsonify(result)

@app.route('/api/sites')
def get_sites():
    """获取站点列表，可选按分类筛选"""
    db = get_db()
    cat_id = request.args.get('category_id')
    if cat_id:
        sites = db.execute(
            "SELECT * FROM sites WHERE category_id=? ORDER BY sort_order", (cat_id,)
        ).fetchall()
    else:
        sites = db.execute("SELECT s.*, c.name as category_name FROM sites s "
                           "JOIN categories c ON s.category_id=c.id ORDER BY c.sort_order, s.sort_order").fetchall()
    db.close()
    return jsonify([row_to_dict(s) for s in sites])

@app.route('/api/stats')
def get_stats():
    """获取统计数据"""
    db = get_db()
    total_sites = db.execute("SELECT COUNT(*) FROM sites").fetchone()[0]
    total_cats = db.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
    db.close()
    return jsonify({"total_sites": total_sites, "total_categories": total_cats})

# ─── Admin Auth ─────────────────────────────────────────────────────

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    db = get_db()
    admin = db.execute("SELECT * FROM admins WHERE username=? AND password_hash=?",
                       (username, hash_password(password))).fetchone()
    db.close()
    if admin:
        token = generate_token()
        TOKENS[token] = {"admin_id": admin['id'], "username": admin['username']}
        return jsonify({"token": token, "username": admin['username']})
    return jsonify({"error": "用户名或密码错误"}), 401

@app.route('/api/admin/verify', methods=['GET'])
@require_auth
def admin_verify():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    info = TOKENS.get(token)
    return jsonify({"ok": True, "username": info['username']})

# ─── Admin: Categories CRUD ─────────────────────────────────────────

@app.route('/api/admin/categories', methods=['GET'])
@require_auth
def admin_get_categories():
    db = get_db()
    cats = db.execute("SELECT c.*, (SELECT COUNT(*) FROM sites WHERE category_id=c.id) as site_count "
                      "FROM categories c ORDER BY sort_order").fetchall()
    db.close()
    return jsonify([row_to_dict(c) for c in cats])

@app.route('/api/admin/categories', methods=['POST'])
@require_auth
def admin_create_category():
    data = request.get_json()
    name = data.get('name', '').strip()
    icon = data.get('icon', '📁')
    if not name:
        return jsonify({"error": "分类名称不能为空"}), 400
    db = get_db()
    max_order = db.execute("SELECT COALESCE(MAX(sort_order),0)+1 FROM categories").fetchone()[0]
    cur = db.execute("INSERT INTO categories (name, icon, sort_order) VALUES (?,?,?)",
                     (name, icon, max_order))
    db.commit()
    cat_id = cur.lastrowid
    db.close()
    return jsonify({"id": cat_id, "name": name, "icon": icon}), 201

@app.route('/api/admin/categories/<int:cat_id>', methods=['PUT'])
@require_auth
def admin_update_category(cat_id):
    data = request.get_json()
    name = data.get('name', '').strip()
    icon = data.get('icon')
    if not name:
        return jsonify({"error": "分类名称不能为空"}), 400
    db = get_db()
    if icon:
        db.execute("UPDATE categories SET name=?, icon=? WHERE id=?", (name, icon, cat_id))
    else:
        db.execute("UPDATE categories SET name=? WHERE id=?", (name, cat_id))
    db.commit()
    db.close()
    return jsonify({"ok": True})

@app.route('/api/admin/categories/<int:cat_id>', methods=['DELETE'])
@require_auth
def admin_delete_category(cat_id):
    db = get_db()
    db.execute("DELETE FROM categories WHERE id=?", (cat_id,))
    db.commit()
    db.close()
    return jsonify({"ok": True})

# ─── Admin: Sites CRUD ──────────────────────────────────────────────

@app.route('/api/admin/sites', methods=['GET'])
@require_auth
def admin_get_sites():
    db = get_db()
    cat_id = request.args.get('category_id')
    if cat_id:
        sites = db.execute(
            "SELECT s.*, c.name as category_name FROM sites s "
            "JOIN categories c ON s.category_id=c.id "
            "WHERE s.category_id=? ORDER BY s.sort_order", (cat_id,)
        ).fetchall()
    else:
        sites = db.execute(
            "SELECT s.*, c.name as category_name FROM sites s "
            "JOIN categories c ON s.category_id=c.id ORDER BY c.sort_order, s.sort_order"
        ).fetchall()
    db.close()
    return jsonify([row_to_dict(s) for s in sites])

@app.route('/api/admin/sites', methods=['POST'])
@require_auth
def admin_create_site():
    data = request.get_json()
    name = data.get('name', '').strip()
    url = data.get('url', '').strip()
    category_id = data.get('category_id')
    if not name or not url or not category_id:
        return jsonify({"error": "名称、URL和分类不能为空"}), 400
    db = get_db()
    max_order = db.execute("SELECT COALESCE(MAX(sort_order),0)+1 FROM sites WHERE category_id=?",
                           (category_id,)).fetchone()[0]
    cur = db.execute(
        "INSERT INTO sites (category_id, name, url, description, badge, domain, sort_order) VALUES (?,?,?,?,?,?,?)",
        (category_id, name, url, data.get('description', ''), data.get('badge', ''),
         data.get('domain', url.split('//')[-1].split('/')[0]), max_order)
    )
    db.commit()
    site_id = cur.lastrowid
    db.close()
    return jsonify({"id": site_id}), 201

@app.route('/api/admin/sites/<int:site_id>', methods=['PUT'])
@require_auth
def admin_update_site(site_id):
    data = request.get_json()
    db = get_db()
    db.execute(
        "UPDATE sites SET category_id=?, name=?, url=?, description=?, badge=?, domain=? WHERE id=?",
        (data.get('category_id'), data.get('name', '').strip(), data.get('url', '').strip(),
         data.get('description', ''), data.get('badge', ''),
         data.get('domain', ''), site_id)
    )
    db.commit()
    db.close()
    return jsonify({"ok": True})

@app.route('/api/admin/sites/<int:site_id>', methods=['DELETE'])
@require_auth
def admin_delete_site(site_id):
    db = get_db()
    db.execute("DELETE FROM sites WHERE id=?", (site_id,))
    db.commit()
    db.close()
    return jsonify({"ok": True})

# ─── Serve Frontend ─────────────────────────────────────────────────

@app.route('/')
def serve_index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/admin')
def serve_admin():
    return send_from_directory(FRONTEND_DIR, 'admin.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)

# ─── Main ───────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("\n" + "="*50)
    print("  🤖 AI 导航站 - 后端服务")
    print("="*50)
    print(f"  前端访问: http://localhost:5000")
    print(f"  管理后台: http://localhost:5000/admin")
    print(f"  API:      http://localhost:5000/api/categories")
    print(f"  管理员:   admin / admin123")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
