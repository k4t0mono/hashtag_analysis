#!/usr/bin/env python
# coding: utf-8

# Gustavo Dimas Franco Freitas


import sys

class Progress:

    def __init__(self, total, msg):
        self._progressTotal = total
        self._progressSteps = 0
        self._progressMsg = msg
        self._progress(0, total, msg)

    def progressStep(self):
        self._progressSteps += 1
        self._progress(self._progressSteps, self._progressTotal, self._progressMsg)
    
    def progressMultiple(self, n):
        self._progressSteps += n
        self._progress(self._progressSteps, self._progressTotal, self._progressMsg)

    def _progress(self, count, total, status=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
        sys.stdout.flush()
