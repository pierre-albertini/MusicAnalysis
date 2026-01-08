from gen_Spotify import SpotifyData
from graphs import Graph

if __name__ == "__main__":
    spotify_data = SpotifyData()

    if spotify_data.sp:
        spotify_data.get_user_data()
        spotify_data.load_spotify_favorite_songs()

        graph = Graph(spotify_data)
        # graph.print_data()
        graph.draw_top_artists(30)
        # graph.draw_artist_histogram()
        # graph.draw_duration_histogram()
        # graph.draw_countries_by_songs()                ### TRES PETIT
        # graph.draw_countries_by_unique_artists()       ### TRES PETIT
        # graph.display_artists_by_country("US")
        # graph.draw_artists_pie_chart_by_country("Unknown")
        # graph.draw_histogram_by_release_year()
        # graph.draw_histogram_by_add_time("hour")

    else:
        print("Failed to set up Spotify API client.")


