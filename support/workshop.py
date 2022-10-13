#!/usr/bin/env python
# encoding: utf-8
#
# Copyright 2020 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.
#
# Run this as follows::
#
#    bin/zope-debug -O 873 run $PWD/support/workshop.py ARGS

from __future__ import print_function
from cStringIO import StringIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.registry.interfaces import IRegistry
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.WorkflowCore import WorkflowException
from zope.component import getUtility
from datetime import date
import logging, sys, argparse, csv, codecs, plone.api, transaction, json, random, time, smtplib


app = globals().get('app', None)  # ``app`` comes from ``instance run`` magic.
_logger = logging.getLogger('Plone')

# 😮 TODO: change these for production
# _overseer = u'sean.kelly@jpl.nasa.gov'
_overseer = u'data-science-wg@jpl.nasa.gov'
_overseerAssistants = (u'sean.kelly@jpl.nasa.gov',)

# 🚨 Change these if the form changes
RESPONSE_COLUMN = 1
FIRST_NAME_COLUMN = 2
AFFILIATION_COLUMN = 5
OTHER_COLUMN = 6

# Pause between messages in seconds
_interEmailWait = 2

_emailSubject = u'''2nd AI and Data Science Workshop is back on as a virtual event, February 9–11, 2021'''

_textEmail = u'''Hello {firstName}

The 2nd AI and Data Science Workshop has been rescheduled as an online,
virtual event on February 9–11, 2021.

Although you registered for the event originally scheduled in March 2020,
we request that you re-confirm your registration at:

    {confirmationURL}

IMPORTANT: you'll need to enter this confirmation code: {code}

Please re-confirm your registration by January 8, 2021. You may also cancel
your registration at the above link if you are unable to attend.

The workshop will include keynote speakers, invited talks, and poster
sessions—all online through video conferencing.

For more information about the workshop, and to encourage colleagues
and friends to register, please visit:

    https://datascience.jpl.nasa.gov/aiworkshop

If we don't hear from you by January 8, 2021, we will cancel your
registration automatically.

Thanks so much for your interest!

Best regards,
2nd AI and Data Science Program Committee
'''

_htmlEmail = u'''
<html>
    <head>
        <title>AI Workshop Confirmation</title>
    </head>
    <body style='font-size=12px; font-family: sans-serif;'>
        <p><img src='https://datascience.jpl.nasa.gov//++theme++ds-theme/assets/images/logo_nasa_trio_black.png'/
            alt='Jet Propulsion Laboratory, California Institute of Technology' /></p>
        <h3>Hello, {firstName}!</h3>
        <p>
            The 2nd AI and Data Science Workshop has been rescheduled as an online,
            virtual event on February 9–11, 2021.
        </p>
        <p>
            Although you registered for the event originally scheduled in March 2020,
            we request that you re-confirm your registration at:
        </p>
        <p style='text-align: center;'>
            <code><a href='{confirmationURL}'>{confirmationURL}</a></code>
        </p>
        <p>
            <em><strong>IMPORTANT</strong>: you'll need to enter this confirmation code:
            <strong style='font-size: 140%;'>{code}</strong></em>
        </p>
        <p>
            Please re-confirm your registration by January 8, 2021. You may also cancel
            your registration at the above link if you are unable to attend.
        </p>
        <p>
            The workshop will include keynote speakers, invited talks, and poster
            sessions—all online through video conferencing.
        </p>
        <p>
            For more information about the workshop, and to encourage colleagues
            and friends to register, please visit:
        </p>
        <p style='text-align: center;'>
            <code><a href='https://datascience.jpl.nasa.gov/aiworkshop'>https://datascience.jpl.nasa.gov/aiworkshop</a></code>
        </p>
        <p>
            If we don't hear from you by January 8, 2021, we will cancel your
            registration automatically.
        </p>
        <p>Thanks so much for your interest!</p>
        <p>
            Best regards,<br/>
            <a href='mailto:data-science-wg@jpl.nasa.gov'>2nd AI and Data Science Program Committee</a>
        </p>
    </body>
<html>
'''


_thanksPrologue = u'''<p>Whether you're joining us virtually or not, we appreciate that you took a moment
to let us know. Barring some computer glitch, we won't be bothering you again about this.</p>
<p>Here are the answers we've recorded in our system:</p>
'''

_thanksEpilogue = u'''<p>Thanks again!</p>'''

_noThanksMessage = u'''<p>Hey, could you go back to the confirmation form and answer it, please?</p>'''

_yesNo = (
    u"1|Yes, I'd still like to attend, online, February 9–11, 2021",
    u"0|No, I'd like to cancel my registration"
)

_institutions = (
    u'Ames Research Center',
    u'Armstrong Flight Research Center',
    u'Deep Space Network',
    u'George C. Marshall Space Flight Center',
    u'Goddard Space Flight Center',
    u'Independent Verification and Validation Facility',
    u'Jet Propulsion Laboratory',
    u'John C. Stennis Space Center',
    u'John F. Kennedy Space Center',
    u'John H. Glenn Research Center',
    u'Langley Research Center',
    u'Lyndon B. Johnson Space Center',
    u'Michoud Assembly Facility',
    u'Wallops Flight Facility',
    u'White Sands Test Facility',
    u'Other; please specify:'
)


class UTF8Recoder(object):
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
    def __iter__(self):
        return self
    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeReader(object):
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]
    def __iter__(self):
        return self


class UnicodeWriter(object):
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def publish(context, wfTool=None):
    if wfTool is None:
        wfTool = plone.api.portal.get_tool('portal_workflow')
    try:
        wfTool.doActionFor(context, action='publish')
        context.reindexObject()
    except WorkflowException:
        pass
    if IFolderish.providedBy(context):
        for itemID, subItem in context.contentItems():
            publish(subItem, wfTool)


def getConfirmationsFolder(context):
    if 'confirmations' in context.keys():
        return context['confirmations']

    confirmations = context[context.invokeFactory('Folder', 'confirmations')]
    confirmations.setTitle(u'Confirmations')
    confirmations.setDescription(u'Re-registration confirmation forms.')
    return confirmations


def makeCode():
    code = []
    for i in range(0, 4):
        code.append(random.choice(range(0, 10)))
    return u''.join(unicode(i) for i in code)


def createForms(context, priorRegistrantsFile):
    confirmations = getConfirmationsFolder(context)
    normalizer = getUtility(IIDNormalizer)
    for fn, ln, jobTitle, affiliation, other, replyTo, abstract, badge in UnicodeReader(priorRegistrantsFile):
        if fn == 'first-name': continue
        formID = normalizer.normalize(replyTo)
        if formID in confirmations.keys():
            _logger.warn(u'Already have a form for %s, not creating a new one', formID)
            continue
        _logger.warn(u'Creating form and related data for %s %s in %s', fn, ln, formID)
        form = confirmations[confirmations.invokeFactory('FormFolder', formID)]
        form.setTitle(u'{} {}'.format(fn, ln))
        form.setDescription(u'Registration confirmation form for {} {}.'.format(fn, ln))

        # Get rid of PloneFormGen's default fields
        plone.api.content.delete(objects=[form[i] for i in form.keys()])

        # Security
        code = makeCode()
        widget = form[form.invokeFactory('FormStringField', 'code')]
        widget.setTitle(u'Confirmation Code')
        widget.setDescription(u'Code from your email; this helps prevent others from answering for you.')
        widget.setFgsize(8)
        widget.setRequired(True)
        widget.fgTValidator.text = u"python:test(value=='{}', False, 'Confirmation code invalid')".format(code)

        # The main question: do you still wanna come?
        widget = form[form.invokeFactory('FormSelectionField', 'yesno')]
        widget.setTitle(u'Registration Confirmation')
        widget.setDescription(u'Are you still interested in attending the Second AI and Data Science Workshop, now being held online, February 9–11, 2021?')
        widget.setFgFormat(u'radio')
        widget.setFgVocabulary(_yesNo)
        widget.setRequired(True)

        # I just need my personal space
        widget = form[form.invokeFactory('FormLabelField', 'spacer')]
        widget.setTitle(u'\xa0')        # That's a NO-BREAK SPACE
        widget.setDescription(u'\xa0')  # That's a NO-BREAK SPACE

        # And the direction to take
        widget = form[form.invokeFactory('FormLabelField', 'flow')]
        widget.setTitle(u'↑ If you answered yes above …')
        widget.setDescription(u'… please confirm your details below ↓')

        # First name
        widget = form[form.invokeFactory('FormStringField', 'first-name')]
        widget.setTitle(u'First Name')
        widget.setDescription(u'Please confirm your first name.')
        widget.setFgStringValidator('isNotLinkSpam')
        widget.setFgDefault(fn)
        widget.setRequired(False)

        # Last name
        widget = form[form.invokeFactory('FormStringField', 'last-name')]
        widget.setTitle(u'Last Name')
        widget.setDescription(u'Please confirm your last name, surname, family name, etc.')
        widget.setFgStringValidator('isNotLinkSpam')
        widget.setFgDefault(ln)
        widget.setRequired(False)

        # Job title
        widget = form[form.invokeFactory('FormStringField', 'job-title')]
        widget.setTitle(u'Title')
        widget.setDescription(u'Please confirm your title, position, etc.')
        widget.setFgStringValidator('isNotLinkSpam')
        widget.setFgDefault(jobTitle)
        widget.setFgsize(40)
        widget.setRequired(False)

        # Affiliation
        widget = form[form.invokeFactory('FormSelectionField', 'affiliation')]
        widget.setTitle(u'Affiliation')
        widget.setDescription(u'Select your institution and/or affiliation.')
        widget.setFgFormat('flex')
        widget.setFgVocabulary(_institutions)
        widget.setFgDefault(affiliation)
        widget.setRequired(False)

        # Other affiliation
        widget = form[form.invokeFactory('FormStringField', 'other-affiliation')]
        widget.setTitle(u'Other Affiliation')
        widget.setDescription(u'If you selected "other" above.')
        widget.setFgStringValidator('isNotLinkSpam')
        widget.setFgDefault(other)
        widget.setFgsize(50)
        widget.setRequired(False)

        # And finally, the email address
        widget = form[form.invokeFactory('FormStringField', 'email')]
        widget.setTitle(u'Your E-Mail Address')
        widget.setDescription(u'An email address is required in order to contact you.')
        widget.setFgStringValidator('isEmail')
        widget.setFgDefault(replyTo)
        widget.setFgsize(60)
        widget.setRequired(False)

        # Thank you!
        widget = form[form.invokeFactory('FormThanksPage', 'thanks')]
        widget.setTitle(u'Thank You')
        widget.setDescription(u"You've got our gratitude for taking the time to respond.")
        widget.setShowAll(True)
        widget.setIncludeEmpties(True)
        widget.setThanksPrologue(_thanksPrologue)
        widget.setThanksEpilogue(_thanksEpilogue)
        widget.setNoSubmitMessage(_noThanksMessage)
        form.setThanksPage('thanks')

        # Save your answers and let us know by email
        widget = form[form.invokeFactory('FormSaveDataAdapter', 'response')]
        widget.setTitle(u'Response')
        widget.setDescription(u'Responses to the confirmation form from {} {}'.format(fn, ln))
        widget.setDownloadFormat(u'csv')
        widget.setUseColumnNames(True)
        widget = form[form.invokeFactory('FormMailerAdapter', 'mailer')]
        widget.setTitle(u'Mailer')
        widget.setDescription(u'Email notification from {} {}'.format(fn, ln))
        widget.setRecipient_name(u'Data Science Working Group')
        widget.setRecipient_email(_overseer)
        widget.setCc_recipients(_overseerAssistants)
        widget.setMsg_subject(u'Attendance confirmation (or cancelation) for {}'.format(replyTo))
        widget.setBody_pre(u'Confirmation (or cancelation) received for the previous registrant detailed below:')
        widget.setShowAll(True)
        widget.setIncludeEmpties(True)
        widget.setBody_type('html')
        form.setActionAdapter(('response', 'mailer'))

        # Add a Page where we can just store some info
        data = form[form.invokeFactory('Document', 'data')]
        data.setTitle(u'Data')
        data.setDescription(u'Data about the confirmation of {} {}'.format(fn, ln))
        data.setText(json.dumps({
            u'email': replyTo,
            u'notifications': [],
            u'answer': None,
            u'code': code,
            u'firstName': fn
        }, ensure_ascii=False))

    publish(confirmations)
    transaction.commit()


def sendEmail(context, mailer):
    data = json.loads(context['data'].getRawText())
    try:
        url = unicode(context.absolute_url()).replace(u'http://nohost/873/', u'https://datascience.jpl.nasa.gov/')
        msg = MIMEMultipart('alternative')
        msg.set_charset('utf8')
        msg['Subject'] = _emailSubject
        msg['From'] = u'"AI & Data Science Program Committee" <{}>'.format(_overseer)
        msg['Cc'] = u','.join(_overseerAssistants)
        plain = _textEmail.format(firstName=data[u'firstName'], confirmationURL=url, code=data[u'code'])
        html = _htmlEmail.format(firstName=data[u'firstName'], confirmationURL=url, code=data[u'code'])
        msg.attach(MIMEText(plain.encode('utf-8'), 'plain', 'UTF-8'))
        msg.attach(MIMEText(html.encode('utf-8'), 'html', 'UTF-8'))
        _logger.warn(u'📧 Sending email to %s', data[u'email'])
        mailer.sendmail(_overseer, data[u'email'], msg.as_string())
        data[u'notifications'].append(unicode(date.today().isoformat()))
    except smtplib.SMTPException:
        data[u'notifications'].append(u'{}-FAILED'.format(unicode(date.today().isoformat())))
    context['data'].setText(json.dumps(data))


def sendEmails(context, campaignNumber):
    confirmations = getConfirmationsFolder(context)
    forms = confirmations.getFolderContents()
    if len(forms) == 0:
        _logger.warn(u'😮 There are no forms in the confirmations folder; did you run ``forms`` first?')
        return
    registry = getUtility(IRegistry)
    mailer = smtplib.SMTP(registry[u'plone.smtp_host'], registry[u'plone.smtp_port'])
    try:
        for formBrain in forms:
            form = formBrain.getObject()
            data = json.loads(form['data'].getRawText())
            if data['answer'] is not None:
                _logger.info(u'😃 Registrant %s has already responded: answer = %r', data['answer'])
                continue
            if len(data['notifications']) < campaignNumber:
                sendEmail(form, mailer)
                time.sleep(_interEmailWait)
    finally:
        mailer.quit()


def tabulate(context):
    forms = getConfirmationsFolder(context).getFolderContents()
    for formBrain in forms:
        form = formBrain.getObject()
        data = json.loads(form['data'].getRawText())
        if data['answer'] is not None:
            # We already have an answer, so skip it
            _logger.info(u'✓ We have a recorded answer for %s already', data['email'])
            continue
        try:
            response = next(UnicodeReader(StringIO(form['response'].getSavedFormInputForEdit())))[RESPONSE_COLUMN] == u'1'
            _logger.info(u'🤨 Got a response %r for %s, recording it', response, data['email'])
            data['answer'] = response
            form['data'].setText(json.dumps(data))
        except StopIteration:
            _logger.info(u'🤷‍♀️ No answer for %s; maybe next time', data['email'])
            pass


def report(context):
    forms = getConfirmationsFolder(context).getFolderContents()
    ballot = {
        True:  u'attending',
        False: u'canceled',
        None:  u'none'
    }
    writer = UnicodeWriter(sys.stdout)
    writer.writerow((u'Email', u'Affiliation', u'Other Affiliation', u'Code', u'Response', u'Notifications'))
    for formBrain in forms:
        form = formBrain.getObject()
        data = json.loads(form['data'].getRawText())

        response = data[u'answer']
        if response is not None:
            affiliation = next(UnicodeReader(StringIO(form['response'].getSavedFormInputForEdit())))[AFFILIATION_COLUMN]
            other = next(UnicodeReader(StringIO(form['response'].getSavedFormInputForEdit())))[OTHER_COLUMN]
        else:
            affiliation = form['affiliation'].getFgDefault().decode('utf-8')
            other = form['other-affiliation'].getFgDefault().decode('utf-8')

        writer.writerow((
            data[u'email'], affiliation, other, data[u'code'], ballot[data[u'answer']], u';'.join(data[u'notifications'])
        ))
    sys.stdout.flush()


def main(argv):
    try:
        _logger.warn(u'🏃‍♀️ Here we go')
        global app
        parser = argparse.ArgumentParser(description=u'Handle workshop forms and reminders')
        parser.add_argument(
            '-r', '--rm', default=False, action='store_true',
            help=u'⚠️ Remove all confirmation data; WARNING! This is used only for development. Have backups!'
        )
        parser.add_argument(
            '-c', '--csv', metavar=u'FILE', default=u'registrants.csv', type=file,
            help=u'Create forms for registrants in FILE (default %(default)s)'
        )
        parser.add_argument(
            '-n', '--number', default=1, type=int,
            help=u'Send email campaign NUMBER (default %(default)d)'
        )
        parser.add_argument('mode', choices=['forms', 'tabulate', 'email', 'report'], help=u'What to do')
        args = parser.parse_args(argv[1:])

        if '873' not in app.keys():
            raise KeyError(u'Portal 873 not found; is this being run with the right database?')
        portal = app['873']
        if 'aiworkshop' not in portal.keys():
            raise KeyError(u'Workshop «aiworkshop» folder not found; is this being run with the right database?')
        workshop = portal['aiworkshop']

        if args.rm:
            _logger.warn(u'🛑 STOP! This is dangerous; dropping into debugger; you know what you doing')
            import pdb
            pdb.set_trace()
            confirmations = plone.api.content.get(path='/aiworkshop/confirmations')
            if confirmations is not None:
                plone.api.content.delete(confirmations)

        if args.mode == 'forms':
            createForms(workshop, args.csv)
        elif args.mode == 'email':
            tabulate(workshop)
            sendEmails(workshop, args.number)
        elif args.mode == 'tabulate':
            tabulate(workshop)
        elif args.mode == 'report':
            tabulate(workshop)
            report(workshop)
        plone.api.portal.get_tool('portal_catalog').clearFindAndRebuild()
        transaction.commit()

    except Exception as ex:
        logging.exception(u'Well this sucks: %s', unicode(ex))
        return False
    return True


if __name__ == '__main__':
    # The [2:] works around plone.recipe.zope2instance-4.2.6's lame bin/interpreter script issue
    sys.exit(0 if main(sys.argv[2:]) is True else -1)
