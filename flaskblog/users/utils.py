import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


def save_picture(form_picture):
    """
    save profile picture into local storage
    :param form_picture: picture file
    :return: random hex name to be saved as picture name
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    """
    function to send password reset email
    :param user: intended user
    :return: None
    """
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='donotreply@demo.com', recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link,
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request please ignore the mail and no changes will be made.    
    """
    mail.send(msg)
