from flask import Flask, render_template, session, redirect, url_for, request, flash
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = "loisel.t@hotmail.fr"
SENDER_PASSWORD = "votre_mot_de_passe"
RECEIVER_EMAIL = "loisel.t@hotmail.fr"

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    panier = session.get('panier', {})
    total_articles = sum(panier.values())
    return render_template('index.html', products=products, total_articles=total_articles)

@app.route('/ajouter/<int:product_id>')
def ajouter_au_panier(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT stock FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()

    if 'panier' not in session:
        session['panier'] = {}
  
    panier = session['panier']
    str_id = str(product_id)

    if product:
        stock_disponible = product['stock']
        quantite_actuelle = panier.get(str_id, 0)

    if quantite_actuelle < stock_disponible:
        panier[str_id] = quantite_actuelle + 1
        session.modified = True

    else:
        pass

    return redirect(url_for('index'))

@app.route('/panier')
def afficher_panier():
    panier = session.get('panier', {})
    
    if not panier:
        return render_template('panier.html', items=[], total=0, total_articles=0)

    ids = [int(p_id) for p_id in panier.keys()]
    
    conn = get_db_connection()

    placeholders = ','.join(['?'] * len(ids))
    query = f"SELECT * FROM products WHERE id IN ({placeholders})"
    products = conn.execute(query, ids).fetchall()
    conn.close()
    
    items = []
    total = 0
    total_articles = 0
    
    for product in products:
        p_id_str = str(product['id'])
        qte = panier.get(p_id_str, 0)
        sous_total = product['price'] * qte
        total += sous_total
        total_articles += qte
        
        items.append({
            'id': product['id'],
            'title': product['title'],
            'price': product['price'],
            'quantite': qte,
            'sous_total': sous_total,
            'image_url': product['image_url']
        })
        
    return render_template('panier.html', items=items, total=total, total_articles=total_articles)

@app.route('/retirer/<int:product_id>')
def retirer_du_panier(product_id):
    panier = session.get('panier', {})
    str_id = str(product_id)

    if str_id in panier:
        if panier[str_id] > 1:
            panier[str_id] -= 1
        else:
            panier.pop(str_id)
            
        session.modified = True  # Indique à Flask que la session a changé

    return redirect(url_for('afficher_panier'))

@app.route('/valider_commande', methods=['POST'])
def valider_commande():
    panier = session.get('panier', {})

    if not panier:
        return redirect(url_for('index'))

    nom_client = request.form.get('nom', 'Client')
    email_client = request.form.get('email', 'Non précisé')

    ids = [int(p_id) for p_id in panier.keys()]
    conn = get_db_connection()
    placeholders = ','.join(['?'] * len(ids))
    products = conn.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", ids).fetchall()
    conn.close()

    recap_produits =   ""
    total = 0
    for product in products:
        qte = panier.get(str(product['id']), 0)
        st = product['price'] * qte
        total += st
        recap_produits += f" - {product['title']} x {qte} : {st:.2f} €\n"

    msg = MIMEMultipart()   
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"🛒 Nouvelle commande de {nom_client}"  

    corps_mail = f"""
    Nouvelle commande reçue !

    Client : {nom_client}
    Email : {email_client}

    Détails de la commande :
    {recap_produits}

    TOTAL : {total:.2f} €
    """
    msg.attach(MIMEText(corps_mail, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        session.pop('panier', None)
        print("✅ Email envoyé avec succès !")
        return render_template('confirmation.html')

    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de l'email : {e}")
        return f"Erreur lors de l'envoi de l'email : {e}"

if __name__ == '__main__':
    app.run(debug=True)