def notify(subject, body):
    import smtplib
    import json
    from datetime import datetime

    gmail_user = 'breno.cardoso@estudante.ufla.br'
    gmail_password = 'iewjbnmnpujoavsm'

    sent_from = gmail_user
    to = ['k4t0mono@gmail.com']

    email_text = """\
From: {}
To: {}
Subject: {}

{}
""".format(sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')