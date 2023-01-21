#  python-holidays
#  ---------------
#  A fast, efficient Python library for generating country, province and state
#  specific sets of holidays on the fly. It aims to make determining whether a
#  specific date is a holiday as fast and flexible as possible.
#
#  Authors: dr-prodigy <dr.prodigy.github@gmail.com> (c) 2017-2023
#           ryanss <ryanssdev@icloud.com> (c) 2014-2017
#  Website: https://github.com/dr-prodigy/python-holidays
#  License: MIT (see LICENSE file)

from datetime import date, timedelta

from dateutil.easter import EASTER_ORTHODOX, easter

from holidays.constants import JAN, MAR, APR, MAY, AUG, OCT, DEC
from holidays.holiday_base import HolidayBase


class Cyprus(HolidayBase):
    """
    https://en.wikipedia.org/wiki/Public_holidays_in_Cyprus
    """

    country = "CY"

    def _populate(self, year):
        super()._populate(year)

        easter_date = easter(year, method=EASTER_ORTHODOX)

        # New Years
        self[date(year, JAN, 1)] = "Πρωτοχρονιά [New Year's Day]"

        # Epiphany
        self[date(year, JAN, 6)] = "Θεοφάνεια [Epiphany]"

        # Clean Monday
        self[
            easter_date + timedelta(days=-48)
        ] = "Καθαρά Δευτέρα [Clean Monday]"

        # Greek Independence Day
        self[
            date(year, MAR, 25)
        ] = "Εικοστή Πέμπτη Μαρτίου [Greek Independence Day]"

        # Cyprus National Day
        self[date(year, APR, 1)] = "1η Απριλίου [Cyprus National Day]"

        # Good Friday
        self[
            easter_date + timedelta(days=-2)
        ] = "Μεγάλη Παρασκευή [Good Friday]"

        # Easter Sunday
        self[easter_date] = "Κυριακή του Πάσχα [Easter Sunday]"

        # Easter Monday
        self[
            easter_date + timedelta(days=+1)
        ] = "Δευτέρα του Πάσχα [Easter Monday]"

        # Labour Day
        self[date(year, MAY, 1)] = "Εργατική Πρωτομαγιά [Labour day]"

        # Monday of the Holy Spirit
        self[
            easter_date + timedelta(days=+50)
        ] = "Δευτέρα του Αγίου Πνεύματος [Monday of the Holy Spirit]"

        # Assumption of Mary
        self[date(year, AUG, 15)] = "Κοίμηση της Θεοτόκου [Assumption of Mary]"

        # Cyprus Independence Day
        self[
            date(year, OCT, 1)
        ] = "Ημέρα Ανεξαρτησίας της Κύπρου [Cyprus Independence Day]"

        # Ochi Day
        self[date(year, OCT, 28)] = "Ημέρα του Όχι [Ochi Day]"

        # Christmas Eve
        self[date(year, DEC, 24)] = "Παραμονή Χριστουγέννων [Christmas Eve]"

        # Christmas
        self[date(year, DEC, 25)] = "Χριστούγεννα [Christmas]"

        # Day after Christmas
        self[
            date(year, DEC, 26)
        ] = "Δεύτερη μέρα Χριστουγέννων [Day after Christmas]"


class CY(Cyprus):
    pass


class CYP(Cyprus):
    pass
