import os
import yt_dlp

def search_and_download_song(song_name, output_path='downloads'):
    try:
        os.makedirs(output_path, exist_ok=True)

        # Gunakan ytsearch untuk pencarian awal
        temp_ydl_opts = {
            'default_search': 'ytsearch1',
            'quiet': True,
            'skip_download': True,
        }

        with yt_dlp.YoutubeDL(temp_ydl_opts) as temp_ydl:
            info = temp_ydl.extract_info(song_name, download=False)
            if 'entries' in info:
                video_info = info['entries'][0]
            else:
                video_info = info
            title = video_info.get('title', 'unknown_title')
            output_filename = os.path.join(output_path, f"{title}.mp3")

        # Cek jika file sudah ada
        if os.path.exists(output_filename):
            return {"status": "exists", "filename": os.path.basename(output_filename)}

        # Opsi unduh MP3 dengan pencarian
        ydl_opts = {
            'format': 'bestaudio/best',
            'default_search': 'ytsearch1',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([song_name])

        return {"status": "success", "filename": os.path.basename(output_filename)}

    except Exception as e:
        return {"status": "error", "message": str(e)}
