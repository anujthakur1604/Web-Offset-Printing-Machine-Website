from flask import Flask, render_template, request, redirect
import sqlite3
from flask_mail import Mail, Message

app = Flask(__name__)

# ----------------- MAIL CONFIG -----------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "gogagraphics0001@gmail.com"      # apna Gmail
app.config['MAIL_PASSWORD'] = "dyaddbykxbbwkpkr"                # Gmail App Password
app.config['MAIL_DEFAULT_SENDER'] = "gogagraphics0001@gmail.com"

mail = Mail(app)

# ----------------- PRODUCTS DATA -----------------
products_data = [
    {
        "id": 1,
        "name": "Mono Unit Web Offset Printing Machine",
        "desc": "High speed printing for newspapers and commercial use.",
        "image": "machine1.jpg",
        "details": {
            "description": " A Mono Unit Web Offset Printing Machine is a type of printing press designed for web-fed printing, meaning it uses a continuous roll of paper (a 'web') rather than individual sheets. The term 'mono unit' signifies that it is a single printing unit capable of printing on a single paper web."
        }
    },
    {
        "id": 2,
        "name": "Books Printing Machine",
        "desc": "Perfect for books & magazines.",
        "image": "machine2.jpg",
        "details": {
            "description": " A book printing machine isn't just one single type of press, but rather a category of specialized equipment used to produce books from digital files to a finished, bound product. The specific type of machine used depends on the volume, quality, and type of book being printed. "
        }
    },
    {
        "id": 3,
        "name": "4 HI Tower Printing Machine",
        "desc": "Multi-color high-speed printing.",
        "image": "machine3.jpg",
        "details": {
            "description": " A 4HI Tower printing machine, also known as a four-high tower press, is a type of printing unit commonly used in newspaper and magazine production. The term '4-HI refers to the vertical arrangement of its four printing cylinders. "
        }
    },
    {
        "id": 4,
        "name": "Reel Stand",
        "desc": "Strong reel stand for large paper rolls.",
        "image": "Reel Stand.png",
        "details": {
            "description": " A reel stand is a crucial component of a web-fed printing press. Its primary function is to hold, unwind, and feed a continuous roll (or 'web') of paper into the printing unit. It is the Heavy duty reel stand for handling large paper rolls efficiently. "
        }
    },
    {
        "id": 5,
        "name": "Standard Folder",
        "desc": "Efficient folding unit for newspapers.",
        "image": "Standard Folder.png",
        "details": {
            "description": "A standard folder is a machine or unit on a printing press that folds the printed paper web into a finished product. It's a critical component in the production of newspapers, magazines, and other publications, as it takes the long, continuous paper web and converts it into a more manageable, folded format."
        }
    },
    {
        "id": 6,
        "name": "3C Satellite Unit",
        "desc": "Advanced satellite printing unit.",
        "image": "3C Satellite unit.png",
        "details": {
            "description": " A 3-Color (3C) Satellite Unit is a specialized printing unit used in web offset presses, particularly in newspaper and commercial printing. Its main purpose is to add three colors to one side of the paper web. It also Provides high-quality, efficient multi-color printing for newspapers. "
        }
    }
]

# ----------------- ROUTES -----------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('products.html', machines=products_data)

@app.route('/products/<int:product_id>')
def product_detail(product_id):
    product = next((item for item in products_data if item["id"] == product_id), None)
    return render_template('product_detail.html', product=product)

# ----------------- CONTACT FORM -----------------
@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    mobile = request.form['mobile']
    message = request.form['message']

    # 1. Save to database
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT, email TEXT, mobile TEXT, message TEXT)''')
    c.execute("INSERT INTO contacts (name, email, mobile, message) VALUES (?, ?, ?, ?)",
              (name, email, mobile, message))
    conn.commit()
    conn.close()

    # 2. Send email to Admin
    try:
        msg = Message("📩 New Contact Form Submission",
                      recipients=["gogagraphics0001@gmail.com"])   # admin email
        msg.body = f"""
        You have a new contact form submission:

        Name: {name}
        Email: {email}
        Mobile: {mobile}
        Message: {message}
        """
        mail.send(msg)

        # Confirmation email to User
        confirm = Message("✅ We received your message",
                          recipients=[email])
        confirm.body = f"""
        Hi {name},

        Thanks for contacting Goga Graphics Company.
        We received your message and will reply soon.

        Your Details:
        Name: {name}
        Email: {email}
        Mobile: {mobile}
        Message: {message}

        Regards,
        Goga Graphics Team
        """
        mail.send(confirm)

    except Exception as e:
        print("Error sending email:", e)

    return redirect('/')

# ----------------- ADMIN VIEW -----------------
@app.route('/admin/contacts')
def view_contacts():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM contacts")
    data = c.fetchall()
    conn.close()
    return render_template('contacts.html', contacts=data)

# ----------------- RUN APP -----------------
if __name__ == '__main__':
    app.run(debug=True)
