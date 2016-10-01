from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm
from .patient import get_patient, get_all_patients


@main.route('/', methods=['GET', 'POST'])
def index():
    """"Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form)


@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)


@main.route('/patients')
def patients():
    """Show list of patients
    """
    return render_template('patients.html', patients=get_all_patients())

@main.route('/patient_info/<_id>')
def patient_info(_id):
    """Show recorded patient info and chat."""
    p = get_patient(_id)
    print _id
    print p.name
    chat_log = p.get_chatlog()
    return render_template('patient_info.html', patient=p, chat_log=chat_log)
