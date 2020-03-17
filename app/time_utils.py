from datetime import datetime, time, timedelta
from pytz import timezone
import pytz

from app import db
from app.models import TimeZone
from app.timezone import USTimeZone

TIME_ZONES = [ 
    (-5, "Eastern", "EST", "EDT"),
    (-6, "Central", "CST", "CDT"),
    (-7, "Mountain", "MST", "MDT"),
    (-8, "Pacific", "PST", "PDT"),
    (-10, "Hawaiian", "HST", "HADT")
]

def add_timezone_to_database(std_offset, std_name, std_abbr, dst_abbr):
    """Add time zones to the database from the flask shell.

    Args:
        std_offset: An integer representing the offset in hours from UTC.
        std_name: A string representing the long form name of the timezone.
        std_abbr: A string representing the abbreviation of the timezone.
        dst_sbbr: A string representing the abbreviation of the timezone during daylight savings time.
    """
    # Query TimeZone table to make sure the record doesn't already exist
    if TimeZone.query.filter_by(std_name=std_name).first() != None:
        print('This time zone is already in the database.') 
    else:
        time_zone = TimeZone(std_offset=std_offset, std_name=std_name, std_abbr=std_abbr, dst_abbr=dst_abbr)
        db.session.add(time_zone)
        db.session.commit()

def print_timezones_to_terminal():
    """Print time zones to flask shell"""
    time_zones = TimeZone.query.all()
    for time_zone in time_zones:
        print(f'<"{time_zone.std_name}" | {time_zone.std_offset} | "{time_zone.std_abbr}" | "{time_zone.dst_abbr}">')

def import_from_list():
    for tz in TIME_ZONES:
        add_timezone_to_database(tz[0], tz[1], tz[2], tz[3])


def get_user_tz_obj(user_query_obj):
    """Converts query data to USTimeZone Object."""
    return USTimeZone(user_query_obj.time_zone.std_offset, \
                        user_query_obj.time_zone.std_name, \
                        user_query_obj.time_zone.std_abbr, \
                        user_query_obj.dst_active, \
                        user_query_obj.time_zone.dst_abbr)




# In use
def is_dst(tz):
    now = datetime.now(tz=tz)
    if now.timetuple().tm_isdst == 1:
        return True
    elif now.timetuple().tm_isdst == 0:
        return False
    else:
        pass
        # SHOULD RAISE AN ERROR IF DST INFO IS NOT SET!

def get_user_tz(tz_name):
    # TZ name must be in TZ database name (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
    return timezone(tz_name)

def time_to_datetime(d, t):
    """Combines a date and time object to return a datetime object"""
    return datetime(d.year, d.month, d.day, t.hour, t.minute)

def datetime_to_time(dt):
    return time(dt.hour, dt.minute)