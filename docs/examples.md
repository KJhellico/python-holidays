# Additional Examples

## Simplest example possible

``` python
>>> from datetime import date
>>> import holidays
>>> date(2014, 1, 1) in holidays.US()
True
>>> date(2014, 1, 2) in holidays.US()
False
```

!!! tip "Tip"
    Don't do this! It is not efficient because it is initializing a new Holiday object and
    generating a list of all the holidays in 2014 during each comparison.

It is more efficient to create the object only once:

``` python
>>> us_holidays = holidays.US()
>>> date(2014, 1, 1) in us_holidays
True
>>> date(2014, 1, 2) in us_holidays
False
```

You can use the `country_holidays` or `financial_holidays` functions to create the object
using a string with the country code:

``` python
>>> us_holidays = holidays.country_holidays('US')
>>> nyse_holidays = holidays.financial_holidays('NYSE')
```

Use `years` parameter to populate the holidays years you are interested in:

``` python
>>> us_holidays = holidays.US(years=2020)  # US 2020 holidays
>>> us_holidays = holidays.US(years=range(2020, 2026))  # US 2020-2025 holidays
```

Let's print out the holidays in 2014 specific to California, USA:

``` python
>>> for date, name in sorted(holidays.US(subdiv='CA', years=2014).items()):
>>>     print(date, name)
2014-01-01 New Year's Day
2014-01-20 Martin Luther King Jr. Day
2014-02-15 Susan B. Anthony Day
2014-02-17 Washington's Birthday
2014-03-31 Cesar Chavez Day
2014-05-26 Memorial Day
2014-07-04 Independence Day
2014-09-01 Labor Day
2014-11-11 Veterans Day
2014-11-27 Thanksgiving
2014-11-28 Day After Thanksgiving
2014-12-25 Christmas Day
```

So far we've only checked holidays in 2014, so that's the only year the Holidays object has
generated:

``` python
>>> us_holidays.years
set([2014])
>>> len(us_holidays)
10
```

## Expand parameter

Because, by default, the `expand` parameter is `True`, the Holiday object will calculate and add
holidays for other years when they are required:

``` python
>>> date(2013, 1, 1) in us_holidays
True
>>> us_holidays.years
set([2013, 2014])
>>> len(us_holidays)
20
```

If we change the `expand` parameter to `False` the Holiday object will no longer add holidays from
new years:

``` python
>>> us_holidays.expand = False
>>> date(2012, 1, 1) in us_holidays
False
>>> us_holidays.expand = True
>>> date(2012, 1, 1) in us_holidays
True
```

## Observed parameter

January 1st, 2012 fell on a Sunday, so the statutory holiday was observed on the 2nd. By default,
the `observed` param is `True`, so the holiday list will include January 2nd, 2012 as a holiday:

``` python
>>> date(2012, 1, 1) in us_holidays
True
>>> us_holidays[date(2012, 1, 1)]
"New Year's Day"
>>> date(2012, 1, 2) in us_holidays
True
>>> us_holidays.get(date(2012 ,1, 2))
"New Year's Day (observed)"
```

The values of `observed` and `expand` can be changed on the fly and the holiday list will be
adjusted accordingly:

``` python
>>> us_holidays.observed = False
>>> date(2012, 1, 2) in us_holidays
False
us_holidays.observed = True
>>> date(2012, 1, 2) in us_holidays
True
```

## Language support

To change the language translation, you can set the language explicitly.

``` python
>>> for dt, name in sorted(holidays.ES(years=2023, language="es").items()):
>>>     print(dt, name)
2023-01-06 Epifanía del Señor
2023-04-07 Viernes Santo
2023-05-01 Fiesta del Trabajo
2023-08-15 Asunción de la Virgen
2023-10-12 Fiesta Nacional de España
2023-11-01 Todos los Santos
2023-12-06 Día de la Constitución Española
2023-12-08 Inmaculada Concepción
2023-12-25 Natividad del Señor
```

## Holiday categories support

To get a list of other categories holidays (for countries that support them):

``` python
>>> for dt, name in sorted(holidays.BE(years=2023, language="en_US", categories=BANK).items()):
>>>     print(dt, name)
2023-04-07 Good Friday
2023-05-19 Friday after Ascension Day
2023-12-26 Bank Holiday

>>> for dt, name in sorted(holidays.BE(years=2023, language="en_US", categories=(BANK, PUBLIC)).items()):
>>>     print(dt, name)
2023-01-01 New Year's Day
2023-04-07 Good Friday
2023-04-09 Easter Sunday
2023-04-10 Easter Monday
2023-05-01 Labor Day
2023-05-18 Ascension Day
2023-05-19 Friday after Ascension Day
2023-05-28 Whit Sunday
2023-05-29 Whit Monday
2023-07-21 National Day
2023-08-15 Assumption Day
2023-11-01 All Saints' Day
2023-11-11 Armistice Day
2023-12-25 Christmas Day
2023-12-26 Bank Holiday
```

## Working day-related calculations

To check if the specified date is a working day:

``` python
>>> us_holidays = holidays.US(years=2024)  # Weekends in the US are Saturday and Sunday.
>>> us_holidays.is_working_day("2024-01-01")  # Monday, New Year's Day.
False
>>> us_holidays.is_working_day("2024-01-02")  # Tuesday, ordinary day.
True
>>> us_holidays.is_working_day("2024-01-06")  # Saturday, ordinary day.
False
>>> us_holidays.is_working_day("2024-01-15")  # Monday, Martin Luther King Jr. Day.
False
```

To find the nth working day after the specified date:

``` python
>>> us_holidays.get_nth_working_day("2024-12-20", 5)
datetime.date(2024, 12, 30)
```

Here we calculate the 5th working day after December 20, 2024. Working days are 23 (Mon), 24 (Tue),
26 (Thu), 27 (Fri), 30 (Mon); 21-22, 28-29 - weekends, 25 - Christmas Day.

To calculate the number of working days between two specified dates:

``` python
>>> us_holidays.get_working_days_count("2024-04-01", "2024-06-30")
63
```

Here we calculate the number of working days in Q2 2024.

## Getting the closest (next or previous) holiday

You can fetch next or previous holiday for a target date of your selected calendar. The function
returns found holiday's date and name excluding the target date.

Get the next holiday for the current date:

``` python
>>> us_holidays = holidays.US(years=2025)
>>> us_holidays.get_closest_holiday()
(datetime.date(2025, 1, 20), 'Martin Luther King Jr. Day')
```

Get the previous holiday for the current date:

``` python
>>> us_holidays = holidays.US(years=2025)
>>> us_holidays.get_closest_holiday(direction="backward")
(datetime.date(2025, 1, 1), "New Year's Day")
```

Get the next holiday for a specific target date:

``` python
>>> us_holidays = holidays.US(years=2025)
>>> us_holidays.get_closest_holiday("2025-02-01")
(datetime.date(2025, 2, 17), "Washington's Birthday")
```

Get the previous holiday for a specific target date:

``` python
>>> us_holidays = holidays.US(years=2025)
>>> us_holidays.get_closest_holiday("2025-02-01", direction="backward")
(datetime.date(2025, 1, 20), 'Martin Luther King Jr. Day')
```

If the closest holiday cannot be found, `None` is returned.

``` python
>>> print(us_holidays.get_closest_holiday("2100-12-31"))
None
>>> print(us_holidays.get_closest_holiday("1777-01-01", direction="backward"))
None
```

## Date from holiday name

Holidays can be retrieved using their name too. `get_named` receives a string and returns a list
of holidays matching it (even partially, with case-insensitive check):

``` python
>>> us_holidays = holidays.UnitedStates(years=2020)
>>> sorted(us_holidays.get_named('day'))
[datetime.date(2020, 1, 1), datetime.date(2020, 1, 20),
datetime.date(2020, 2, 17), datetime.date(2020, 5, 25),
datetime.date(2020, 7, 3), datetime.date(2020, 7, 4),
datetime.date(2020, 9, 7), datetime.date(2020, 10, 12),
datetime.date(2020, 11, 11), datetime.date(2020, 12, 25)]
```

## Additions

Holiday objects can be added together, and the resulting object will generate the holidays from
all the initial objects:

``` python
>>> north_america = holidays.CA() + holidays.US() + holidays.MX()
>>> north_america.get('2014-07-01')
"Canada Day"
>>> north_america.get('2014-07-04')
"Independence Day"
```

The other form of addition is also available:

``` python
>>> north_america = holidays.CA()
>>> north_america += holidays.US()
>>> north_america += holidays.MX()
>>> north_america.country
['CA', 'US', 'MX']
```

We can even get a set of holidays that include all the subdivision-specific holidays using
the built-in `sum` function:

``` python
>>> a = sum([holidays.CA(subdiv=x) for x in holidays.CA.subdivisions])
>>> a.subdiv
['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT']
```

## Creating custom holidays (or augmenting existing ones with private ones)

Sometimes we may not be able to use the official federal statutory holiday list in our code. Let's
pretend we work for a company that does not include New Year's Day as a statutory holiday but does
include "Ninja Turtle Day" on July 13th. We can create a new class that inherits the US (please
note the base class import path) and the only method we need to override is `_populate`:

``` python
>>> from holidays.countries import US
>>> class CorporateHolidays(US):
>>>     def _populate(self, year):
>>>         # Populate the holiday list with the default US holidays.
>>>         super()._populate(year)
>>>         # Remove New Year's Day.
>>>         self.pop_named("New Year's Day")
>>>         # Add Ninja Turtle Day.
>>>         self._add_holiday_jul_13("Ninja Turtle Day")
>>> date(2014, 1, 1) in holidays.country_holidays(country="US")
True
>>> date(2014, 1, 1) in CorporateHolidays()
False
>>> date(2014, 7, 13) in holidays.country_holidays(country="US")
False
>>> date(2014, 7, 13) in CorporateHolidays()
True
```

We can also inherit from the HolidayBase class which has an empty `_populate` method so we start
with no holidays and must define them all ourselves. This is how we would create a holidays class
for a country that is not supported yet:

``` python
>>> class NewCountryHolidays(holidays.HolidayBase):
>>>     def _populate(self, year):
>>>         self[date(year, 1, 2)] = "Some Federal Holiday"
>>>         self[date(year, 2, 3)] = "Another Federal Holiday"
>>> hdays = NewCountryHolidays()
```

We can use the `self._add_holiday_*` methods to specify holidays:

``` python
>>> class MovingHolidays(holidays.HolidayBase):
>>>     def _populate(self, year):
>>>         super()._populate(year)
>>> 
>>>         self._add_holiday_3rd_mon_of_jan("Martin Luther King Jr. Day")
>>>         self._add_holiday_last_fri_of_feb("Last Friday of February")
>>>         self._add_holiday_1st_mon_before_dec_25("Monday before Christmas")
>>> moving = MovingHolidays(years=2025)
```

The supported `_add_holiday_*` patterns are:

- `_add_holiday_<month>_<day>` for fixed-date holidays
- `_add_holiday_<last/nth>_<weekday>_of_<month>` for holidays that occur on a specific weekday of a month
- `_add_holiday_<n>_day(s)_<past/prior>_<last/nth>_<weekday>_of_<month>`
- `_add_holiday_<nth>_<weekday>_<before/from>_<month>_<day>`
- `_add_holiday_<n>_day(s)_<prior/past>_easter` (requires inheritance from `ChristianHolidays` holidays group)

Some examples of these methods would be:

- `_add_holiday_jan_1`
- `_add_holiday_last_mon_of_feb`
- `_add_holiday_1st_thu_of_nov`
- `_add_holiday_2_days_prior_2nd_mon_of_jan`
- `_add_holiday_1_day_past_last_fri_of_dec`
- `_add_holiday_1st_tue_from_dec_25`
- `_add_holiday_2nd_fri_before_jun_15`
- `_add_holiday_2_days_prior_easter` (make sure to derive from `ChristianHolidays`)
- `_add_holiday_1_day_past_easter` (make sure to derive from `ChristianHolidays`)

You can find the implementation details at `HolidayBase.__getattr__` method.

We can also include holidays for a subdivision (e.g. prov/state) in our new class:

``` python
>>> class NewCountryHolidays(holidays.HolidayBase):
>>>     def _populate(self, year):
>>>         # Set default subdiv if not provided
>>>         if self.subdiv == None:
>>>             self.subdiv = 'XX'
>>>         self[date(year, 1, 2)] = "Some Federal Holiday"
>>>         if self.subdiv == 'XX':
>>>             self[date(year, 2, 3)] = "Special XX subdiv-only holiday"
>>>         if self.subdiv == 'YY':
>>>             self[date(year, 3, 4)] = "Special YY subdiv-only holiday"
>>> hdays = NewCountryHolidays()
>>> hdays = NewCountryHolidays(subdiv='XX')
```

If you write the code necessary to create a holiday class for a country not currently supported,
please contribute your code to the project!

Perhaps you just have a list of dates that are holidays and want to turn them into a Holiday class
to access all the useful functionality. You can use the `append()` method which accepts a
dictionary of `{date: name}` pairs, a list of dates, or even singular date/string/timestamp
objects:

``` python
>>> custom_holidays = holidays.HolidayBase()
>>> custom_holidays.append(['2015-01-01', '07/04/2015'])
>>> custom_holidays.append(date(2015, 12, 25))
```

## Add years to an existing Holiday object

Because the Holiday class is a subclass of dictionary, we use the
[update()](https://docs.python.org/3/library/stdtypes.html?highlight=update#dict.update)
method to add years to an existing holiday object:

``` python
>>> from holidays import country_holidays
>>> us_holidays = country_holidays('US', years=2020)
# to add new years of holidays to the object:
>>> us_holidays.update(country_holidays('US', years=2021))
```

## Other ways to specify the country

Each country has two class names that can be called in addition to the alpha-2 ISO code: its
3-digit ISO code and an internal class name.

``` python
>>> holidays.USA() == holidays.US()
True
>>> holidays.UnitedStates() == holidays.US()
True
```

## Generate iCalendar content and export to `.ics`

[ICalExporter][holidays.ical.ICalExporter] facilitates the creation and export of iCalendar files
in compliance with [RFC 5545](https://datatracker.ietf.org/doc/html/rfc5545).

``` python
>>> from holidays import country_holidays
>>> from holidays.ical import ICalExporter
>>> us_holidays = country_holidays('US', years=2020)
# Initializes the iCalendar exporter.
>>> exporter = ICalExporter(us_holidays)
```

To create iCalendar content, use `generate`.

``` python
>>> from holidays import country_holidays
>>> from holidays.ical import ICalExporter
>>> th_holidays = country_holidays('TH', years=2024)
>>> exporter = ICalExporter(th_holidays)
>>> ical_content = exporter.generate()
# Thailand's Songkran Festival (April 13th–15th) should be counted as a single
# VEVENT with a duration of three days.
>>> ical_content.count("SUMMARY:วันสงกรานต์\r\n")
1
>>> "DURATION:P3D\r\n" in ical_content
True
# Adds ";LANGUAGE=" to SUMMARY too.
>>> exporter = ICalExporter(th_holidays, show_language=True)
>>> ical_content = exporter.generate()
>>> ical_content.count("SUMMARY;LANGUAGE=th:วันสงกรานต์\r\n")
1
```

!!! tip "Tip"
    Although the iCalendar specification supports a wide range of language formats as outlined
    in [RFC 5646](https://datatracker.ietf.org/doc/html/rfc5646), the Holidays object requires
    that the `language` attribute adhere to the [ISO 639-1 or
    ISO 639-2](https://www.loc.gov/standards/iso639-2/php/code_list.php) language codes,
    such as `en` or `pap-AW`.

    Additionally, if no `language` is specified for a holiday, but a `default_language` is set
    for the Holiday object, the default language will be used instead.

``` python
>>> from holidays import country_holidays
>>> from holidays.ical import ICalExporter
>>> cn_holidays = country_holidays("CN", years=2024, language="en_US")
>>> jp_holidays = country_holidays("JP", years=2024, language="en_US")
>>> kr_holidays = country_holidays("KR", years=2024, language="en_US")
>>> east_asia_holidays = cn_holidays + jp_holidays + kr_holidays
>>> ical_content = ICalExporter(east_asia_holidays).generate()
# Even with the combined China-Japan-Korea calendar, there should be only one
# 'New Year's Day' VEVENT.
>>> ical_content.count("SUMMARY:New Year's Day\r\n")
1
```

To export to `.ics` format, use `save_ics`.

``` python
>>> from pathlib import Path
>>> from holidays import financial_holidays
>>> from holidays.ical import ICalExporter
# Export the NYSE_2024_calendar.ics file in the current directory
>>> nyse_exporter = ICalExporter(financial_holidays("NYSE", years=2024))
>>> nyse_exporter.save_ics(file_path="NYSE_2024_calendar.ics")
# Export the NYSE_2024_calendar.ics file to MS Windows' Downloads folder instead.
>>> downloads_path = Path.home() / "Downloads"
>>> nyse_exporter.save_ics(file_path=str(downloads_path / "NYSE_2024_calendar.ics"))
```

For advanced features and customization of the exported `.ics` output, consider using
the [icalendar](https://github.com/collective/icalendar) package.
