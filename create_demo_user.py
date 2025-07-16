#!/usr/bin/env python3
"""
Script pour créer un utilisateur de démonstration
"""
import sys
import os

# Ajouter le répertoire parent au path pour importer app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, session, User, init_db
from werkzeug.security import generate_password_hash

def create_demo_user():
    """Crée un utilisateur de démonstration"""
    
    # Initialiser la base de données
    with app.app_context():
        init_db()
        
        # Vérifier si l'utilisateur demo existe déjà
        existing_user = session.query(User).filter_by(username='demo').first()
        if existing_user:
            print("✅ L'utilisateur de démonstration existe déjà")
            print(f"   Nom d'utilisateur: demo")
            print(f"   Mot de passe: demo123")
            return
        
        # Créer l'utilisateur demo
        demo_user = User(
            username='demo',
            password_hash=generate_password_hash('demo123'),
            total_points=150,  # Quelques points pour la démo
            level=2
        )
        
        session.add(demo_user)
        session.commit()
        
        print("🎉 Utilisateur de démonstration créé avec succès!")
        print(f"   Nom d'utilisateur: demo")
        print(f"   Mot de passe: demo123")
        print(f"   Points: 150")
        print(f"   Niveau: 2")

if __name__ == '__main__':
    create_demo_user()
