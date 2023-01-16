from flask import Blueprint, render_template, flash, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .model import Note
import datetime
from .import db
import json

views = Blueprint("views", __name__)

#@views.route('/', methods = ["GET", "POST"])
@views.route('/home', methods = ["GET", "POST"])
def home():
    results = current_user.notes
    if request.method == "POST":
        if request.form["submitbtn"] == "Submit":
            note = request.form.get("titleInput")
            due = request.form.get("datetimeInput")
            if not due:
                due = None

            if len(note) < 1:
                flash("Note too short!", category="error")
            else:
                new_note = Note(data = note, duedate = due, status="Incomplete", user_id = current_user.id)
                db.session.add(new_note)
                db.session.commit()
                results = current_user.notes
                flash("Note added!", category="success") 

        elif request.form["submitbtn"] == "filterSort":
            filter_element = request.form.get("state_filter")
            sort_element = request.form.get("date_sort")
            if str(filter_element) != "All":
                results = Note.query.filter_by(user_id = current_user.id, status=str(filter_element)).order_by(sort_element)
            else:
                results = Note.query.filter_by(user_id = current_user.id).order_by(sort_element)
    return render_template("index.html", user=current_user, notes= results)

@views.route("/delete-note", methods = ["GET", "POST"])
def delete_note():
    note = json.loads(request.data)
    note_id = note["note_id"]
    result = Note.query.get(note_id)
    if result:
        if result.user_id == current_user.id:
            db.session.delete(result)
            db.session.commit()
    return jsonify({'code': 200})

@views.route('/complete', methods = ["GET", "POST"])
def complete():  
    note = json.loads(request.data)
    note_id = note["note_id"]
    result = Note.query.get(note_id)
    if result:
        if result.user_id == current_user.id:
            if result.status == "Incomplete":
                result.status = "Completed"
            else:
                result.status = "Incomplete"
            db.session.commit()
    return jsonify({'code': 200})



@views.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    result = Note.query.filter_by(user_id = current_user.id, id=int(id)).first()
    if result:
        if request.method == 'POST':
            if request.form["action"] == "update":
                note = request.form.get("titleInput")
                due = request.form.get("datetimeInput")
                if not due:
                    due = datetime.datetime.now()
                result.data = note
                result.duedate = due
                db.session.commit()
                flash('Note updated successfully!', category="success")
                return redirect(url_for("views.home"))
            elif request.form["action"] == "cancel":
                flash('Cancel update!', category="success")
                return redirect(url_for("views.home"))
        return render_template('edit_album.html', user=current_user, prev = result)
    else:
        return 'error loading #{id}'.format(id=id)