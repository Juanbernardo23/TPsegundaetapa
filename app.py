from flask import Flask, render_template, request
from solver.ocr_and_solver import solve_from_image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    latex = None
    solution = None

    if request.method == 'POST':
        file = request.files.get('image')
        if file and file.filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            latex, solution = solve_from_image(filepath)

    return render_template('index.html', latex=latex, solution=solution)
if __name__ == '__main__':
    app.run(debug=True)