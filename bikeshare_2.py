import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # User input for cities (Chicago, New York City, Washington), using while loop to ensure valid city input, normalized with lower()
    while True:
        city = input("\nFor which city would you like to see data: Chicago, New York City, or Washington? \n").lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print("Please enter either Chicago, New York City, or Washington. Invalid entry.")
            continue
        else:
            break

    # User input for month between January and June, or all, using while loop to ensure valid month input, normalized with lower()
    while True:
        month = input("\nFor which month would you like to see data: January, February, March, April, May, June, or all? \n").lower()
        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print("Please enter a month between January and June. Invalid entry.")
            continue
        else:
            break

    # User input for day of the week, or all, normalized with lower()
    while True:
        day = input("\nFor which day would you like to see data: "
                    "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? Or all?\n").lower()
        if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            print("Please enter full name of a day of the week. Invalid entry")
            continue
        else:
            break

    print('-'*40)
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
    # load file into dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # month and day of week from Start Time, creating new columns. Return month name, not integer.
    df['month'] = df['Start Time'].dt.strftime('%B')
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month, if applicable
    if month != 'all':
        # use index of months list to get corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

    # filter by day of week, if applicable
    if day!= 'all':
        # filter by day of week to create new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def display_data(df):
    """Displays five rows of the data in no order"""

    while True:
        data_rows = input("Would you like to see a sample of the data? Y or N\n").lower()
        if data_rows == 'y':
            print( df.sample(5))
        elif data_rows == 'n':
            break
        else:
            print("Please choose Y or N.\n")

    df.sample(5)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    frequent_month = df['month'].mode()[0]
    print("The most common month for travel is ", frequent_month)

    # display the most common day of week
    frequent_day = df['day_of_week'].mode()[0]
    print("The most common day of the week is ", frequent_day)

    # display the most common start hour. Converted to time format for the hour.
    df['hour'] = df['Start Time'].values.astype('<M8[h]')
    df['hour'] = df['hour'].dt.time
    frequent_hour = df['hour'].mode()[0]
    print("The most common time of the day for travel is ", frequent_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station. idxmax returns the value in the row for the highest count
    frequent_start = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station is ", frequent_start)

    # display most commonly used end station. idxmax returns the value in the row for the highest count
    frequent_end = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station is ", frequent_end)

    # display most frequent combination of start station and end station trip.
    combo_station = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).idxmax()
    print('The most common combination of start and end station: ', combo_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = sum(df['Trip Duration'])
    # divide time in seconds by seconds in a day to get days
    print("The total travel time is ", travel_time/86400 , "days.")

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print("The average travel time is ", avg_travel_time/60, "minutes.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count of user types:\n', user_types)


    # Display counts of gender
    try:
        count_gender = df['Gender'].value_counts()
        print('Count of gender types:\n', count_gender)
    except KeyError:
        print("No gender data available for this month.")


    # Display earliest, most recent, and most common year of birth
    try:
        oldest_birth_year = df['Birth Year'].min()
        print("The oldest birth year is ", oldest_birth_year)
    except KeyError:
        print("No birth year data available for this month.")

    try:
        youngest_birth_year = df['Birth Year'].max()
        print("The youngest birth year is ", youngest_birth_year)
    except KeyError:
        print("No birth year data available for this month.")

    try:
        common_birth_year = df['Birth Year'].value_counts().idxmax()
        print("The most common birth year is ", common_birth_year)
    except KeyError:
        print("No birth year data available for this month.")

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

        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
