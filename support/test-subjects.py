#!/usr/bin/env python

import csv, codecs, cStringIO, random


_middleNames = [
    u'Amelia',
    u'Blue',
    u'Brighton',
    u'Brock',
    u'Brooke',
    u'Coleen',
    u'Conrad',
    u'Drake',
    u'Gavin',
    u'Gregory',
    u'Haiden',
    u'Hope',
    u'Jackson',
    u'Javan',
    u'Jordan',
    u'Julian',
    u'Kalan',
    u'Kerrie',
    u'Laurie',
    u'Louisa',
    u'Pink',
    u'Rory',
    u'Rupert',
    u'Rylie',
    u'Silvia',
]
_jobTitles = [
    u'Drink Dissemination Officer',
    u'Bird Sexer',
    u'Digital Overlord',
    u'Retail Jedi',
    u'Wizard Of Lightbulb Moments',
    u'Chief Chatter',
    u'Animal Colorist',
    u'Problem Wrangler',
    u'Twister Brother',
    u'Direct Mail Demigod',
    u'Marketing Rock Star',
    u'Light Bender',
    u'Brand Evangelist',
    u'Cooper',
    u'Potter',
    u'Shipwright',
    u'Associate Vice President',
    u'Hair Boiler',
    u'Cheese Sprayer',
]


class UTF8Recoder(object):
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeWriter(object):
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
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


def main():
    with open('large-scale.csv', 'w') as f:
        writer = UnicodeWriter(f)
        # Header
        writer.writerow([
            'first-name', 'last-name' ,' title-1', 'affiliation', 'other-affiliation', 'replyto',
            'accepted-abstract', 'badge-nickname'
        ])
        # People
        for i in range(1, 101):
            name = random.choice(_middleNames)
            writer.writerow([
                u'Sean ' + name,
                u'Kelly',
                random.choice(_jobTitles),
                u'Jet Propulsion Laboratory',
                u'',
                u'sean.c.kelly+test-{}-{}@gmail.com'.format(name.lower(), i),
                u'False',
                name
            ])


if __name__ == '__main__':
    main()