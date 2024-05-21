# # ユーザーからのリクエストを処理する関数定義
from flask import Flask, render_template, request, redirect
from app import app, db
from app.models import Task
from datetime import datetime

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    print("Received POST request at /add")
    title = request.form.get('title')
    content = request.form.get('content')
    due_date_str = request.form.get('due_date')
    status = request.form.get('status', '未実施')  # デフォルト値を 'ToDo' に設定
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
    new_task = Task(title=title, content=content, due_date=due_date)
    print(f"Title: {title}, Content: {content}, Due Date: {due_date}")
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return 'Task not found', 404
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.content = request.form.get('content')
        due_date_str = request.form.get('due_date')
        task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
        task.status = request.form.get('status')
        print(f"Title: {task.title}, Content: {task.content}, Due Date: {task.due_date}")
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', task=task)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return 'Task not found', 404
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/detail/<int:task_id>')
def detail_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return 'Task not found', 404
    return render_template('detail.html', task=task)

