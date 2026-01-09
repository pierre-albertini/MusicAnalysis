from gen_Spotify import SpotifyData
from graphs import Graph

if __name__ == "__main__":
    spotify_data = SpotifyData()

    if spotify_data.sp:
        spotify_data.get_user_data()
        spotify_data.load_spotify_favorite_songs()

        graph = Graph(spotify_data)

        graph.draw_top_artists(30,is_show=False)
        graph.draw_artist_histogram(is_show=False)
        graph.draw_duration_histogram(is_show=False)
        graph.draw_countries_by_songs(is_show=False)
        graph.draw_countries_by_unique_artists(is_show=False)

        graph.draw_artists_pie_chart_by_country("Unknown", is_show=False)
        graph.draw_histogram_by_release_year(is_show=False)
        graph.draw_histogram_by_add_time("hour",is_show=False)

        graph.draw_duration_vs_release_year(is_show=False)

        graph.draw_pie_charts_for_all_countries(is_save=True, is_show=False)

        #graph.print_data()
        #graph.display_artists_by_country("US")

    else:
        print("Failed to set up Spotify API client.")


