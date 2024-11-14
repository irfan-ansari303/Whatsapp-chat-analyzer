import re
import pandas as pd
#this function the take the string data and return the data data frame
def preproces(data):
    # this is used to change the text into regex expression this can be also done by the webiste regular expression 101
    # d{1,2} which means may contain 1 or 2 char:
    # \s it denote the spaces
    pattern = '\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s[ap]m\s-\s'
    # extract all the messages
    messages = re.split(pattern, data)[1:]
    # extract all the date
    dates = re.findall(pattern, data)

    # Step 1: Clean up the message_date column by removing ' - '
    cleaned_dates = [date.strip(' -') for date in dates]

    # Step 2: Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': cleaned_dates})

    # Step 3: Convert to datetime
    df["message_date"] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p')

    # Step 4: Rename column
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # seprate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            # if : is not found the say it is gropt notification
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # extract the year from the date
    df['year'] = df['date'].dt.year

    # extract the month name
    df['month'] = df['date'].dt.month_name()

    # extract the day from the date
    df['day'] = df['date'].dt.day

    # ectrat hour and minute from the the date
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df