
from server import db, mail, get_app
from flask_mail import Message

def send_mail(subject, msg_body, msg_html, dest):
    '''
    envoie un mail aux administrateurs de l'application
    '''
    app = get_app()
    msg = Message(subject,
            sender=app.config['MAIL_SENDER'],
            recipients=[dest]
            )

    msg.body = msg_body
    msg.html = msg_html

    with app.app_context():
        mail.send(msg)
