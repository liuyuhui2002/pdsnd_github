import time
import pandas as pd

CITY_DATA = {'Chicago': 'chicago.csv',
             'New York': 'new_york_city.csv',
             'Washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("\nHello! Let's explore some US bikes hare data!")

    # get user input for city (chicago, new york city, washington).
    cities = ['Chicago', 'New York', 'Washington']
    city = input("\nWould you like to see the data for Chicago, New York, or Washington?\n").title()
    while city not in cities:
        city = input("The city name you enter is incorrect, please try again. "
                     'Please enter "Chicago", "New York", or "Washington".\n').title()

    # ask user to select time filter (month, day, both or none)
    time_filters = ['month', 'day', 'both', 'none']
    time_filter = input('\nWould you like to filter the data by month, day, both, or not at all? '
                        'Type "none" for no time filter.\n').lower()
    while time_filter not in time_filters:
        time_filter = input(
            'The filter you enter is incorrect. Please enter "month", "day", "both", or "none".\n').lower()

    # define months and days lists
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    # get user input for month (january, february, ... , june)
    if time_filter == 'month':
        month = input("\nWhich month? January, February, March, April, May, June?\n").title()
        while month not in months:
            month = input("The month you enter is incorrect, please try again. "
                          'Please enter "January", "February", "March", "April", "May", "June".\n').title()

        # set day to None
        day = None

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if time_filter == 'day':
        day = input("\nWhich day? Mon, Tue, Wed, Thu, Fri, Sat, or Sun?\n").title()
        while day not in days:
            day = input("The day you enter is incorrect, please try again. "
                        "Which day? Mon, Tue, Wed, Thu, Fri, Sat, or Sun?\n").title()

        # set month to None
        month = None

    # get user input for month and day if user selected both
    if time_filter == 'both':
        month = input("\nWhich month? January, February, March, April, May, June?\n").title()
        while month not in months:
            month = input("The month you enter is incorrect, please try again. "
                          'Please enter "January", "February", "March", "April", "May", "June".\n').title()

        day = input("\nWhich day? Mon, Tue, Wed, Thu, Fri, Sat, or Sun?\n").title()
        while day not in days:
            day = input("The day you enter is incorrect, please try again. "
                        "Which day? Mon, Tue, Wed, Thu, Fri, Sat, or Sun?\n").title()

    # set month and day to none when user select 'none' time filter
    if time_filter == 'none':
        month = None
        day = None

    print('-'*80)
    print("\nYour filter selection\nCity:  {}\nMonth: {}\nDay:   {}".format(city, month, day))
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns.
    # E.g. January = 1, March = 3, Monday=0, Sunday=6.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month is not None:
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day is not None:
        # use the index of day of the week to get the corresponding int
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        day = days.index(day)

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    # validate result
    # print(df)
    # print("\nLoaded data\nCity: {}\nMonth: {}\nDay: {}".format(city, month, day))

    # reset df index
    df = df.reset_index()

    # save to excel to validate filtered result
    # df.to_csv("filtered_city.csv")

    return df


def time_stats(df, month, day):
    """
    calculate time statistic

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        Most popular month/day/hour
    """

    # get start running time of this function
    start_time = time.time()

    print("\nWorking on time statistic...")
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    # Get top month if no month filter
    if month is None:
        top_month = df.groupby('month')['month'].count().sort_values().tail(1).index.values[0]
        top_month_value = df.groupby('month')['month'].count().sort_values().tail(1).iloc[0]

        # match int to month(str) and output result
        print("Most popular month: {}, count: {}".format(months[top_month - 1], top_month_value))

    # Get top day if no day filter
    if day is None:
        top_day = df.groupby('day_of_week')['day_of_week'].count().sort_values().tail(1).index.values[0]
        top_day_value = df.groupby('day_of_week')['day_of_week'].count().sort_values().tail(1).iloc[0]

        # match int to day of week(str) and output result
        print("Most popular day: {}, count: {}".format(days[top_day], top_day_value))

    # Get top hour no matter what time filter is selected
    top_hour = df.groupby('hour')['hour'].count().sort_values().tail(1).index.values[0]
    top_hour_value = df.groupby('hour')['hour'].count().sort_values().tail(1).iloc[0]

    # output result
    print("Most popular hour: {}, count: {}".format(top_hour, top_hour_value))

    # get the end running time of this function
    end_time = time.time()
    # print run time of this function
    print("It took {} seconds.".format(end_time - start_time))


def station_stats(df):
    """
    calculate station statistic

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        Most common start station, most common end station, most common trip(start & end station)
    """

    # get start running time of this function
    start_time = time.time()

    # get most common start station
    print("\nWorking on station statistic...")
    most_common_start_station = df.groupby('Start Station')['Start Station'].count().sort_values().tail(1)\
        .index.values[0]
    most_common_start_station_count = df.groupby('Start Station')['Start Station'].count().sort_values().tail(1).iloc[0]
    print("Most common Start Station: {}, count: {}".format(most_common_start_station, most_common_start_station_count))

    # get most common end station
    most_common_end_station = df.groupby('End Station')['End Station'].count().sort_values().tail(1).index.values[0]
    most_common_end_station_count = df.groupby('End Station')['End Station'].count().sort_values().tail(1).iloc[0]
    print("Most common End Station: {}, count: {}".format(most_common_end_station, most_common_end_station_count))

    # get most common trip (start & end station)
    # create Trip column with Start Station & End Station
    df['Trip'] = df['Start Station'] + " + " + df['End Station']
    # print("\nCombine with Start and End station\n", df)
    most_common_trip = df.groupby('Trip')['Trip'].count().sort_values().tail(1).index.values[0]
    most_common_trip_count = df.groupby('Trip')['Trip'].count().sort_values().tail(1).iloc[0]
    print("Most common Trip: {}, count: {}".format(most_common_trip, most_common_trip_count))

    # get the end running time of this function
    end_time = time.time()
    # print run time of this function
    print("It took {} seconds.".format(end_time - start_time))


def trip_duration_stats(df):
    """
    calculate travel time statistic

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        Total travel time, average travel time.
    """

    # get start running time of this function
    start_time = time.time()

    print("\nWorking on Trip statistic...")
    # get total travel time (hours)
    total_travel_time = df['Trip Duration'].sum() / 3600
    total_travel_time = format(total_travel_time, '.0f')

    # get average travel time (minutes)
    average_travel_time = df['Trip Duration'].mean() / 60
    average_travel_time = format(average_travel_time, '.0f')

    # output result
    print("Total travel time: {} hours\nAverage travel time: {} minutes".format(total_travel_time, average_travel_time))

    # get the end running time of this function
    end_time = time.time()
    # print run time of this function
    print("It took {} seconds.".format(end_time - start_time))


def user_stats(df, city):
    """
    calculate user statistic

    Args:
        (str) city - name of the city to analyze
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        User type, gender, earliest year of birth, most recent year of birth, most common year of birth
    """

    # get start running time of this function
    start_time = time.time()

    print("\nWorking on User statistic...")
    # get user type information
    user_type = df.groupby('User Type')['User Type'].count()
    # print(user_type, "\n")
    print("User Type count")
    print("Customer: ", user_type['Customer'])
    print("Subscriber: ", user_type['Subscriber'])

    if city == 'Chicago' or city == 'New York':
        # get gender information
        gender = df.groupby('Gender')['Gender'].count()
        # print(gender, "\n")
        print("\nGender count")
        print("Female: ", gender['Female'])
        print("Male: ", gender['Male'])

        # set "Birth Year" column as int
        df['Birth Year'] = df['Birth Year'].astype('Int64')
        # print("\nBirth Year\n", df['Birth Year'])

        # get earliest year of birth
        earliest_birth = df.sort_values(by=['Birth Year']).head(1)['Birth Year'].iloc[0]
        # print("\nSort by earliest year of birth\n", df.sort_values(by=['Birth Year'])['Birth Year'])
        print("\nThe earliest year of birth:", earliest_birth)

        # get most recent year of birth
        most_recent_birth = df.sort_values(by=['Birth Year'], na_position='first').tail(1)['Birth Year'].iloc[0]
        print("The most recent year of birth:", most_recent_birth)

        # get most common year of birth, covert output list to string, and remove "[" and "]" by [1:-1]
        most_common_birth = df['Birth Year'].mode().tolist().__str__()[1:-1]
        print("The most common year(s) of birth:", most_common_birth)

    # get the end running time of this function
    end_time = time.time()
    # print run time of this function
    print("It took {} seconds.\n".format(end_time - start_time))


def raw_data(df):
    """
    Ask whether user want to see raw data, if yes then show the first 5 records, and so on.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        raw data
    """

    # ask if user want to view individual trip data
    answer = input('Would you like view first 5 individuals trip data? Type "yes" or "no".\n').lower()
    while answer not in ['yes', 'no']:
        answer = input('The answer you enter is incorrect. Please enter "yes" or "no".\n').lower()

    # set num = 0 as the first row
    num = 0

    # user want to view individual trip data
    while answer == 'yes':
        print(f"\nHere are data of row {num + 1} to {num + 5}.")
        # show raw data for 5 rows
        for i in range(num, num+5):
            # show 5 rows with all columns except last 3 columns which are customized columns
            print(df.loc[i][:-3], "\n")

        # prepare for next 5 rows
        num += 5

        # ask if user want to get next 5 individuals trip data
        answer = input('\nWould you like view next 5 individuals trip data? Type "yes" or "no".\n').lower()
        while answer not in ['yes', 'no']:
            answer = input('The answer you enter is incorrect. Please enter "yes" or "no".\n').lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        # ask if user want to restart this script again
        restart = input('\nWould you like to restart? Enter "yes" or "no".\n').lower()
        while restart not in ['yes', 'no']:
            restart = input('The answer you enter is incorrect. Please enter "yes" or "no".\n').lower()
        if restart == 'no':
            break


if __name__ == "__main__":
    main()
