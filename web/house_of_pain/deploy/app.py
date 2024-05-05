from flask import *

import random
import re

app = Flask(__name__, static_folder='static')

ssti_pattern = re.compile(r'[!@#$%^&*{}[\]]', re.MULTILINE)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    random_number = random.randint(1, 6)

    if request.method == 'POST':
        shortcode = request.form['shortcode']
        print(shortcode)
        if "\r\n" in shortcode:
            parts = shortcode.split("\r\n")
            part_to_check = parts[0]
            if ssti_pattern.search(part_to_check):
                return render_template('hack.html')
        else:
            if ssti_pattern.search(shortcode):
                return render_template('hack.html')

        data = [render_template_string(shortcode)]

        if random_number == 1:
            return render_template('stark.html', data=data)
        elif random_number == 2:
            return render_template('baratheon.html', data=data)
        elif random_number == 3:
            return render_template('greyjoy.html', data=data)
        elif random_number == 4:
            return render_template('lannister.html', data=data)
        elif random_number == 5:
            return render_template('targaryen.html', data=data)
        elif random_number == 6:
            return render_template('tyrell.html', data=data)

if __name__ == "__main__":
    app.run(port=5555)