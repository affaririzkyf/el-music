import discord

current_filter = "normal"

FILTERS = {

    "normal": (
        "volume=1"
    ),

    "bassboost": (
        "bass=g=8,"
        "treble=g=2"
    ),

    "nightcore": (
        "asetrate=48000*1.15,"
        "atempo=1.1,"
        "bass=g=4"
    ),

    "vaporwave": (
        "asetrate=48000*0.8,"
        "atempo=0.9,"
        "bass=g=3"
    ),

    "clear": (
        "bass=g=4,"
        "treble=g=3,"
        "acompressor"
    )
}

def set_filter(filter_name):

    global current_filter

    if filter_name in FILTERS:

        current_filter = filter_name

        return True

    return False

def create_source(url):

    ffmpeg_options = {

        "before_options": (

            "-reconnect 1 "

            "-reconnect_streamed 1 "

            "-reconnect_delay_max 10 "

            "-reconnect_on_network_error 1 "

            "-reconnect_on_http_error 4xx,5xx "

            "-reconnect_delay_total_max 30"
        ),

        "options": (
            f"-vn -bufsize 256k "
            f"-af '{FILTERS[current_filter]}'"
        )
    }

    return discord.FFmpegPCMAudio(

        url,

        executable="ffmpeg",

        **ffmpeg_options
    )