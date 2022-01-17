import time
import pandas as pd
import numpy as np

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
    
    while True:
        try:
            city = input("\nKindly enter the city name (chicago, new york city, washington): ").lower()
            if city in ["chicago", "new york city", "washington"]:
                break
            else:
                raise Exception()
        except Exception:
            print("That's not a valid city!")
            
    while True:
        try:
            month = input("\nWhat month would you like to filter by (all, january, february, ... , june): ").lower()
            if month in ["all", "january", "february", "march", "april", "may", "june"]:
                break
            else:
                raise Exception()
        except Exception:
            print("That's not a valid month!")

    while True:
        try:
            day = input("\nWhat day would you like to filter by (all, monday, tuesday, ... sunday): ").lower()
            if day in ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
                break
            else:
                raise Exception()
        except Exception:
            print("That's not a valid day of week!")

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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    time.sleep(3)

    start_time = time.time()

    m = df["month"].mode()[0] - 1
    months_of_year = ["January", "February", "March", "April", "May", "June"]
    print("Most common month of travel is {}".format(months_of_year[m]))

    print("Most common day of travel is {}".format(df["day_of_week"].mode()[0]))

    print("Most common start hour is {}".format(df["Start Time"].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    time.sleep(3)

    start_time = time.time()

    print("Most commonly used start station is \"{}\"".format(df["Start Station"].mode()[0]))

    print("Most commonly used end station is \"{}\"".format(df["End Station"].mode()[0]))

    df["station_combination"] = df["Start Station"] + "," + df["End Station"]
    first_station = df["station_combination"].mode()[0].split(",")[0]
    second_station = df["station_combination"].mode()[0].split(",")[1]
    print("Most frequent combination of start station and end station trip is from \"{}\" to \"{}\"".format(first_station, second_station))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    time.sleep(3)

    start_time = time.time()


    print("Total travel time is {} minutes".format(df['Trip Duration'].sum().round()))

    print("Mean travel time is {} minutes".format(df['Trip Duration'].mean().round()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    time.sleep(3)
    
    start_time = time.time()

    print("User Type Count is: ")
    print(df['User Type'].value_counts())

    print("\nGender Count details are as follows: ")
    
    try:
        print(df['Gender'].value_counts())
    except:
        print("Gender column is absent in the dataset")

    print("\nBirth Year stats are as follows: ")
    try:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df["Birth Year"].mode()[0])
    
        print("Earliest birth year is {} \nMost recent birth year is {} \nMost common birth year is {}".format(earliest_year, most_recent_year, most_common_year))
    except:
        print("Birth Year column is absent in the dataset")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_raw_data(df):
    """ Prompts user to display raw data """
    i = 0
    raw = input("Would you like to see the raw data (yes or no): ").lower()
    pd.set_option('display.max_columns',200)

    while True:            
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df.iloc[i:i+5, :])
            raw = input("Would you like to see the next 5 rows (yes or no): ").lower()
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no': ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        restart = ""

        while True:
            try:
                restart = input('\nWould you like to restart? (Enter yes or no): ')
                if restart.lower() != 'yes' and restart.lower() != 'no':
                    raise Exception()
                elif restart.lower() == 'no' or restart.lower() == 'yes':
                    break
            except Exception:
                print("Kindly enter a valid response")
                
        if restart.lower() == 'no':
            break
if __name__ == "__main__":
	main()