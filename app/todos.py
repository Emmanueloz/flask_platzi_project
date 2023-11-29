from flask import Blueprint, flash, redirect, render_template, session, url_for
from app.forms import TodosForm
from app.utils.db import db
from app.models.todos import Todos
from flask_login import login_required, current_user

todos = Blueprint('todos', __name__, url_prefix='/todos')


@todos.route("/add", methods=["GET", "POST"])
@login_required
def add():
    user_id = current_user.id
    print(user_id)

    todo_form = TodosForm()
    todo_form.id_user.data = user_id
    context = {
        'todo_form': todo_form,
        'username': "sads"
    }

    if todo_form.validate_on_submit():
        id_use = todo_form.id_user.data
        description = todo_form.description.data
        flash("Todo registrado con éxito")
        new_todo = Todos(id_use, description)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("hello.index"))
    return render_template('todos.html', **context)
