from datetime import datetime, date, time, timedelta
from pytz import timezone
import pytz

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

def local_to_utc(loc_time, tz):
    """converts localized time to utc time

    Assumes that the date is localized date of execution.

    Args:
        time: Time Object as unaware time. 
        tz: pytz Object containing localized timezone information.
    """
    loc_datetime = tz.localize(time_to_datetime(date.today(), loc_time))
    utc_datetime = loc_datetime.astimezone(timezone('UTC'))
    
    return datetime_to_time(utc_datetime)

def utc_to_local(utc_time, tz):
    """Converts utc time to localized time

    Assumes that date is localized date of execution.

    Args:
        time: Time Object as unaware utc time
        tz: pytz Object containing localized timezone information.
    """
    utc_current_datetime = datetime.utcnow()
    utc_current_date = date(utc_process_datetime.year, utc_process_datetime.month, utc_process_datetime.day)
    utc_tz = timezone('UTC')
    utc_datetime = utc_tz.localize(time_to_datetime(utc_process_date, utc_time))
    
    return utc_datetime.astimezone(tz)
    

    
