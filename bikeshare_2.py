#Import required packages
import time
import pandas as pd
import numpy as np

#dictionary of cities corresponding to their data files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
days = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}

#The following fuction will get the user choices for filters: city, month, and day.
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    #The following loop will get the user's choice of which city to display results.
    while True:
        city = input('Would you like to see data for Chicago/Ch, New York City/NYC, or Washington/WA: ').lower()
        if city not in CITY_DATA.keys() and city not in ['ch', 'nyc', 'wa']:
            print('this city is not available, please enter one of the three provided cities')
            continue
        else:
            if city == 'ch':
                city = 'chicago'
            elif city == 'nyc':
                city = 'new york city'
            elif city == 'wa':
                city = 'washington'
            city = CITY_DATA[city]
            break

    #The following loop will get the user choice whether to use filters or display unfiltered results.
    while True:
        filter = input('Would you like to filter the data by month or day, or not at all? \nPlease chose(yes/no): ').lower()
        if filter == 'yes':
            filter = True
        elif filter == 'no':
            filter = False
        else:
            print('Please enter a valid answer!')
            continue
        break


    #the following loop will get the user choice for filters: whether by month, by day, or include both.
    while True:
        if filter:
            choice = input('What filter do you want to apply? please choose (month/day/both) ').lower()
            if choice not in ['month', 'day', 'both']:
                print('Please Enter a valid answer!')
                continue
            if choice == 'month':
                month = input('Which month - January, February, March, April, May, or June? ')
                if month not in months.keys():
                    print('This month is invalid, Please Try again.')
                    continue
                else:
                    month = months[month]
                    day = days
                    break
            elif choice == 'day':
                day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ').lower()
                if day not in days.keys():
                    print('This day is invalid. Please try again.')
                    continue
                else:
                    day = days[day]
                    month = months
                    break
            elif choice == 'both':
                month = input('Which month - January, February, March, April, May, or June? ').lower()
                if month not in months.keys():
                    print('This month is invalid. Please try again')
                    continue
                month = months[month]
                day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ').lower()
                if day not in days.keys():
                    print('This day is invalid. Please try again')
                    continue
                day = days[day]
                break
        else:
            day = days
            month = months
            break

    #Print Separator
    print('-'*40)
    #Return chosen values
    return city, month, day

#The following function will load the data from the provided data files
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
    df = pd.read_csv(city)
    #add a column for day of week extracted from start time column
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    #add a column for month extracted from start time column
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    #add a column for hour extracted from start time column
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour
    if day != days:
        df = df[df['day_of_week'] == day]
    if month != months:
        df = df[df['month'] == month]
    return df

#The following function will display time statistics of most frequent schedules.
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    for key, value in months.items():
        if value == most_common_month:
            print('The most common month is {}'.format(key))
    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    for key, value in days.items():
        if value == most_common_day:
            print('The most common day is {}'.format(key))
    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common hour is {}'.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#The following function will display station statistics of most frequent rides.
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used Start Station is: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most commonly used End Station is: {}'.format(df['End Station'].mode()[0]))


    # display most frequent combination of start station and end station trip
    print('The most common station combination is: {}'.format((df['Start Station'] + ' to ' + df['End Station']).mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#The following function will display duration statistics of travel time.
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    trip_duration = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])

    # display total travel time
    total_travel_time = trip_duration.sum()
    print('Total trave time was: {}'.format(total_travel_time))


    # display mean travel time
    mean_travel_time = trip_duration.mean()
    print('Average travel time was: {}'.format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#The following function will display user info statistics of most common user type and gender if applicable.
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of each user type is:\n{}'.format(user_types))

    # Display counts of gender
    try:
        user_gender = df['Gender'].value_counts()
        print('\nCounts for each gender is:\n{}'.format(user_gender))
    except:
        print('\nCounts for each gender is: No data available.')
        #No gender data available for washington


    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min()
        print('\nEarliest year: Oldest users were born in {}'.format(earliest_year))
    except:
        print('\nEarliest year: No available data')

    try:
        latest_year = df['Birth Year'].max()
        print('Latest year: Youngest users were born in {}'.format(latest_year))
    except:
        print('Latest year: No available data')

    try:
        most_common_year = df['Birth Year'].value_counts().idxmax()
        print('Most common Year of Birth is {}'.format(most_common_year))
    except:
        print('Most common year of Birth: No available data')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        while True:
            raw_data_iterator = 0
            display_raw = input('\nWould you like to see some of the raw data for that City? Please choose yes or no.\n')
            if display_raw.lower() == 'yes':
                print(df.iloc[raw_data_iterator : raw_data_iterator+5])
                while True:
                    display_more = input('Above is displayed 5 rows by the chosen filters.\nDo you want to see the next 5 rows? Please choose yes or no.\n')
                    if display_more.lower() == 'yes':
                        raw_data_iterator += 5
                        print(df.iloc[raw_data_iterator : raw_data_iterator+5])
                    else:
                        break
                break
            else:
                break


        restart = input('\nWould you like to restart? Please choose yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
