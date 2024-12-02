from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Database setup
def create_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS students (username TEXT, password TEXT, marks INTEGER)')
    c.execute("INSERT INTO students (username, password, marks) VALUES ('student1', 'password123', 85)")
    c.execute("INSERT INTO students (username, password, marks) VALUES ('student2', 'password456', 92)")
    c.execute("INSERT INTO students (username, password, marks) VALUES ('admin', 'adminpass', 100)")
    conn.commit()
    conn.close()

create_db()

# Route to handle login and display marks
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # SQL Injection vulnerable query
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM students WHERE username='{username}' AND password='{password}'")
        user = c.fetchone()
        conn.close()
        
        if user:
            marks = user[2]
            return render_template_string('''
                <div class="welcome">
                    <h2>Welcome, {{ username }}</h2>
                    <p>Your marks: {{ marks }}</p>
                    <p><strong>Flag:</strong> r00t@locahost{SIM9L3_Sql_Injection}</p>
                </div>
            ''', username=username, marks=marks)
        else:
            return "Invalid login. Try again."
    
    return render_template_string('''
        <html>
            <head>
                <title>90's Sql Injection Bug</title>
                <style>
                    /* Global Styles */
                    body {
                        font-family: 'Arial', sans-serif;
                        background-color: #f0f4f8;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }

                    .container {
                        background-color: #fff;
                        padding: 40px;
                        border-radius: 10px;
                        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                        width: 300px;
                        text-align: center;
                    }

                    h1 {
                        color: #333;
                        font-size: 24px;
                    }

                    h2 {
                        color: #4CAF50;
                        font-size: 28px;
                    }

                    input[type="text"], input[type="password"] {
                        width: 100%;
                        padding: 10px;
                        margin: 10px 0;
                        border-radius: 5px;
                        border: 1px solid #ccc;
                        font-size: 16px;
                    }

                    button {
                        width: 100%;
                        padding: 10px;
                        background-color: #4CAF50;
                        color: #fff;
                        border: none;
                        border-radius: 5px;
                        font-size: 16px;
                        cursor: pointer;
                    }

                    button:hover {
                        background-color: #45a049;
                    }

                    .welcome {
                        padding: 40px;
                        background-color: #fff;
                        border-radius: 10px;
                        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                        text-align: center;
                    }

                    .welcome p {
                        font-size: 20px;
                        color: #333;
                    }

                    .welcome strong {
                        color: #4CAF50;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Sql</h1>
                    <form method="POST">
                        <div class="input-group">
                            <label>Username:</label>
                            <input type="text" name="username" required>
                        </div>
                        <div class="input-group">
                            <label>Password:</label>
                            <input type="password" name="password" required>
                        </div>
                        <button type="submit">Login</button>
                    </form>
                </div>
            </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

