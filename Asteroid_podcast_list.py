import random

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import client_id, client_secret

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)


# 🎙️ Function to search for podcasts based on a topic
def search_podcasts(topic, num_results=5):
    """
    Searches for podcast episodes on Spotify about a topic.
    :param topic: The word(s) you want to search for (e.g., "technology").
    """

    print(f"\nSearching for podcast episodes about {topic}:\n")

    # Asks Spotify for podcast episodes about the topic
    results = sp.search(q=topic, type="episode", limit=20)

    # Check if results were found
    if "episodes" in results and results["episodes"]["items"]:
        episodes = results["episodes"]["items"]

        random.shuffle(episodes)

        selected_episodes = episodes[:num_results]

        # Loop through each episode and print details
        for idx, episode in enumerate(selected_episodes, start=1):
            print(f"{idx}. {episode['name']}")
            print(f"{episode['description'][:100]}...")  # Show first 100 characters of description
            print(f"Listen here: {episode['external_urls']['spotify']}\n")
    else:
        print(f"No podcast episodes found for {topic}.")


# Hardcoded topic
topic = "asteroids"

# 🔎 Run the search function with the user's input
search_podcasts(topic)

if __name__ == "__main__":
    topic = input("Enter a topic to search for podcasts: ").strip()
    search_podcasts(topic)