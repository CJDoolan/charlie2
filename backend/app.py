from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, 
    static_folder='../public', 
    static_url_path=''
)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:3001"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def serve_react_app():
    return send_from_directory(app.static_folder, 'login.html')




@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')  # 获取姓名
    email = data.get('email')  # 获取电子邮件
    password = data.get('password')  # 获取密码

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists!"}), 400

    hashed_password = generate_password_hash(password)  # 使用默认哈希方法
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/home')
def serve_home():
    return send_from_directory('../public/frontend/booklog/public', 'index.html')
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials!"}), 401

    user_data = {
        "message": "Login successful!",
        "user": {
            "email": user.email,
            "name": email.split('@')[0]  
        }
    }
    print("Sending user data:", user_data)  
    return jsonify(user_data), 200

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
print(f"Upload folder path: {UPLOAD_FOLDER}")  

ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print(f"Created upload folder: {UPLOAD_FOLDER}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload-pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print(f"File saved to: {file_path}")
        if os.path.exists(file_path):
            print(f"File exists at: {file_path}")
            print(f"File size: {os.path.getsize(file_path)} bytes")
        return jsonify({
            "message": "File uploaded successfully",
            "filename": filename
        }), 200
    
    return jsonify({"message": "Invalid file type"}), 400

@app.route('/api/get-pdf/<filename>', methods=['GET'])
def get_pdf(filename):
    try:
        filename = secure_filename(filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(f"Attempting to serve file from: {file_path}")
        
        if os.path.exists(file_path):
            print(f"File found: {file_path}")
            print(f"File size: {os.path.getsize(file_path)} bytes")
            
            response = send_from_directory(app.config['UPLOAD_FOLDER'], filename)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            response.headers['Cache-Control'] = 'no-cache'
            print("Response headers:", dict(response.headers))
            return response
        else:
            print(f"File not found: {file_path}")
            return jsonify({"message": "File not found"}), 404
    except Exception as e:
        print(f"Error serving file: {str(e)}")
        return jsonify({"message": f"Error serving file: {str(e)}"}), 500

@app.route('/reader')
def serve_reader():
    return send_from_directory('../public/frontend/home/public', 'index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)