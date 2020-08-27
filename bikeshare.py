import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    time_filter = ""
    month = ""
    day = ""
    error_text = "Wrong entry. Select from the list and make sure to spell correctly."
    while city not in ["chicago", "new york", "washington"]:
        city = input("Please choose city from list: Chicago, New York or Washington: ").lower()
        if city == "chicago" or city == "new york" or city == "washington":
            city = city
        else:
            print(error_text)  

    while time_filter not in ["month", "day", "none"]:
        time_filter = input("Please choose time filter from list: Month, Day or None: ").lower()
        if time_filter == "month" or time_filter == "day" or time_filter == "none":
            time_filter = time_filter
        else:
            print(error_text)   
    
    # get user input for month (all, january, february, ... , june)
    if time_filter == "month":
        while month not in ["all", "january", "february", "march", "april", "may", "june"]:
            month = input("Please choose month from list: All, January, February, March, April, May or June: ").lower()
            if month in ["all", "january", "february", "march", "april", "may", "june"]:
                month = month
            else:
                print(error_text) 

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if time_filter == "day":
        while day not in ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            day = input("Please choose day from list: All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday: ").lower()
            if day in ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
                day = day
            else:
                print(error_text) 

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != "":
        if month != 'all':
            # use the index of the months list to get the corresponding int
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != "":
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    # dur bi month = months.index(month) + 1
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Frequent Month:', months[popular_month - 1].title())

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    popular_weekday = df['day_of_week'].mode()[0]
    print('Most Frequent Day of Week:', popular_weekday)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df["Start Station"].mode()[0]
    print('Most Frequent Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df["End Station"].mode()[0]
    print('Most Frequent End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df["trip"] = df["Start Station"] + " --> " + df["End Station"]
    popular_trip = df["trip"].mode()[0]
    print('Most Frequent Trip:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print("Total travel time:", total_duration, "s")

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print("Mean travel time:", mean_duration, "s")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print("User type counts:\n")
    print(user_types)

    # Display counts of gender
    print("\nGender counts:\n")
    if 'Gender' in df:
        genders = df["Gender"].value_counts()
        print(genders)
    else: 
        print("\nThere is no gender data for Washington")

    # Display earliest, most recent, and most common year of birth
    print("\nBirthyear stats:\n")
    if 'Birth Year' in df:
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        common = df['Birth Year'].mode()[0]
        print("\nEarliest birth year:", earliest)
        print("Most recent birth year:", recent)
        print("Most common birth year:", common)
    else:
        print("\nThere is no birth year data for Washington")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays raw data in 5 row increments upon user request.""" 
    raw_rows = 0
    error_text = "Wrong entry. Select from the list and make sure to spell correctly."
    response = input("Do you want to see the first 5 lines of the raw data? Enter yes or no.\n").lower()

    while response == "yes":
        print(df.iloc[raw_rows : raw_rows + 5])
        raw_rows += 5
        response = input("Do you want to see the next 5 lines of the raw data? Enter yes or no.\n").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
