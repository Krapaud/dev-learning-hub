from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_super_securisee'  # Changez ceci en production

# Configuration de la base de données
DATABASE = 'users.db'

def init_db():
    """Initialise la base de données avec les tables nécessaires"""
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Créer un admin par défaut si aucun utilisateur n'existe
        cursor = conn.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            admin_password = generate_password_hash('admin123')
            conn.execute('''
                INSERT INTO users (username, email, password_hash, is_admin)
                VALUES (?, ?, ?, ?)
            ''', ('admin', 'admin@geeksite.com', admin_password, True))
        
        conn.commit()

def get_user_by_username(username):
    """Récupère un utilisateur par son nom d'utilisateur"""
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute('SELECT * FROM users WHERE username = ?', (username,))
        return cursor.fetchone()

def get_user_by_id(user_id):
    """Récupère un utilisateur par son ID"""
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        return cursor.fetchone()

def login_required(f):
    """Décorateur pour protéger les routes nécessitant une authentification"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Décorateur pour protéger les routes d'administration"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user = get_user_by_id(session['user_id'])
        if not user or not user['is_admin']:
            flash('Accès refusé. Privilèges administrateur requis.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Page de connexion"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = get_user_by_username(username)
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            
            # Mise à jour de la dernière connexion
            with sqlite3.connect(DATABASE) as conn:
                conn.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', 
                           (user['id'],))
                conn.commit()
            
            flash(f'Connexion réussie ! Bienvenue {username}', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Page d'inscription"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Le mot de passe doit contenir au moins 6 caractères', 'error')
            return render_template('register.html')
        
        # Vérifier si l'utilisateur existe déjà
        if get_user_by_username(username):
            flash('Ce nom d\'utilisateur est déjà pris', 'error')
            return render_template('register.html')
        
        try:
            password_hash = generate_password_hash(password)
            with sqlite3.connect(DATABASE) as conn:
                conn.execute('''
                    INSERT INTO users (username, email, password_hash)
                    VALUES (?, ?, ?)
                ''', (username, email, password_hash))
                conn.commit()
            
            flash('Inscription réussie ! Vous pouvez maintenant vous connecter', 'success')
            return redirect(url_for('login'))
        
        except sqlite3.IntegrityError:
            flash('Cet email est déjà utilisé', 'error')
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Tableau de bord utilisateur"""
    user = get_user_by_id(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/admin')
@admin_required
def admin_panel():
    """Panel d'administration"""
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute('SELECT * FROM users ORDER BY created_at DESC')
        users = cursor.fetchall()
    
    return render_template('admin.html', users=users)

@app.route('/admin/toggle_admin/<int:user_id>')
@admin_required
def toggle_admin(user_id):
    """Basculer le statut administrateur d'un utilisateur"""
    if user_id == session['user_id']:
        flash('Vous ne pouvez pas modifier vos propres privilèges', 'error')
        return redirect(url_for('admin_panel'))
    
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('UPDATE users SET is_admin = NOT is_admin WHERE id = ?', (user_id,))
        conn.commit()
    
    flash('Privilèges utilisateur mis à jour', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/admin/delete_user/<int:user_id>')
@admin_required
def delete_user(user_id):
    """Supprimer un utilisateur"""
    if user_id == session['user_id']:
        flash('Vous ne pouvez pas supprimer votre propre compte', 'error')
        return redirect(url_for('admin_panel'))
    
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
    
    flash('Utilisateur supprimé', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/profile')
@login_required
def profile():
    """Page de profil utilisateur"""
    user = get_user_by_id(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    """Déconnexion"""
    session.clear()
    flash('Vous avez été déconnecté', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
