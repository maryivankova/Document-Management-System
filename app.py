from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///documents.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Определяем модель документа и истории

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    version = db.Column(db.Integer, default=1)
    history = db.relationship('History', backref='document', lazy=True)


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    version = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Определяем маршруты Flask

# Определяем маршруты Flask (продолжение)

@app.route('/')
def index():
    documents = Document.query.filter_by(is_deleted=False).all()
    return render_template('index.html', documents=documents)

@app.route('/add', methods=['GET', 'POST'])
def add_document():
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        document = Document(name=name, content=content)
        db.session.add(document)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_document(id):
    document = Document.query.get(id)
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        if content != document.content:
            history = History(document_id=document.id, content=document.content, version=document.version)
            db.session.add(history)
            document.version += 1
        document.name = name
        document.content = content
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', document=document)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_document(id):
    document = Document.query.get(id)
    document.is_deleted = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/compare/<int:id>', methods=['GET'])
def compare_document(id):
    document = Document.query.get(id)
    history = History.query.filter_by(document_id=document.id).order_by(History.version.desc()).first()
    if history is None:
        return render_template('compare.html', document=document, message="Изменений в документ внесено не было")
    else:
        return render_template('compare.html', document=document, history=history)


# Запуск приложения
if __name__ == '__main__':
    app.run(host='localhost', port=8080)