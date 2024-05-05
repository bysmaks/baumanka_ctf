import sqlite3, os, re
from flask import Flask, jsonify, render_template, request, g

app = Flask(__name__)
app.database = "main.db"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/v1.0/storeAPI', methods=['GET'])
def storeapi():
    if request.method == 'GET':
        g.db = connect_db()
        curs = g.db.execute("SELECT * FROM char_db")
        items = [{'items':[dict(name=row[0], fandom=row[1], status=row[2]) for row in curs.fetchall()]}]
        g.db.close()
        return jsonify(items)

@app.route('/api/v1.0/storeAPI/<item>', methods=['GET'])
def searchAPI(item):
    g.db = connect_db()
    pattern = r'[@#$%^=&]'
    union_pattern = r'\bUNION\b'
    drop_pattern = r'\bDROP\b'
    alter_pattern = r'\bALTER\b'
    true_pattern = r'\bTRUE\b'
    
    if re.search(pattern, item) or re.search(union_pattern, item) or re.search(drop_pattern, item, flags=re.IGNORECASE) or re.search(alter_pattern, item, flags=re.IGNORECASE) or re.search(true_pattern, item, flags=re.IGNORECASE):
        return render_template('error.html', error=error)
    else:
        curs = g.db.execute("SELECT * FROM char_db WHERE fandom = '%s'" %item)
        results = [dict(name=row[0], fandom=row[1], status=row[2]) for row in curs.fetchall()]
        g.db.close()
        return jsonify(results)

@app.errorhandler(404)
def page_not_found_error(error):
    return render_template('error.html', error=error)

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error=error)

def connect_db():
    return sqlite3.connect(app.database)

if __name__ == "__main__":

    if not os.path.exists(app.database):
        with sqlite3.connect(app.database) as connection:
            c = connection.cursor()
            c.execute("""CREATE TABLE char_db(name TEXT, fandom TEXT, status TEXT)""")
            c.execute('INSERT INTO char_db VALUES("Sansa", "Game of Thrones", "alive")')
            c.execute('INSERT INTO char_db VALUES("Laena", "The House of Dragon", "dead")')
            c.execute('INSERT INTO char_db VALUES("Déagol", "The Lord of the Ring", "dead")')
            c.execute('INSERT INTO char_db VALUES("Shadowheart", "Baldurs gate 3", "depends")')
            c.execute('INSERT INTO char_db VALUES("Arya", "Game of Thrones", "alive")')
            c.execute('INSERT INTO char_db VALUES("Ciri", "The Witcher", "depends")')
            c.execute('INSERT INTO char_db VALUES("Theon", "Game of Thrones", "dead")')
            c.execute('INSERT INTO char_db VALUES("Lae’zel", "Baldurs gate 3", "depends")')
            c.execute('INSERT INTO char_db VALUES("Khamûl", "The Lord of the Ring", "dead")')
            c.execute('INSERT INTO char_db VALUES("Rhaenyra", "The House of Dragon", "alive")')
            c.execute('INSERT INTO char_db VALUES("Daenerys", "Game of Thrones", "dead")')
            c.execute('INSERT INTO char_db VALUES("Gale", "Baldurs gate 3", "depends")')
            c.execute('INSERT INTO char_db VALUES("Frodo", "The Lord of the Ring", "alive")')
            c.execute('INSERT INTO char_db VALUES("Yadriel", "Y3Rme2RBcmtfZmFuVGEzeV9pc19jbDBzZXJfdGhhbl9VX3RoMW5rXzF0XzFzfQ==", "N/A")')
            connection.commit()
            connection.close()

    app.run()
