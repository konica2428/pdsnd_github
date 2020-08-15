import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#MONTH_LIST = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nHello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs


    while True:
        city = input("For Which City would you like to access the bikeshare data- New York City, Washington or Chicago?\n")
        city=city.lower()
        if city not in ("new york city", "chicago", "washington"):
            print("Please enter a valid city name.")
            continue
        else:
            break


    # TO DO: get user input for month (all, january, february, ... , june)

    while True:

        month = input("For which month between January and June you would like to access the data? Provide 'all' as an input for accessing the data for all the months.\n")

        if month not in ('January', 'February', 'March', 'April', 'May', 'June', 'all'):
            print("Please enter a valid month.")
            continue
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day=''

        day=input("For which day of the week would you like to access the data? If there is no preference, provide 'all' as an input\n")
        day=day.lower()
        if day not in DAY_LIST:
            print("Please enter a valid day of the week.")
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
     # load data file
    df = pd.read_csv(CITY_DATA[city])

    # conversion of the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extraction of the month and day of the week from Start Time to create the new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    if month != 'all':
   	 	# using the index of the months list to get the respective int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month for the creation of new dataframe
        df = df[df['month'] == month]

    if day != 'all':

        # filter by the day_of_week for the creation of new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    freq_month = df['month'].mode()[0]
    print('The most popular month is:', freq_month)


    # TO DO: display the most common day of week

    freq_day = df['day_of_week'].mode()[0]
    print('The most Popular day of the week is', freq_day)



    # TO DO: display the most common start hour

    df['starthour'] = df['Start Time'].dt.hour
    freq_hour = df['starthour'].mode()[0]
    print('The most common start hour for travel is:', freq_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station

    Start_Station = df['Start Station'].value_counts().idxmax()
    print('The most Commonly used start station is:', Start_Station)


    # TO DO: display most commonly used end station

    End_Station = df['End Station'].value_counts().idxmax()
    print('\nThe most Commonly used end station is:', End_Station)


    # TO DO: display most frequent combination of start station and end station trip

    freq_start_to_end_station=df['Start Station'] + 'TO' + df['End Station']
    print('\nThe frequent combination of start to End station is:', Start_Station, " & ", End_Station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']


    # TO DO: display total travel time

    total_travel_time = sum(df['Trip Duration'])
    print ("\nThe total travel time is ", total_travel_time/3600, 'Hours')



    # TO DO: display mean travel time

    mean_travel_time = df['Trip Duration'].mean()
    print('The Mean travel time is:', mean_travel_time/3600, 'Hours or', mean_travel_time/60, 'Minutes' )



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types

    type_of_users = df['User Type'].value_counts()
    print('Types of Users are:\n',type_of_users)

    # TO DO: Display counts of gender


    if 'Gender' in df:

        gender_of_users = df.groupby('Gender',as_index=False).count()
        print('The count of gender of users mentioned in the data are {}'.format(len(gender_of_users)))
        for i in range(len(gender_of_users)):
            print('{}s - {}'.format(gender_of_users['Gender'][i], gender_of_users['Start Time'][i]))
        print('Gender data for {} users is not available.'.format(len(df)-gender_of_users['Start Time'][0]-gender_of_users['Start Time'][1]))

    else:
        print('Sorry, no gender data is available for this city.')


    # TO DO: Display earliest, most recent, and most common year of birth

    if 'Birth Year' not in df:
        print('The data related to the birth year is not available for this city.')
    else:
        birth = df.groupby('Birth Year', as_index=False).count()
        print('The earliest year of birth is {}.'.format(int(birth['Birth Year'].min())))
        print('The most recent year of birth is {}.'.format(int(birth['Birth Year'].max())))
        print('The most common year of birth year is {}.'.format(int(birth.iloc[birth['Start Time'].idxmax()]['Birth Year'])))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_ind_data(df):

    #Displays 5 rows of data of individual trips from the csv file for the selected city.

    ACCEPTED_RESPONSE_LIST = ['yes', 'no']
    ind_data = ''

    counter = 0
    while ind_data not in ACCEPTED_RESPONSE_LIST:
        print("\nWould you like to see the data for the individual trips for the selected city?")
        print("\nYes\nNo")
        ind_data = input().lower()
        #the individual trip data will be displayed if the response from the users is Yes
        if ind_data == "yes":
            print(df.head())
        elif ind_data not in ACCEPTED_RESPONSE_LIST:
            print("\nPlease enter the valid response.")


    while ind_data == 'yes':
        print("Would you like to see more data? Yes or No")
        counter += 5
        ind_data = input().lower()
        if ind_data == "yes":
             print(df[counter:counter+5])

        elif ind_data == "no":
             break

    print('-'*80)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)


        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_ind_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
