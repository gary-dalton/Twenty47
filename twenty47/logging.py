#!/usr/bin/env python
#

#
"""Test harness for the logging module. Tests BufferingSMTPHandler, an alternative implementation
of SMTPHandler.

Copyright (C) 2001-2002 Vinay Sajip. All Rights Reserved.

Modified to handle SMTP_SSL connections
"""
import string, logging, logging.handlers 
from logging import Formatter

class BufferingSMTP_SSLHandler(logging.handlers.BufferingHandler):
    '''
    Modified to handle SMTP_SSL connections
    '''
    # Copyright 2001-2002 by Vinay Sajip. All Rights Reserved.
    #
    # Permission to use, copy, modify, and distribute this software and its
    # documentation for any purpose and without fee is hereby granted,
    # provided that the above copyright notice appear in all copies and that
    # both that copyright notice and this permission notice appear in
    # supporting documentation, and that the name of Vinay Sajip
    # not be used in advertising or publicity pertaining to distribution
    # of the software without specific, written prior permission.
    # VINAY SAJIP DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
    # ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
    # VINAY SAJIP BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
    # ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
    # IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
    # OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
    #
    # This file is part of the Python logging distribution. See
    # http://www.red-dove.com/python_logging.html

    def __init__(self, server, port, username, password, fromaddr, toaddrs, subject, capacity):
        logging.handlers.BufferingHandler.__init__(self, capacity)
        self.fromaddr = fromaddr
        self.toaddrs = toaddrs
        self.subject = subject
        self.mailhost = server
        self.mailport = port
        self.username = username
        self.password = password
        self.setFormatter(logging.Formatter("%(asctime)s %(levelname)-5s %(message)s"))

    def flush(self):
        if len(self.buffer) > 0:
            try:
                import smtplib
                smtp = smtplib.SMTP_SSL(self.mailhost, self.mailport)
                msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (self.fromaddr, string.join(self.toaddrs, ","), self.subject)
                for record in self.buffer:
                    s = self.format(record)
                    print s
                    msg = msg + s + "\r\n"
                smtp.login(self.username, self.password)
                smtp.sendmail(self.fromaddr, self.toaddrs, msg)
                smtp.quit()
            except:
                self.handleError(None)  # no particular record
            self.buffer = []

'''
Set up logging
'''
if app.config['LOG_TO_FILE']:
    file_handler = logging.handlers.RotatingFileHandler(
                  app.config['LOG_FILENAME'],
                  maxBytes=100000,
                  backupCount=5)
    file_handler.setLevel(app.config['LOG_FILE_LEVEL'])
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(file_handler)
    
if app.config['LOG_TO_EMAIL']:
    mail_handler = BufferingSMTP_SSLHandler(
        app.config['MAIL_SERVER'],
        app.config['MAIL_PORT'],
        app.config['MAIL_USERNAME'],
        app.config['MAIL_PASSWORD'],
        app.config['DEFAULT_MAIL_SENDER'],
        app.config['LOG_EMAIL_TO'],
        app.config['LOG_EMAIL_SUBJECT'],
        0,
        )
    mail_handler.setLevel(logging.WARNING)
    mail_handler.setFormatter(Formatter('''
    Message type:       %(levelname)s
    Location:           %(pathname)s:%(lineno)d
    Module:             %(module)s
    Function:           %(funcName)s
    Time:               %(asctime)s

    Message:

    %(message)s
    '''))
    app.logger.addHandler(mail_handler)
