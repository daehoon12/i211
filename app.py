from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

CLASSES_PATH = app.root_path + '/classes.csv'
classes_keys=["date", "name", "duration", "type", "trainer", "type", "level", "description"]

@app.route('/')
def index(c=None):
    classes=get_classes()
    if c and c in classes.keys():
        return render_template('classes.html', classes = classes)
    else:
        return render_template('index.html', classes = classes)

@app.route('/classes')
@app.route('/classes/<class_id>')
def classes(class_id=None):
    classes=get_classes()
    if class_id and class_id in classes.keys():
        return render_template('class.html', classes = classes[class_id])
    else:
        return render_template('classes.html', classes = classes)


@app.route('/classes/create', methods=('GET', 'POST'))
@app.route('/classes/create/<class_id>', methods=('GET', 'POST'))
def class_form():
    if request.method =='POST':
        content = request.form
        classes = get_classes()
        q = {}
        q['date'] = request.form['date']
        q['name'] = request.form['name']
        q['duration'] = request.form['duration']
        q['trainer'] = request.form['trainer']
        q['type'] = request.form['type']
        q['level'] = request.form['level']
        q['description'] = request.form['description']

        classes[request.form['name']]=q
        set_classes(classes)
        return redirect(url_for('classes', classes = q))
    return render_template('class_form.html')

@app.route('/classes/<class_id>/edit', methods=('GET', 'POST'))
def edit_form(class_id=None):
    classes = get_classes()

    if request.method =='POST':
        content = request.form
        q = {}
        q['date'] = request.form['date']
        q['name'] = request.form['name']
        q['duration'] = request.form['duration']
        q['trainer'] = request.form['trainer']
        q['type'] = request.form['type']
        q['level'] = request.form['level']
        q['description'] = request.form['description']

        classes[request.form['name']]=q
        set_classes(classes)
        return redirect(url_for('classes', classes = q))
    return render_template('class_form.html', c = classes[class_id])


@app.route('/classes/<class_id>/delete', methods=('GET', 'POST'))
def delete_form(class_id = None):
    classes = get_classes()
    if request.method =='POST':
        content = request.form
        set_classes(classes, content['name'])
        q = get_classes()
        return redirect(url_for('classes', classes = q))
    return render_template('delete_form.html', c = classes[class_id])


def get_classes():
    with open(CLASSES_PATH, 'r') as csvfile:
        data = csv.DictReader(csvfile)
        classes = {}
        for c in data:
            classes[c['name']] = c
    return classes


def set_classes(classes, name = None):
    with open(CLASSES_PATH, mode='w', newline='') as csv_file:
        writer=csv.DictWriter(csv_file, fieldnames=classes_keys)
        writer.writeheader()
        for c in classes.values():
            if c['name'] != name:
                writer.writerow(c)
            

@app.route('/about')
def about():
    return "about"

@app.route('/add_dino')
def add_dino():
    return "add_dino"

@app.route('/dino_quiz')
def dino_quiz():
    return "dino_quiz"


if __name__ == "__main__":
    app.run()