import os
import smtplib
import pandas as pd
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "secretkey"

UPLOAD_FOLDER = "uploads"
USER_DATA = "user_data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(USER_DATA, exist_ok=True)


def send_email_smtp(sender, password, receiver, subject, body, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
        part = MIMEBase('application', 'octet-stream')
        with open(attachment_path, 'rb') as f:
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        f'attachment; filename={os.path.basename(attachment_path)}')
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_folder = os.path.join(USER_DATA, username)
        os.makedirs(user_folder, exist_ok=True)
        with open(os.path.join(user_folder, 'profile.txt'), 'w') as f:
            f.write(password)
        flash('Account created!')
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            with open(os.path.join(USER_DATA, username, 'profile.txt')) as f:
                if f.read() == password:
                    session['user'] = username
                    return redirect(url_for('dashboard'))
        except:
            pass
        flash('Invalid credentials')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# ✅ UPDATED DASHBOARD — REAL STATS
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    stats_file = os.path.join(USER_DATA, session['user'], 'stats.csv')

    total_sent = 0
    total_failed = 0
    campaigns = 0

    if os.path.exists(stats_file):
        df = pd.read_csv(stats_file)
        total_sent = df['success'].sum()
        total_failed = df['failed'].sum()
        campaigns = len(df)

    used = total_sent + total_failed

    return render_template(
        'dashboard.html',
        user=session['user'],
        total_sent=total_sent,
        campaigns=campaigns,
        failed=total_failed,
        used=used
    )


# ✅ UPDATED SEND — SAVE STATS
@app.route('/send', methods=['GET', 'POST'])
def send():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        sender = request.form['email']
        password = request.form['password']
        subject = request.form['subject']
        message = request.form['message']

        excel_file = request.files['excel']
        attachment = request.files.get('attachment')

        excel_path = os.path.join(UPLOAD_FOLDER, excel_file.filename)
        excel_file.save(excel_path)

        attachment_path = None
        if attachment and attachment.filename:
            attachment_path = os.path.join(UPLOAD_FOLDER, attachment.filename)
            attachment.save(attachment_path)

        df = pd.read_excel(excel_path)

        success, failed = 0, 0

        for _, row in df.iterrows():
            try:
                personalized = message.replace('{Name}', str(row['Name'])) \
                                      .replace('{Company}', str(row['Company']))

                send_email_smtp(sender, password, row['Email'],
                                subject, personalized, attachment_path)
                success += 1
            except:
                failed += 1

        # ✅ SAVE STATS
        user_folder = os.path.join(USER_DATA, session['user'])
        stats_file = os.path.join(user_folder, 'stats.csv')
        file_exists = os.path.isfile(stats_file)

        with open(stats_file, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['success', 'failed'])
            writer.writerow([success, failed])

        flash(f"Done! Success: {success}, Failed: {failed}")

    return render_template('send_email.html')

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)