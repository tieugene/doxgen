# -*- coding: utf-8 -*-
"""
Utility module
"""

# 1. system
import datetime
import sys
# 2. 3rd party
# 3. django


def eprint(s: str):
    print(s, file=sys.stderr)


class ShortUUIDConverter:
    regex = '[0-9A-Z]{32}'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return '%s' % value


def date2str(data, name):
    """
    @param data:dict
    @param name:str
    """
    data[name] = data[name].strftime('%d.%m.%Y') if data[name] else ''


def str2date(data, name):
    """
    @param data:dict
    @param name:str
    """
    data[name] = datetime.datetime.strptime(data[name], '%d.%m.%Y').date() if data[name] else None

def chk_inn(s):
    """
    Check INN
    @param s:str - INN (e.g. 1234567894 or 123456789093)
    @return int - errcode:
        0 - ok
        1 - non-digits
        2 - wrong len
        3 - wrong check code
    """
    k10 = (2, 4, 10, 3, 5, 9, 4, 6, 8)
    k11 = (7, 2, 4, 10, 3, 5, 9, 4, 9, 8)
    k12 = (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)

    def chk_cs(s, k):
        """
        Calculates cs
        @param s:str - inn
        @param k:tuple - koefficients
        @return boolean - CS ok
        """
        sum = 0
        l = len(k)
        for i in range(l):
            sum += int(s[i]) * k[i]
        # print ((sum%11)%10)%11
        return ((sum % 11) % 10) % 11 == int(s[l])

    if not s.isdigit():
        return 1
    if len(s) == 10:
        return 0 if chk_cs(s, k10) else 3
    elif len(s) == 12:
        return 0 if (chk_cs(s, k11) and chk_cs(s, k12)) else 3
    return 2


def chk_ogrn(s):
    """
    Check OGRN
    @param s:str - OGRN (e.g. 5067847579135)
    @return int - errcode:
        0 - ok
        1 - non-digits
        2 - wrong len
        3 - wrong check code
    """
    if not s.isdigit():
        return 1
    if len(s) != 13:
        return 2
    if (int(s[:12]) % 11) % 10 != int(s[12]):
        return 3
    return 0
