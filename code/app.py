import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors
import spotipy
from spotipy import SpotifyClientCredentials, SpotifyOAuth
import tkinter as tk
from tkinter import messagebox
import pprint

# Authentication - replace with your actual client ID and secret
client_id = 'acfcc7158efc4a50a48deb112e838428'
client_secret = 'c08a8971713e4086899a36007b35c897'
redirect_uri = 'http://localhost:8888/callback'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="user-library-read"))

# Load dataset and preprocess
df = pd.read_csv('dataset.csv')
df = df.dropna()
df = df.drop_duplicates(subset="track_id")
df = df.drop_duplicates(subset=["track_name", "artists"])

features = ['duration_ms', 'explicit', 'danceability', 'energy', 'loudness', 'mode',
            'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']

scaler = StandardScaler()
df[features] = scaler.fit_transform(df[features])

le = LabelEncoder()
df['track_genre'] = le.fit_transform(df['track_genre'].astype(str))

X = df[features].values
k = 2000
model = NearestNeighbors(n_neighbors=k, algorithm='auto').fit(X)

# Function to get song name by ID from Spotify
def get_song_name_by_id(song_id):
    try:
        track = sp.track(song_id)
        return track['name']
    except spotipy.exceptions.SpotifyException as e:
        return f"An error occurred: {e}"

# Function to recommend songs based on NearestNeighbors model
def recommend_songs(track_id, df, model, features):
    data = df.copy()
    idx = data.index[data['track_id'] == track_id].tolist()
    if not idx:
        return []
    idx = idx[0]
    input_features = data.loc[idx, features].values.reshape(1, -1)

    distances, indices = model.kneighbors(input_features)
    recommendations = data.iloc[indices[0]].copy()
    recommendations['distance'] = distances[0]
    recommendations = recommendations[recommendations['track_genre'] == df['track_genre'][idx]]
    return recommendations[:10]

# Function to get recommendations from Spotify API
def get_recommendations_by_song_id(song_id, limit=10):
    recommendations = sp.recommendations(seed_tracks=[song_id], limit=limit)
    recommended_tracks = []

    for track in recommendations['tracks']:
        track_id = track['id']
        track_info = sp.track(track_id)
        track_features = sp.audio_features(track_id)[0]

        album_info = sp.album(track_info['album']['id'])
        genres = album_info['genres'] if album_info['genres'] else sp.artist(track_info['artists'][0]['id'])['genres']

        track_data = {
            'track_id': track_id,
            'artists': ', '.join([artist['name'] for artist in track_info['artists']]),
            'album_name': track_info['album']['name'],
            'track_name': track_info['name'],
            'popularity': track_info['popularity'],
            'duration_ms': track_info['duration_ms'],
            'explicit': track_info['explicit'],
            'danceability': track_features['danceability'],
            'energy': track_features['energy'],
            'loudness': track_features['loudness'],
            'mode': track_features['mode'],
            'speechiness': track_features['speechiness'],
            'acousticness': track_features['acousticness'],
            'instrumentalness': track_features['instrumentalness'],
            'liveness': track_features['liveness'],
            'valence': track_features['valence'],
            'tempo': track_features['tempo'],
            'time_signature': track_features['time_signature'],
            'track_genre': ', '.join(genres)
        }

        recommended_tracks.append(track_data)

    return recommended_tracks

# Function to calculate loss between two recommendation systems
def calculate_loss(recommendations1, recommendations2, features):
    df1 = pd.DataFrame(recommendations1)

    df2 = pd.DataFrame(recommendations2)
    scaler = StandardScaler()
    df2[features] = scaler.fit_transform(df2[features])

    le = LabelEncoder()
    df2['track_genre'] = le.fit_transform(df2['track_genre'].astype(str))

    # Calculate mean values for each feature
    mean1 = df1[features].mean()
    mean2 = df2[features].mean()

    # Calculate the loss as the mean squared difference
    loss = np.mean((mean1 - mean2) ** 2)

    return loss

# GUI setup
def show_recommendations():
    track_id = entry_track_id.get()
    recommendations1 = recommend_songs(track_id, df, model, features)
    recommendations2 = get_recommendations_by_song_id(track_id)
    
    if recommendations1.empty or not recommendations2:
        messagebox.showerror("Error", "Song ID not found or recommendations not available.")
        return
    
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Recommendations for {get_song_name_by_id(track_id)} from NearestNeighbors model:\n\n")
    result_text.insert(tk.END, recommendations1[['track_name', 'artists', 'distance']].to_string(index=False))

    # Calculate and display loss
    loss = calculate_loss(recommendations1.to_dict('records'), recommendations2, features)
    result_text.insert(tk.END, f"\n\nLoss between the two recommendation systems: {loss:.2f}")

# Main GUI window
root = tk.Tk()
root.title("Song Recommendation App")

# Widgets
label_track_id = tk.Label(root, text="Enter Track ID:")
label_track_id.pack()

entry_track_id = tk.Entry(root, width=30)
entry_track_id.pack()

btn_recommend = tk.Button(root, text="Recommend Songs", command=show_recommendations)
btn_recommend.pack()

result_text = tk.Text(root, height=20, width=100)
result_text.pack()

root.mainloop()
