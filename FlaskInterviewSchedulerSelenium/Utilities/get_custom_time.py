def get_modified_time_format(time):
    h, m = time.split(':')
    prefix_ = 'am'
    h = int(h)
    if h > 12:
        h -= 12
        prefix_ = 'pm'
    elif h == 12:
        prefix_ = 'pm'

    return f"{h}:{m}{prefix_}"