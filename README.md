# 🎵 Sorter Spotify

**Sorter Spotify** is a desktop application that allows you to organize your Spotify playlists based on various audio features. Whether you want to sort by energy, danceability, or acousticness, this tool gives you control over your listening experience.

## ✨ Features

*   **Playlist Retrieval**: Automatically fetches all your public and private playlists.
*   **Audio Analysis**: Uses Spotify's API to analyze tracks for:
    *   Danceability 💃
    *   Energy ⚡
    *   Acousticness 🎻
    *   Instrumentalness 🎹
    *   Valence (Mood) 😊
    *   Liveness 🎤
    *   Tempo 🥁
    *   Mode 🎼
*   **Custom Sorting**: Choose which criteria to prioritize when sorting.
*   **Direct Update**: Reorders the tracks directly in your Spotify account.
*   **GUI Interface**: User-friendly interface built with PyQt5.

## 🚀 Installation & Setup

### Prerequisites

*   Python 3.x
*   A Spotify Developer Account

### 1. Clone the Repository

```bash
git clone https://github.com/iangrosssan/Sorter-Spotify.git
cd Sorter-Spotify
```

### 2. Install Dependencies

Install the required Python packages using pip:

```bash
pip install PyQt5 spotipy numpy
```

### 3. Configure Credentials

To access your Spotify account, you need to provide your developer credentials.

1.  Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2.  Create a new app to get your `Client ID` and `Client Secret`.
3.  Create a file named `credenciales.csv` inside the `backend/` folder.
4.  The file should contain a single line with your credentials in the following format:

```text
client_id, client_secret, user_id
```

*Note: The `user_id` is your Spotify username.*

## 🖥️ Usage

Run the application by executing the main script:

```bash
python main.py
```

1.  The application will launch and list your playlists.
2.  Select a playlist and choose your sorting preferences.
3.  The app will process the tracks and update the order on Spotify!

## 🛠️ Technologies Used

*   **Python**: Core programming language.
*   **PyQt5**: For the Graphical User Interface (GUI).
*   **Spotipy**: Lightweight Python library for the Spotify Web API.

## 📌 Roadmap & Status

*   [x] Windows Executable (.exe) support
*   [x] Frontend/Backend separation
*   [ ] **Progress Bar**: Implement thread-based progress tracking (requires QThread).
*   [ ] **Language Sort**:
    *   *Constraint*: Spotify data doesn't provide track language.
    *   *Proposal*: Explore Musixmatch API for lyrics analysis.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.