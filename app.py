from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Configuration de la session
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'votre_cle_secrete')  # Change cela par une vraie clé secrète
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Liste pour stocker les utilisateurs (avec mots de passe hashés)
users = []

# Route pour la page d'accueil avec le formulaire d'ajout d'utilisateur
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_name = request.form['name']
        password = request.form['password']

        # Vérifier si l'utilisateur existe déjà
        for user in users:
            if user['name'] == user_name:
                flash('Nom d’utilisateur déjà pris, veuillez en choisir un autre.')
                return redirect(url_for('index'))

        # Hash du mot de passe
        hashed_password = generate_password_hash(password)

        new_user = {
            "id": len(users) + 1,
            "name": user_name,
            "password": hashed_password  # Stocke le mot de passe haché
        }
        users.append(new_user)
        flash('Utilisateur ajouté avec succès !')  # Message de succès
        return redirect(url_for('users_page'))
    return render_template('index.html')

# Route pour afficher la liste des utilisateurs
@app.route('/users')
def users_page():
    if 'user' not in session:  # Vérifier si l'utilisateur est connecté
        flash('Vous devez vous connecter pour voir cette page.')
        return redirect(url_for('login'))
    return render_template('users.html', users=users)

# Route de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['name']
        password = request.form['password']
        
        # Rechercher l'utilisateur dans la liste
        for user in users:
            if user['name'] == user_name:
                if check_password_hash(user['password'], password):
                    session['user'] = user_name  # Stocke le nom d'utilisateur dans la session
                    flash('Connexion réussie !')
                    return redirect(url_for('users_page'))
                else:
                    flash('Mot de passe incorrect.')
                    return redirect(url_for('login'))
        flash('Utilisateur non trouvé.')
        return redirect(url_for('login'))
    return render_template('login.html')

# Route de déconnexion
@app.route('/logout')
def logout():
    session.pop('user', None)  # Supprime l'utilisateur de la session
    flash('Déconnexion réussie.')  # Message de succès
    return redirect(url_for('index'))  # Redirige vers la page d'accueil

if __name__ == '__main__':
    app.run(debug=True)

    app.run(debug=True)

