from pygame import mixer
from mutagen.mp3 import MP3
import keyboard as kb
import sys, time, os
from rich.layout import Layout
from rich.align import Align
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
import ffmpeg
from rich import box
from scipy.io.wavfile import read
import numpy as np
import json

# from rich.progress import Progress
# from rich.progress import track


player = mixer
# SONG_END = USEREVENT + 1
player_state = None

# load animation disk_frames and media buttons

with open("./utils/ascii_arts.json", "r", encoding="utf8") as f:
    temp = json.load(f)

disk_frames = temp["disk_frames"]
media_buttons_json = temp["media_buttons"]

default_config = {"music_file_location": "./sample-music", "default_vol": 0.5}


default_theme = {
    "panel_border": "#d600ff",
    "spectro_color": "#0FFF50",
}

song_idx = 0
currently_playing = None
music_list = []


def exit_player():
    player.music.stop()
    os._exit(0)


def play_n_pause():
    global player_state
    if player.music.get_busy():
        player.music.pause()
        player_state = None
    else:
        player.music.unpause()
        player_state = "playing"


def next_track():
    global song_idx, currently_playing
    song_idx = music_list.index(currently_playing)
    if song_idx == len(music_list):
        song_idx = 0
    elif song_idx < len(music_list):
        song_idx = song_idx + 1
    if len(music_list) > 0:
        currently_playing = music_list[song_idx]
    # currently_playing = music_list[song_idx]
    player.music.load(currently_playing)
    player.music.play()


def prev_track():
    global song_idx, currently_playing
    song_idx = music_list.index(currently_playing)
    if song_idx == 0:
        song_idx = len(music_list)
    elif song_idx > 0:
        song_idx = song_idx - 1
    if len(music_list) > 0:
        currently_playing = music_list[song_idx]
    player.music.load(currently_playing)
    player.music.play()


def increase_vol():
    curr_vol = player.music.get_volume()
    if curr_vol > 1:
        curr_vol = 1
    else:
        curr_vol = curr_vol + 0.1
    player.music.set_volume(curr_vol)


def decrease_vol():
    curr_vol = player.music.get_volume()
    if curr_vol < 0:
        curr_vol = 0
    else:
        curr_vol = curr_vol - 0.1
    player.music.set_volume(curr_vol)


def user_controls():
    kb.add_hotkey("p", play_n_pause)

    kb.add_hotkey("r", lambda: player.music.rewind())

    kb.add_hotkey("s", lambda: player.music.stop())

    kb.add_hotkey("v", prev_track)

    kb.add_hotkey("n", next_track)

    kb.add_hotkey("+", increase_vol)

    kb.add_hotkey("-", decrease_vol)

    kb.add_hotkey("q", exit_player)


def disk_animate(layout, state):
    curr_frame = disk_frames["frame1"]
    if state == "playing":
        for frame in disk_frames:
            curr_frame = disk_frames[frame]
            layout["disk"].update(
                Panel(
                    Align.center("\n".join(curr_frame), vertical="middle"),
                    border_style=default_theme["panel_border"],
                )
            )
            time.sleep(0.1)
    else:
        layout["disk"].update(
            Panel(
                Align.center("\n".join(curr_frame), vertical="middle"),
                border_style=default_theme["panel_border"],
            )
        )


def draw_ui(layout):

    layout.split(
        Layout(name="header", size=3),
        Layout(
            name="main",
            size=25,
        ),
        Layout(name="footer", size=3),
    )

    layout["header"].update(
        Panel(
            Align.center("[bold][#feff6e] ♪ Python CLI Audio Player[/#feff6e][/bold]"),
            border_style=default_theme["panel_border"],
        )
    )

    layout["main"].split_row(Layout(name="disk"), Layout(name="player", ratio=3))

    # layout["disk"].minimum_size = 20
    layout["disk"].update(
        Panel(
            Align.center("\n".join(disk_frames["frame1"]), vertical="middle"),
            border_style=default_theme["panel_border"],
        )
    )

    layout["player"].split_column(
        Layout(name="now_playing", size=3),
        Layout(name="media_n_spectro", size=22),
        # Layout(name="status_bar", size=3),
        # Layout(name="seek_bar", size=3),
    )

    layout["media_n_spectro"].split_row(
        Layout(name="media_controls"), Layout(name="spectro")
    )
    layout["media_controls"].split_column(
        Layout(name="song_list", size=10), Layout(name="media_buttons")
    )

    layout["media_buttons"].split_column(
        Layout(name="media_big_buttons"), Layout(name="media_user_controls", size=3)
    )

    layout["media_user_controls"].update(
        Panel(
            Align.center(
                "[bold][#feff6e]Pre(v) (P)lay/Pause (S)top (N)ext  (R)epeat  (Q)uit (+)Vol (-)Vol [/#feff6e][/bold]"
            ),
            title="Controls",
            border_style=default_theme["panel_border"],
        )
    )
    layout["footer"].update(
        Panel(
            Align.center(
                "[bold][#feff6e] Created with [#ff2b2b]♥[/#ff2b2b] by [link=https://github.com/Sr-vZ]SrvZ[/link] [/#feff6e][/bold]"
            ),
            # title="Controls",
            border_style=default_theme["panel_border"],
        )
    )
    return layout


def draw_buttons():
    grid = Table.grid(expand=True)

    grid.add_column(justify="center")
    grid.add_column(justify="center")
    grid.add_column(justify="center")
    grid.add_column(justify="center")
    grid.add_column(justify="center")

    play_pause_btn = (
        Panel("\n".join(media_buttons_json["play"]))
        if player_state == "playing"
        else Panel("\n".join(media_buttons_json["pause"]))
    )
    grid.add_row(
        Panel("\n".join(media_buttons_json["prev"])),
        play_pause_btn,
        Panel("\n".join(media_buttons_json["stop"])),
        Panel("\n".join(media_buttons_json["next"])),
        Panel("\n".join(media_buttons_json["repeat"])),
        Panel("\n".join(media_buttons_json["quit"])),
    )

    return grid


def generate_songlist(layout, song_list):
    global currently_playing
    currently_playing_name = currently_playing.split("\\")[-1].replace(".mp3", "")
    table = Table(
        show_lines=False,
        box=box.SIMPLE,
        border_style=default_theme["panel_border"],
    )
    table.add_column("File", justify="left", style="cyan", no_wrap=False)
    table.add_column("Duration", justify="right", style="green")

    for song in song_list:
        song_meta = MP3(song)
        dur = time_format(song_meta.info.length)
        name = song.split("\\")[-1].replace(".mp3", "")
        if name == currently_playing_name:
            table.add_row(name, dur, style="red on white")
        else:
            table.add_row(name, dur)

    return Panel(
        table,
        border_style=default_theme["panel_border"],
        title="[#feff6e]Music Queue",
    )


def time_format(seconds):
    # to convert int seconds to mm:ss format
    minutes = seconds // 60
    return "%02d:%02d" % (minutes, seconds % 60)


def spectrogram(sz):
    ch = "█"
    # ch = "▒"
    if len(sz) == 0:
        return ""
    bar_strength = 10
    sz = np.abs(np.int_(sz))
    mn, mx = min(sz), max(sz)
    df = (mx - mn) // bar_strength
    # print(df)
    bkt = [(el - mn) // df for el in sz]
    # print(bkt)
    hrz = [
        f"{b}{c}" for b, c in [(ch * (el + 1), "⠿" * (bar_strength - el)) for el in bkt]
    ]
    return "\n".join([" ".join(el) for el in list(map(list, zip(*hrz)))[::-1]])


def song_end():
    player_state = None


def audio_processor(currently_playing):
    pass


def main():
    layout = Layout()
    layout = draw_ui(layout)
    global player_state, song_idx, currently_playing, music_list
    player_state = None
    # Starting the mixer
    player.init()

    # Loading the song
    for file in os.listdir(default_config["music_file_location"]):
        if file.endswith(".mp3"):
            music_list.append(os.path.join(default_config["music_file_location"], file))
    # currently_playing = "./sample-music/my-lofi-morning-music-ig-version-60s-9651.mp3"
    currently_playing = music_list[0]
    song_idx = 0
    currently_playing_name = currently_playing.split("\\")[-1].replace(".mp3", "")
    # subprocess.call(["ffmpeg", "-i", currently_playing, "temp.wav"])
    wav_file = f"./temp/{currently_playing_name}.wav"
    if not os.path.isfile(f"./temp/{currently_playing_name}.wav"):
        stream = ffmpeg.input(currently_playing)
        stream = ffmpeg.output(stream, wav_file)
        ffmpeg.run(stream, overwrite_output=True, quiet=True)
    sampleRate, audioBuffer = read(wav_file)
    # duration = len(audioBuffer) / sampleRate
    # time_w = np.arange(0, duration, 1 / sampleRate)  # time vector

    audioBuffer = audioBuffer.sum(axis=1) / 2
    player.music.load(currently_playing)
    for m in music_list:
        if not m == currently_playing:
            player.music.queue(m)

    song_meta = MP3(currently_playing)
    song_length = song_meta.info.length
    # Setting the volume
    player.music.set_volume(default_config["default_vol"])

    # Start playing the song
    player.music.play()
    player_state = "playing"

    user_controls()

    with Live(layout, refresh_per_second=15, screen=True) as live:
        while True:
            layout["song_list"].update(generate_songlist(layout, music_list))
            curr_pos = int(player.music.get_pos() / 1000)
            seek_percent = int(curr_pos * 100 / song_length)

            seek_bar_str = (
                "[#3fff2d]━" * int(seek_percent)
                + "[white]|"
                + "[#ff2b2b]━" * (100 - int(seek_percent))
            )
            curr_vol = player.music.get_volume()
            vol_percent = int(curr_vol * 10)
            vol_bar_str = (
                "[#feff6e]━" * int(vol_percent)
                + "[white]█"
                + "[grey]━" * (10 - int(vol_percent))
            )
            amp = []
            curr_ms = int(player.music.get_pos() * sampleRate / 1000)
            # amp = audioBuffer[-100 : curr_pos * sampleRate]
            # amp = amp[-25::]
            # for i in range(curr_ms, -100):
            # amp.append(audioBuffer[i])
            amp.append(audioBuffer[curr_ms])
            # amp = [random.randint(10, 99) for _ in range(25)]
            amp = audioBuffer[curr_ms : curr_ms + 100 : 3]
            layout["spectro"].update(
                Panel(
                    Align.center(spectrogram(amp), vertical="middle"),
                    border_style=default_theme["panel_border"],
                    style=default_theme["spectro_color"],
                    # style="red on green",
                )
            )

            # Panel(Align.center("\n".join(media_buttons_json["prev"])), border_style="white")

            layout["media_big_buttons"].update(
                Panel(
                    # f"{str(player.music.get_pos())}  {str(audioBuffer[curr_ms])} {str(time_w[curr_ms])}",
                    Align.center(draw_buttons()),
                    border_style=default_theme["panel_border"],
                    style=default_theme["spectro_color"],
                )
            )
            currently_playing_name = currently_playing.split("\\")[-1].replace(
                ".mp3", ""
            )
            layout["now_playing"].update(
                # Panel.fit(print(f"{str(curr_pos)} {seek_bar_str} {str(song_length)}"))
                Panel(
                    # Align.center(currently_playing_name),
                    Align.center(
                        f"{time_format(curr_pos)} {seek_bar_str} {time_format(song_length)}  🔈[white][{vol_bar_str}][/white]"
                    ),
                    title=f"Now Playing : [#feff6e]{currently_playing_name}",
                    border_style=default_theme["panel_border"],
                )
            )
            if player.music.get_busy() == False:
                player_state = None
            else:
                player_state = "playing"

            if curr_pos == -1:
                pass
            disk_animate(layout, player_state)


if __name__ == "__main__":
    main()
