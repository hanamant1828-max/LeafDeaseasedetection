
import os
import logging
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, flash, redirect, url_for, session
from models import db, User, Analysis
from email_validator import validate_email, EmailNotValidError
from analysis import DiseaseAnalyzer

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///plant_disease.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize database
db.init_app(app)

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create database tables and add default user
with app.app_context():
    db.create_all()
    
    # Create default demo user if it doesn't exist
    demo_user = User.query.filter_by(username='demo').first()
    if not demo_user:
        demo_user = User(
            username='demo',
            email='demo@example.com',
            full_name='Demo User'
        )
        demo_user.set_password('demo123')
        db.session.add(demo_user)
        db.session.commit()
        app.logger.info('Default demo user created: username=demo, password=demo123')

def allowed_file(filename):
    """Check if file extension is allowed."""
    if not filename:
        return False
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    """Decorator to require login for certain routes"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    """Main page with upload form."""
    user = User.query.get(session['user_id'])
    return render_template('index.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page."""
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        full_name = request.form.get('full_name', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not username or len(username) < 3:
            flash('Username must be at least 3 characters long.', 'error')
            return render_template('register.html')
        
        if not full_name:
            flash('Full name is required.', 'error')
            return render_template('register.html')
        
        try:
            # Validate email
            validate_email(email)
        except EmailNotValidError:
            flash('Please enter a valid email address.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please use a different email or log in.', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username, email=email, full_name=full_name)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            app.logger.error(f"Registration error: {e}")
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email', '').strip()
        password = request.form.get('password', '')
        
        if not username_or_email or not password:
            flash('Please enter both username/email and password.', 'error')
            return render_template('login.html')
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username_or_email) | 
            (User.email == username_or_email)
        ).first()
        
        if user and user.check_password(password):
            if user.is_active:
                session['user_id'] = user.id
                session['username'] = user.username
                flash(f'Welcome back, {user.full_name}!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Your account has been deactivated. Please contact support.', 'error')
        else:
            flash('Invalid username/email or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user."""
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """Handle file upload and perform disease analysis."""
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload an image file (PNG, JPG, JPEG, GIF, BMP, WEBP)', 'error')
        return redirect(url_for('index'))
    
    try:
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(filepath)
        
        analyzer = DiseaseAnalyzer()
        result = analyzer.analyze_image(filepath)
        
        analysis = Analysis(
            user_id=session['user_id'],
            image_filename=unique_filename,
            disease_detected=result['disease_name'],
            confidence=result['confidence'],
            severity=result['severity'],
            description=result['description'],
            treatment=result['treatment'],
            prevention=result['prevention']
        )
        
        db.session.add(analysis)
        db.session.commit()
        
        flash('Image analyzed successfully!', 'success')
        return redirect(url_for('view_result', analysis_id=analysis.id))
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Analysis error: {e}")
        flash('An error occurred during analysis. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/result/<int:analysis_id>')
@login_required
def view_result(analysis_id):
    """View analysis result."""
    analysis = Analysis.query.get_or_404(analysis_id)
    
    if analysis.user_id != session['user_id']:
        flash('You do not have permission to view this analysis.', 'error')
        return redirect(url_for('index'))
    
    return render_template('result.html', analysis=analysis)

@app.route('/history')
@login_required
def history():
    """View analysis history."""
    user = User.query.get(session['user_id'])
    analyses = Analysis.query.filter_by(user_id=session['user_id']).order_by(Analysis.created_at.desc()).all()
    return render_template('history.html', user=user, analyses=analyses)

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    flash('File too large. Please upload an image smaller than 16MB.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
