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
    plot_path = None
    if request.method == 'POST':
        file = request.files.get('image')
        if file and file.filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            resultado = solve_from_image(filepath)
        if isinstance(resultado, tuple) and len(resultado) == 3:
            latex, solution, plot_path = resultado
        else:
            latex, solution = resultado
            plot_path = None
    
    return render_template('index.html', latex=latex, solution=solution, plot_path=plot_path)

if __name__ == '__main__':
    app.run(debug=True)