import matplotlib.pyplot as plt
import random
import math

import pycountry
from collections import defaultdict
from datetime import datetime

class Graph:
    def __init__(self, spotify_data):
        self.spotify_data = spotify_data

    def print_data(self, song_names=False):
        print(f"Username: {self.spotify_data.user_data.get('username', 'N/A')}")
        print(f"User ID: {self.spotify_data.user_data.get('userid', 'N/A')}")
        print(f"Country/Region: {self.spotify_data.user_data.get('country', 'N/A')}")
        print(f"Profile Picture URL: {self.spotify_data.user_data.get('profile_picture', 'N/A')}")
        print(f"Number of Playlists Created: {self.spotify_data.user_data.get('num_playlists', 0)}")
        print(f"Total Number of Tracks in Playlists: {self.spotify_data.user_data.get('num_tracks', 0)}")
        print(f"Number of Liked Tracks: {self.spotify_data.user_data.get('num_liked_tracks', 0)}")
        print(f"Top Genres: {self.spotify_data.user_data.get('top_genres', [])}")
        print(f"Number of Favorite Songs: {len(self.spotify_data.user_data.get('favorite_songs', []))}")
        if song_names:
            for song in self.spotify_data.user_data.get('favorite_songs', []):
                print(f"- {song[0]} by {song[1]}, added on {song[7]}")

    def draw_top_artists(self, selectednumber, is_show:bool=False):
        # Count the number of songs per artist
        artist_count = {}
        for song in self.spotify_data.user_data['favorite_songs']:
            artist_name = song[1]
            if artist_name in artist_count:
                artist_count[artist_name] += 1
            else:
                artist_count[artist_name] = 1

        # Order the list of artists by descending song count
        sorted_artists = sorted(artist_count.items(), key=lambda x: x[1], reverse=True)
        sorted_artists = sorted_artists[:selectednumber]

        # Extract artist names and song counts for the selected number of artists
        labels = [artist[0] for artist in sorted_artists]
        counts = [artist[1] for artist in sorted_artists]

        # Create a list of random colors for each bar
        colors = [random.choice(['#' + format(random.randint(0, 16777215), '06x') for _ in range(6)]) for _ in
                  range(selectednumber)]

        # Set the font family to Arial Unicode
        plt.rcParams['font.family'] = 'Arial Unicode MS'

        # Create a bar chart with different colors for each bar and add a grid
        plt.bar(labels, counts, color=colors)

        plt.xlabel('Artist')
        plt.ylabel('Number of Songs')
        plt.title(f'Top {selectednumber} Artists by Song Count')

        # Set the y-axis tick locations as integer values
        plt.yticks(range(math.ceil(max(counts)) + 1))

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')

        # Display the histogram
        plt.tight_layout()
        plt.savefig(f"images/top_artists_top_{selectednumber}.png")
        if is_show:
            plt.show()
        plt.close()

    def draw_artist_histogram(self, is_show:bool=False):
        # Compter le nombre de chansons par artiste
        artist_count = {}
        for song in self.spotify_data.user_data['favorite_songs']:
            artist_name = song[1]
            if artist_name in artist_count:
                artist_count[artist_name] += 1
            else:
                artist_count[artist_name] = 1

        # Compter le nombre d'artistes par nombre de chansons
        count_artist = {'1': 0, '2': 0, '3': 0,
                        '4': 0, '5': 0, '6': 0,
                        '7': 0, '8': 0, '9': 0, '10+': 0}
        for count in artist_count.values():
            if count == 1:
                count_artist['1'] += 1
            if count == 2:
                count_artist['2'] += 1
            if count == 3:
                count_artist['3'] += 1
            if count == 4:
                count_artist['4'] += 1
            if count == 5:
                count_artist['5'] += 1
            if count == 6:
                count_artist['6'] += 1
            if count == 7:
                count_artist['7'] += 1
            if count == 8:
                count_artist['8'] += 1
            if count == 9:
                count_artist['9'] += 1
            if count >= 10:
                count_artist['10+'] += 1

        # Préparer les étiquettes et les hauteurs des barres
        labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10+']
        counts = [count_artist['1'], count_artist['2'], count_artist['3'],
                  count_artist['4'], count_artist['5'], count_artist['6'],
                  count_artist['7'], count_artist['8'], count_artist['9'],
                  count_artist['10+']]

        # Créer un histogramme
        plt.bar(labels, counts)
        plt.xlabel('Number of Songs')
        plt.ylabel('Number of Artists')
        plt.title('Number of Artists by Song Count')

        # Afficher l'histogramme
        plt.savefig("images/artists_by_song_count_histogram.png")
        if is_show:
           plt.show()
        plt.close()

    def draw_duration_histogram(self, is_show:bool=False):
        # Compter le nombre de chansons par durée
        duration_count = {'<2m00': 0, '2m00-2m15': 0,'2m15-2m30': 0,
                          '2m30-2m45': 0, '2m45-3m00': 0, '3m00-3m15': 0,
                           '3m15-3m30': 0, '3m30-3m45': 0,'3m45-4m00': 0,
                           '4m00-4m15': 0, '4m15-4m30': 0,
                          '4m30-4m45': 0, '4m45-5m00': 0, '>5m00': 0}

        for song in self.spotify_data.user_data['favorite_songs']:
            duration = song[4] / 1000

            if duration < 120:
                duration_count['<2m00'] += 1
            elif 120 <= duration < 135:
                duration_count['2m00-2m15'] += 1
            elif 135 <= duration < 150:
                duration_count['2m15-2m30'] += 1
            elif 150 <= duration < 165:
                duration_count['2m30-2m45'] += 1
            elif 165 <= duration < 180:
                duration_count['2m45-3m00'] += 1
            elif 180 <= duration < 195:
                duration_count['3m00-3m15'] += 1
            elif 195 <= duration < 210:
                duration_count['3m15-3m30'] += 1
            elif 210 <= duration < 225:
                duration_count['3m30-3m45'] += 1
            elif 225 <= duration < 240:
                duration_count['3m45-4m00'] += 1
            elif 240 <= duration < 255:
                duration_count['4m00-4m15'] += 1
            elif 255 <= duration < 270:
                duration_count['4m15-4m30'] += 1
            elif 270 <= duration < 285:
                duration_count['4m30-4m45'] += 1
            elif 285 <= duration < 300:
                duration_count['4m45-5m00'] += 1
            else:
                duration_count['>5m00'] += 1

        # Préparer les étiquettes et les hauteurs des barres
        labels = ['<2m00', '2m00-2m15', '2m15-2m30', '2m30-2m45', '2m45-3m00', '3m00-3m15', '3m15-3m30',
                  '3m30-3m45', '3m45-4m00', '4m00-4m15', '4m15-4m30', '4m30-4m45', '4m45-5m00', '>5m00']
        counts = [duration_count[label] for label in labels]

        # Créer un histogramme
        plt.bar(labels, counts)
        plt.xlabel('Duration')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Number of Songs')
        plt.title('Number of Songs by Duration')

        # Afficher l'histogramme
        plt.savefig("images/duration_histogram.png")
        if is_show:
            plt.show()
        plt.close()


    def draw_countries_by_songs(self, is_show:bool=False):
        country_scores = {}

        for song in self.spotify_data.user_data['favorite_songs']:
            artist_country = song[6]
            if artist_country in country_scores:
                country_scores[artist_country] += 1
            else:
                country_scores[artist_country] = 1

        # Sort country scores in descending order (excluding 'Unknown')
        sorted_scores = sorted(country_scores.items(), key=lambda x: x[1], reverse=True)
        sorted_scores = [score for score in sorted_scores if score[0] != 'Unknown']
        sorted_scores.append(('Unknown', country_scores.get('Unknown', 0)))

        labels = [score[0] for score in sorted_scores]
        values = [score[1] for score in sorted_scores]

        # Calculate the total number of songs
        total_songs = sum(values)

        # Create a list to store the legend labels
        legend_labels = []

        # Create a list to store the pie labels
        pie_labels = []

        # Iterate over the sorted scores and check the percentage for each country
        for label, value in zip(labels, values):
            percentage = (value / total_songs) * 100

            # Check if the country name is void
            country = pycountry.countries.get(alpha_2=label)
            if country is not None:
                legend_label = f"{label} ({country.name}) - Songs: {value} - {percentage:.1f}%"
            else:
                legend_label = f"{label} - Songs: {value} - {percentage:.1f}%"

            legend_labels.append(legend_label)

            # Check if the percentage is below 2
            if percentage >= 2:
                pie_labels.append(f"{label}")
            else:
                pie_labels.append('')

        plt.figure(figsize=(8, 6))
        patches, _ = plt.pie(values, labels=pie_labels, startangle=90)
        plt.title("Origins of Favorite Artists (by total number of songs)")
        plt.legend(patches, legend_labels, loc='center right', bbox_to_anchor=(0.01, 0.5))
        plt.tight_layout()

        plt.savefig("images/countries_by_song.png")
        if is_show:
           plt.show()
        plt.close()

    def draw_countries_by_unique_artists(self, is_show:bool=False):
        country_scores = {}
        distinct_artist_list = []

        for song in self.spotify_data.user_data['favorite_songs']:
            current_artist=song[1]
            if current_artist not in distinct_artist_list:
                distinct_artist_list.append(current_artist)
                artist_country = song[6]
                if artist_country in country_scores:
                    country_scores[artist_country] += 1
                else:
                    country_scores[artist_country] = 1

        # Sort country scores in descending order (excluding 'Unknown')
        sorted_scores = sorted(country_scores.items(), key=lambda x: x[1], reverse=True)
        sorted_scores = [score for score in sorted_scores if score[0] != 'Unknown']
        sorted_scores.append(('Unknown', country_scores.get('Unknown', 0)))

        labels = [score[0] for score in sorted_scores]
        values = [score[1] for score in sorted_scores]

        # Calculate the total number of artists
        total_artists = len(self.spotify_data.user_data['favorite_songs'])

        # Create a list to store the legend labels
        legend_labels = []

        # Create a list to store the pie labels
        pie_labels = []

        # Iterate over the sorted scores and check the percentage for each country
        for label, value in zip(labels, values):
            percentage = (value / len(distinct_artist_list)) * 100

            # Check if the percentage is below 2
            country = pycountry.countries.get(alpha_2=label)
            if country is not None:
                legend_label = f"{label} ({country.name}) - Artists: {value} - {percentage:.1f}%"
            else:
                legend_label = f"{label} - Artists: {value} - {percentage:.1f}%"

            legend_labels.append(legend_label)

            # Check if the percentage is below 2
            if percentage >= 2:
                pie_labels.append(f"{label}")
            else:
                pie_labels.append('')

        plt.figure(figsize=(8, 6))
        patches, _ = plt.pie(values, labels=pie_labels, startangle=90)
        plt.title("Origins of Favorite Artists (by total number of artists)")
        plt.legend(patches, legend_labels, loc='center right', bbox_to_anchor=(0.01, 0.5))
        plt.tight_layout()

        plt.savefig("images/countries_by_unique_artists.png")
        if is_show:
           plt.show()
        plt.close()


    def display_artists_by_country(self, country):
        artist_counts = {}

        # Convert the input country name or abbreviation to uppercase
        country = country.upper()

        # Iterate over favorite songs to count the number of songs for each artist
        for song in self.spotify_data.user_data['favorite_songs']:
            artist_country = song[6]
            # Check if the artist's country matches the input country
            if artist_country.upper() == country:
                artist = song[1]
                # Increment the count for the artist
                artist_counts[artist] = artist_counts.get(artist, 0) + 1

        # Sort artists by descending number of songs
        sorted_artists = sorted(artist_counts.items(), key=lambda x: x[1], reverse=True)

        # Display the list of artists from the specified country with song counts
        if sorted_artists:
            print(f"Artists from {country}:")
            for artist, count in sorted_artists:
                # Check if the count is 1 and modify the word "song" accordingly
                if count == 1:
                    song_word = "song"
                else:
                    song_word = "songs"
                print(f"{artist} - {count} {song_word}")
        else:
            print(f"No artists found from {country}.")

    def draw_artists_pie_chart_by_country(self, country_abbr, is_show:bool=False):
        country_artists = {}

        # Count the number of songs for each artist from the specified country
        for song in self.spotify_data.user_data['favorite_songs']:
            artist_country = song[6]
            if artist_country == country_abbr:
                artist_name = song[1]
                country_artists[artist_name] = country_artists.get(artist_name, 0) + 1

        # Sort artists by descending number of songs
        sorted_artists = sorted(country_artists.items(), key=lambda x: x[1], reverse=True)

        # Prepare data for the pie chart
        labels = []
        counts = []
        pie_labels = []

        # Create separate lists for labels and counts
        for artist, count in sorted_artists:
            labels.append(artist)
            counts.append(count)
            # Check if the percentage is below 2
            if count >= 2:
                pie_labels.append(f"{artist}")
            else:
                pie_labels.append('')

        # Create a legend with artist names and song counts
        legend_labels = [f"{artist} - {count}" for artist, count in sorted_artists]

        # Draw the pie chart with the artist distribution by country

        plt.figure(figsize=(8, 6))
        patches, _ = plt.pie(counts, labels=pie_labels, startangle=90)
        plt.title(f"Artists Distribution from {country_abbr}")
        plt.legend(patches, legend_labels, loc='center right', bbox_to_anchor=(0.01, 0.2))
        plt.tight_layout()

        plt.savefig("images/countries_by_country.png")
        if is_show:
           plt.show()
        plt.close()

    def draw_histogram_by_release_year(self, is_show:bool=False):
        # Extract the favorite songs list from the data
        favorite_songs = self.spotify_data.user_data['favorite_songs']

        # Count the number of songs released in each year
        release_years_count = {}
        for song in favorite_songs:
            release_date = song[5]  # Assuming release_date is at index 5 in the tuple (modify if necessary)
            year = release_date.split("-")[0]  # Get the year from the release_date
            if year in release_years_count:
                release_years_count[year] += 1
            else:
                release_years_count[year] = 1

        # Sort the years in ascending order
        sorted_years = sorted(release_years_count.keys(), key=lambda x: int(x))

        # Prepare the labels and the heights of the bars
        labels = sorted_years
        counts = [release_years_count[year] for year in sorted_years]

        # Create the histogram
        plt.bar(labels, counts)
        plt.xlabel('Release Year')
        plt.ylabel('Number of Songs')
        plt.title('Number of Songs by Release Year')

        # Rotate the x-axis labels for better visibility
        plt.xticks(rotation=45)

        # Show the histogram
        plt.savefig("images/by_release_year.png")
        if is_show:
           plt.show()
        plt.close()

    def draw_histogram_by_add_time(self, time_unit, is_show:bool=False):
        favorite_songs = self.spotify_data.user_data['favorite_songs']

        # Define a function to extract the appropriate time unit from the add_date
        def extract_time_unit(date_str, time_unit):
            date_time_parts = date_str.split('T')
            date_part = date_time_parts[0]
            time_part = date_time_parts[1]
            if time_unit == "hour":
                hour = time_part.split(':')[0]
                return f"{hour}:00"
            elif time_unit == "day":
                return date_part  # Get the day (year-month-day) for daily grouping
            elif time_unit == "weekday":
                dt = datetime.fromisoformat(date_part)
                return dt.strftime("%A")  # Get the weekday name (monday, tuesday, ...) for weekday grouping
            elif time_unit == "week":
                dt = datetime.fromisoformat(date_part)
                return dt.strftime("%U")  # Get the week number for weekly grouping
            elif time_unit == "month":
                dt = datetime.fromisoformat(date_part)
                return dt.strftime("%m")  # Get the month number (01-12) for monthly grouping
            elif time_unit == "year":
                dt = datetime.fromisoformat(date_part)
                return dt.strftime("%Y")  # Get the year (YYYY) for yearly grouping
            else:
                raise ValueError("Invalid time unit. Use 'hour', 'day', 'weekday', 'week', 'month' or 'year'.")

        # Initialize the count for each time unit
        time_units_count = defaultdict(int)

        # Count the number of songs added in each time unit
        for song in favorite_songs:
            add_date = song[7]
            time_unit_value = extract_time_unit(add_date, time_unit)
            time_units_count[time_unit_value] += 1

        if time_unit == "hour":
            labels = [f"{str(hour).zfill(2)}:00" for hour in range(24)]
            counts = [time_units_count[label] for label in labels]
        elif time_unit == "weekday":
            labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            counts = [time_units_count[label] for label in labels]
        else:
            sorted_time_units = sorted(time_units_count.keys())
            labels = [f"{time_unit_value}" for time_unit_value in sorted_time_units]
            counts = [time_units_count[time_unit_value] for time_unit_value in sorted_time_units]

        # Create the histogram
        plt.bar(labels, counts)
        plt.xlabel(f'Add Time ({time_unit.capitalize()})')
        plt.ylabel('Number of Songs')
        plt.title(f'Number of Songs Added by {time_unit.capitalize()}')

        # Show the histogram
        plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
        plt.tight_layout()  # Adjust layout for better fit

        plt.savefig("images/by_add_time.png")
        if is_show:
           plt.show()
        plt.close()


    def draw_duration_vs_release_year(self, is_show:bool=False):
        import matplotlib.pyplot as plt

        years = []
        durations = []

        for song in self.spotify_data.user_data["favorite_songs"]:
            duration_ms = song[4]
            release_date = song[5]

            try:
                year = int(release_date[:4])
                years.append(year)
                durations.append(duration_ms / 60000)  # minutes
            except:
                continue

        plt.figure(figsize=(10, 6))
        plt.scatter(years, durations, alpha=0.6)
        plt.title("Durée des chansons en fonction de l'année de sortie")
        plt.xlabel("Année de sortie")
        plt.ylabel("Durée (minutes)")
        plt.grid(True)
        plt.tight_layout()

        plt.savefig("images/duration_vs_release_year.png")
        if is_show:
           plt.show()
        plt.close()

    def draw_pie_charts_for_all_countries(self, is_save=False, is_show=True):

        import math
        import pycountry
        import matplotlib.pyplot as plt

        favorite_songs = self.spotify_data.user_data["favorite_songs"]

        def draw_artists_pie_chart_by_country_and_ax(country_abbr, ax, country_songs_count):
            country_artists = {}

            for song in favorite_songs:
                artist_country = song[6]
                if artist_country == country_abbr:
                    artist_name = song[1]
                    country_artists[artist_name] = country_artists.get(artist_name, 0) + 1

            sorted_artists = sorted(country_artists.items(), key=lambda x: x[1], reverse=True)

            counts = [count for _, count in sorted_artists]
            pie_labels = ['' for _ in sorted_artists]

            ax.pie(counts, labels=pie_labels, startangle=90)

            country = pycountry.countries.get(alpha_2=country_abbr)
            title_country = country.name if country else country_abbr
            n = country_songs_count[country_abbr]

            ax.set_title(f"{title_country} ({n} {'song' if n == 1 else 'songs'})")

        # --- Comptage des pays ---
        country_abbrs = set(song[6] for song in favorite_songs)

        country_songs_count = {
            abbr: sum(song[6] == abbr for song in favorite_songs)
            for abbr in country_abbrs
        }

        sorted_countries = sorted(
            country_abbrs,
            key=lambda x: country_songs_count[x],
            reverse=True
        )

        num_countries = len(sorted_countries)
        num_cols = math.ceil(math.sqrt(num_countries))
        num_rows = math.ceil(num_countries / num_cols)

        fig, axes = plt.subplots(
            num_rows,
            num_cols,
            figsize=(5 * num_cols, 4 * num_rows),
            constrained_layout=True
        )

        axes = axes.flatten() if num_countries > 1 else [axes]

        for i, country_abbr in enumerate(sorted_countries):
            draw_artists_pie_chart_by_country_and_ax(
                country_abbr,
                axes[i],
                country_songs_count
            )

        for j in range(num_countries, len(axes)):
            fig.delaxes(axes[j])

        if is_save:
            plt.savefig("images/pie_charts_artists_by_country.png")

        if is_show:
            plt.show()

        plt.close(fig)