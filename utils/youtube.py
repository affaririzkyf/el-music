import yt_dlp

YDL_OPTIONS = {

    "format": (
        "bestaudio/best"
    ),

    "noplaylist": True,

    "extractor_args": {

        "youtube": {

            "player_client": [
                "android"
            ]
        }
    }
}

def search_youtube(search):

    with yt_dlp.YoutubeDL(
        YDL_OPTIONS
    ) as ydl:

        info = ydl.extract_info(

            f"ytsearch:{search}",

            download=False
        )

        entry = (
            info["entries"][0]
        )

        song = {

            "url": (
                entry["url"]
            ),

            "title": (
                entry["title"]
            ),

            "thumbnail": (
                entry["thumbnail"]
            ),

            "duration": (
                entry.get(
                    "duration",
                    0
                )
            ),

            "webpage_url": (
                entry.get(
                    "webpage_url",
                    ""
                )
            )
        }

        return song