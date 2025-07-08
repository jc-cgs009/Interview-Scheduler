def get_modified_date_format(date):
    month_data = {1:'January',
                 2:'February',
                 3:'March',
                 4:'April',
                 5:'May',
                 6:'June',
                 7:'July',
                 8:'August',
                 9:'September',
                 10:'October',
                 11:'November',
                 12:'December'
                 }
    y, m, d = date.split('-')

    return f"{month_data[int(m)]} {d} {y}"

