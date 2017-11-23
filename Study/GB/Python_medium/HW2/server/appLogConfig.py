import logging
import sys
import datetime

now = datetime.datetime.now()

fname = 'Logs/%s-%s-%s.log' % (now.day, now.month, now.year)

format = logging.Formatter('%(levelname)-10s %(asctime)s %(message)s')


crit_hand = logging.StreamHandler(sys.stderr)
crit_hand.setLevel(logging.CRITICAL)
crit_hand.setFormatter(format)


applog_hand = logging.FileHandler(fname)
applog_hand.setFormatter(format)

app_log = logging.getLogger('app')
app_log.setLevel(logging.INFO)
app_log.addHandler(applog_hand)
#app_log.addHandler(crit_hand)


logging.getLogger('app.net').setLevel(logging.ERROR)

