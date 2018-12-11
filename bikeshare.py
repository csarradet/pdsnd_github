import time
import pandas as pd

CITIES = ['chicago', 'new york city', 'washington']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


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
    city = numeric_prompt('Choose a target city:', CITIES)

    # get user input for month (all, january, february, ... , june)
    month = numeric_prompt('Choose a target month:', ['all'] + MONTHS)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = numeric_prompt('Choose a target day:', ['all'] + DAYS)

    print('\nFiltering by {} / {} / {}'.format(city, month, day))
    print_line()
    return city, month, day


def print_line():
    print('-' * 40)


def numeric_prompt(intro_text, allowed_choices, start_number=1):
    """ Presents the user with allowed_choices, has them select one
        by entering a number.  Returns an entry from allowed_choices. """
    print('\n' + intro_text)
    i = iter(range(start_number, start_number + len(allowed_choices) + 1))
    indexed_choices = {next(i): x for x in allowed_choices}
    end_number = next(i) - 1
    while (True):
        for a in indexed_choices:
            print('\t{}: {}'.format(a, indexed_choices[a]))
        choice = raw_input('\nEnter a number from {} to {}: '.format(start_number, end_number))
        try:
            return indexed_choices[int(choice)]
        except Exception:
            print('\n** Invalid selection, please try again **')


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
    city_filename = city.replace(' ', '_') + '.csv'
    df = pd.read_csv(city_filename)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract datetime components from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day if applicable
    if day != 'all':
        df = df[df['day_of_week'] == DAYS.index(day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month:')
    print(MONTHS[df['month'].mode()[0] - 1])

    # display the most common day of week
    print('Most common day of week:')
    print(DAYS[df['day_of_week'].mode()[0]])

    # display the most common start hour
    print('Most common start hour:')
    print(df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_line()


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most common start station:')
    print(df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most common end station:')
    print(df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('Most common start / end station pair:')
    df['trips'] = df.apply(lambda x: x['Start Station'] + ' >> ' + x['End Station'], axis=1)

    print(df['trips'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_line()


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['travel_time'] = df.apply(lambda x: x['End Time'] - x['Start Time'], axis=1)
    print('Total travel time:')
    print(df['travel_time'].sum())

    # display mean travel time
    print('Mean time:')
    print(df['travel_time'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_line()


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCounts of user types:')
    print(df['User Type'].value_counts())

    # Display counts of gender
    try:
        print('\nCounts of gender:')
        print(df['Gender'].value_counts())
    except KeyError:
        # Not all cities have gender/birthday data in the source CSVs
        print('No gender data available')

    # Display earliest, most recent, and most common year of birth
    try:
        print('\nBirth year stats:')
        print('\tearliest: {0:g}'.format(df['Birth Year'].min()))
        print('\tmost recent: {0:g}'.format(df['Birth Year'].max()))
        print('\tmost common: {0:g}'.format(df['Birth Year'].mode()[0]))
    except KeyError as e:
        print('No birthday data available ({})'.format(e))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_line()


def display_raw_data(df):
    start_row = 0
    interval = 5
    while True:
        print(df[start_row:start_row + interval])
        start_row += interval
        restart = raw_input('\nEnter "r" to see five more lines of raw data, or anything else to restart: ')
        if restart != 'r':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = raw_input('\nChoose an option:\n\tEnter "y" to restart\n\t"r" to see five lines of raw data\n\tanything else to exit: \n')
        if restart not in ['y', 'r']:
            break

        if restart == 'y':
            continue

        if restart == 'r':
            display_raw_data(df)


if __name__ == "__main__":
    main()
