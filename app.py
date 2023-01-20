from pygame import mixer
from mutagen.mp3 import MP3
import keyboard as kb
import sys, time, os
from rich.layout import Layout
from rich.align import Align
from rich.panel import Panel
from rich.live import Live
from rich.spinner import Spinner, SPINNERS
from rich.columns import Columns
from rich.text import Text

# from rich.progress import Progress
# from rich.progress import track

import random

# import FFT

all_spinners = Columns(
    [
        Spinner(spinner_name, text=Text(repr(spinner_name), style="green"))
        for spinner_name in sorted(SPINNERS)
    ],
    column_first=True,
    expand=True,
)

player = mixer
default_config = {"graph_width": 70, "panel_border": "#d600ff"}

frame1 = [
    ".:^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^:.    ",
    ".^^^^^^^^^^^^^^^^^^^^^^:::::^^^^^^^^^^^^^^^^^^^^^.",
    ":^^^^^^^^^^^^^^^:...            ..:^^^^^^^^^^^^^^^",
    ":^^^^^^^^^^^::..                     .:^^^!PPPY^^^",
    ":^^^^^^^^^:.:~:                         :^7GGG5^^^",
    ":^^^^^^^::~~~^:..                         ~BGG5^^^",
    ":^^^^^^.~5Y7^:::^.                        .5PPY^^^",
    ":^^^^^.~??!^!!~^:..                         ^~^^^^",
    ":^^^^.?5?^:~!!!:::..  .^!7!~.               ^:^^^^",
    ":^^^:^YJ7:77!~.:^:..?#@@@@@@@&Y.           .^ .^^^",
    ":^^^.~~~.^^~~::^: :#@@@@@@@@@@@@^         .^  .^^^",
    ":^^^.~~^.^:::.....B@@@@@@@@@@@@@&        ::    :^^",
    ":^^^.. ..        .&@@@@@@@@@@@@@@. .....:^::::::^^",
    ":^^^.             J@@@@@@@@@@@@@Y .:::^^^^^^~~^^^^",
    ":^^^.              7&@@@@@@@@@&7 .:^^^^~!77777:^^^",
    ":^^^^.               ~YB#&#B5~  .:^^^^^~7?JYP?:^^^",
    ":^^^^:                          .::^~!7?7!7?7^^^^^",
    ":^^^^^^.                         .:::~7?Y5Y~:^^^^^",
    ":^^^^^^^.                         .^^^^!?J!^^^^^^^",
    ":^^^^^^^^:.                        .:~~^^:^^^^^^^^",
    ":^^^^^^^^^^^.                       .:^^^^^^^^^^^^",
    ":^^^^^^^^^^^^^^:.                 ..:^^^^^^^^^^^^^",
    ".^^^^^^^^^^^^^^^^^^::.........::^^^^^^^^^^^^^^^^^.",
    "  .^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^:  ",
]

frame2 = [
    ".:^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^:.    ",
    ".^^^^^^^^^^^^^^^^^^^^:::::::::^^^^^^^^^^^^^^^^^^^.",
    ":^^^^^^^^^^^^^^^::::~7?!!!?Y7~^::::^^^^^^^^^^^^^^^",
    ":^^^^^^^^^^^^:..~~^!7?J7~!?J7!^^!^. ..:^^^!PPPY^^^",
    ":^^^^^^^^^:.   .:^::^~7!~~77~^:^:.     .:^7GGG5^^^",
    ":^^^^^^^:.       .^::~!!^^!!^:^:          ~BGG5^^^",
    ":^^^^^^.          .:..:^::^^:..           .5PPY^^^",
    ":^^^^^.             ...:......              ^~^^^^",
    ":^^^^.                .~!77~:               ^:^^^^",
    ":^^^:              .?#@@@@@@@&5.            ^ .^^^",
    ":^^^.             :#@@@@@@@@@@@@~         .:   ^^^",
    ":^^^             .B@@@@@@@@@@@@@@.       ::    :^^",
    ":^^^             .&@@@@@@@@@@@@@@.      :.     :^^",
    ":^^^.             ?@@@@@@@@@@@@@5     .^.      ^^^",
    ":^^^.              !&@@@@@@@@@&7    .^~:      .^^^",
    ":^^^^.               ~YG#&#BY~     .^^.       :^^^",
    ":^^^^:                 ........              :^^^^",
    ":^^^^^^.             ..:^::^^:..            :^^^^^",
    ":^^^^^^^.          .:::^~^^~~^:::.        .^^^^^^^",
    ":^^^^^^^^:.       .:^:~!?!~!?!~:^^..    .:^^^^^^^^",
    ":^^^^^^^^^^^..   .^^:^~!7~^~?7!~^~!:...:^^^^^^^^^^",
    ":^^^^^^^^^^^^^^:.:~^^7J55?77YPJ7^^^^:^^^^^^^^^^^^^",
    ".^^^^^^^^^^^^^^^^^^::^^!!^^^~~^^^^^^^^^^^^^^^^^^^.",
    "  .^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^:  ",
]

frame3 = [
    ".:^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^:.    ",
    ".^^^^^^^^^^^^^^^^^^^^^^::::::^^^^^^^^^^^^^^^^^^^^.",
    ":^^^^^^^^^^^^^^^:...         .:^::::^^^^^^^^^^^^^^",
    ":^^^^^^^^^^^^:.              .~~^~7?!^:^^^!PPPY^^^",
    ":^^^^^^^^^:.                 :^:^!?55?!^::7GGG5^^^",
    ":^^^^^^^:.                   ^::~7J7!!?Y5!!GGG5^^^",
    ":^^^^^^.                    .::^!7~~!JYJJ?75PPY^^^",
    ":^^^^^.                     ..:~^^~!7!!~^^~!~~^^^^",
    ":^^^^.                .^!77~:...:^~~^::^^^::^:^^^^",
    ":^^^:              .?#@@@@@@@&5. :......   .^..^^^",
    ":^^^.             :#@@@@@@@@@@@@!         .:   ^^^",
    ":^^^             .B@@@@@@@@@@@@@@.       ::    :^^",
    ":^^^             .#@@@@@@@@@@@@@@:      :.     :^^",
    ":^^^.             ?@@@@@@@@@@@@@G     .^.      ^^^",
    ":^^^.        . ....!&@@@@@@@@@@J    .^~:      .^^^",
    ":^^^^.  ...:::..:^:..~YB#&#B5!     .^^.       :^^^",
    ":^^^^:.~~^.:^~~~:::^:.                       :^^^^",
    ":^^^^^::~!!~^!7!~^^::..                     :^^^^^",
    ":^^^^^^^:!55J~:^!?!~::.                   .^^^^^^^",
    ":^^^^^^^^:~77777!~^::^.                  :^^^^^^^^",
    ":^^^^^^^^^^::~JPJ7^:^:.               .:^^^^^^^^^^",
    ":^^^^^^^^^^^^^^^^^^~!.            ..:^^^^^^^^^^^^^",
    ".^^^^^^^^^^^^^^^^^^^^::.......::^^^^^^^^^^^^^^^^^.",
    "  .^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^:  ",
]

frame4 = [
    ".:^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^:.    ",
    ".^^^^^^^^^^^^^^^^^^^^^^:::::^^^^^^^^^^^^^^^^^^^^^.",
    ":^^^^^^^^^^^^^^^:...            ..:^^^^^^^^^^^^^^^",
    ":^^^^^^^^^^^^:.                      .:^^^!PPPY^^^",
    ":^^^^^^^^^:.                           .:^7GGG5^^^",
    ":^^^^^^^:.                               .~GGG5^^^",
    ":^^^^^^.                                 .~PPPY^^^",
    ":^^^^^.                               .:^~~~~^^^^^",
    ":^^^^..               .^!7!~.       .::^^^~!~^^^^^",
    ":^^^::~^...        .?#@@@@@@@&5.  ..::^~!?J7~J^^^^",
    ":^^^.~~~.:^:...   :#@@@@@@@@@@@@! ::^~!!!77~!?^^^^",
    ":^^^:J?!.~~^^.::..B@@@@@@@@@@@@@@. :^^~~~^!7?Y7:^^",
    ":^^:^PY?:77!~.^:..#@@@@@@@@@@@@@@: :^^~!~~??J5J:^^",
    ":^^^.?7!.~!~~.^^: ?@@@@@@@@@@@@@G  ..:^^^^^~~!^^^^",
    ":^^^.75Y~^7!!:.:.. !&@@@@@@@@@@Y    .^^:.:^^~!:^^^",
    ":^^^^^5?7.:^::...    ~YB#&&#P!.    .^^.    ..:^^^^",
    ":^^^^::~~~.::.                               :^^^^",
    ":^^^^^::~^.                                 :^^^^^",
    ":^^^^^^^..                                .^^^^^^^",
    ":^^^^^^^^:.                              :^^^^^^^^",
    ":^^^^^^^^^^^.                         .:^^^^^^^^^^",
    ":^^^^^^^^^^^^^^:.                 ..:^^^^^^^^^^^^^",
    ".^^^^^^^^^^^^^^^^^^::.........::^^^^^^^^^^^^^^^^^.",
    "  .^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^:  ",
]
frame5 = [
    ".:^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^:.    ",
    ".^^^^^^^^^^^^^^^^^^^^^^::::::^^^^^^^^^^^^^^^^^^^^.",
    ":^^^^^^^^^^^^^^^:...            ..:^^^^^^^^^^^^^^^",
    ":^^^^^^^^^^^:::..                    .:^^^!PPPY^^^",
    ":^^^^^^^^^:::^~~.                       :^7GGG5^^^",
    ":^^^^^^^::?J?~::::                        ~BGG5^^^",
    ":^^^^^^.^7YJ~^~^:^.                       .5PPY^^^",
    ":^^^^^.7J?~:^77!^...                        ^~^^^^",
    ":^^^^.!5Y!^7!~^::^:.  .^!7!^.               ^:^^^^",
    ":^^^::!~~.~!!!.:::..?#@@@@@@@&5.           .^ .^^^",
    ":^^^.~~~.:^::..::.:#@@@@@@@@@@@@~         .:   ^^^",
    ":^^^............ .B@@@@@@@@@@@@@@.       ::    :^^",
    ":^^^.            .#@@@@@@@@@@@@@@:      ::     :^^",
    ":^^^.             ?@@@@@@@@@@@@@G ...::^^:^:^^:^^^",
    ":^^^.              !&@@@@@@@@@@Y .:^^^^^^^^^~~:^^^",
    ":^^^^.               ~YB#&&#P!. :^^^^^~7??7??^:^^^",
    ":^^^^:                         ..:~!!!~!7?JPJ:^^^^",
    ":^^^^^^.                       .:::^!?J?77?~:^^^^^",
    ":^^^^^^^.                        :^:~!?YPJ^:^^^^^^",
    ":^^^^^^^^^.                      .:~^~!7!^^^^^^^^^",
    ":^^^^^^^^^^^.                     .:!^::^^^^^^^^^^",
    ":^^^^^^^^^^^^^^:.                ..:^^^^^^^^^^^^^^",
    ".^^^^^^^^^^^^^^^^^^::.........::^^^^^^^^^^^^^^^^^.",
    "  .^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^:  ",
]

frames = [frame1, frame2, frame3, frame4]


def exit_player():
    player.music.stop()
    os._exit(0)


def user_controls():
    kb.add_hotkey("p", lambda: player.music.pause())

    kb.add_hotkey("r", lambda: player.music.unpause())

    kb.add_hotkey("q", exit_player)


def disk_animate(layout, state):
    if state == "playing":
        for frame in frames:
            layout["disk"].update(
                Panel(
                    Align.center("\n".join(frame), vertical="middle"),
                    border_style=default_config["panel_border"],
                )
            )
            time.sleep(0.2)
    else:
        layout["disk"].update(
            Panel(
                Align.center("\n".join(frame1), vertical="middle"),
                border_style=default_config["panel_border"],
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
            Align.center("[bold][yellow] ♪ Python CLI Audio Player[/yellow][/bold]"),
            border_style=default_config["panel_border"],
        )
    )

    layout["main"].split_row(Layout(name="disk"), Layout(name="player", ratio=2))

    layout["disk"].minimum_size = 20
    layout["disk"].update(
        Panel(
            Align.center("\n".join(frame1), vertical="middle"),
            border_style=default_config["panel_border"],
        )
    )

    layout["player"].split_column(
        Layout(name="song_name", size=3),
        Layout(name="spectro", size=15),
        Layout(name="media_buttons", size=3),
        Layout(name="seek_bar", size=3),
    )

    layout["footer"].update(
        Panel(
            Align.center(
                "[bold][yellow](P)lay/Pause (S)top (Q)uit (F)orward (B)ackward [/yellow][/bold]"
            ),
            title="Controls",
            border_style=default_config["panel_border"],
        )
    )
    return layout


def time_format(seconds):
    # to convert int seconds to mm:ss format
    minutes = seconds // 60
    return "%02d:%02d" % (minutes, seconds % 60)


def spectrogram(sz):
    # ch = "█"
    ch = "▒"
    if len(sz) == 0:
        return ""
    sz = np.abs(np.int_(sz))
    mn, mx = min(sz), max(sz)
    df = (mx - mn) // 8
    # print(df)
    bkt = [(el - mn) // df for el in sz]
    # print(bkt)
    hrz = [f"{b}{c}" for b, c in [(ch * (el + 1), " " * (8 - el)) for el in bkt]]

    # hrz = [f"{b}{c}" for b, c in [(ch * (el + 1), " " * (8 - el)) for el in bkt]]
    return "\n".join([" ".join(el) for el in list(map(list, zip(*hrz)))[::-1]])


from scipy.io.wavfile import read
import numpy as np


sampleRate, audioBuffer = read("./temp.wav")
duration = len(audioBuffer) / sampleRate
time_w = np.arange(0, duration, 1 / sampleRate)  # time vector

audioBuffer = audioBuffer.sum(axis=1) / 2


def main():
    layout = Layout()
    layout = draw_ui(layout)

    # Starting the mixer
    player.init()

    # Loading the song
    song_file = "./sample-music/my-lofi-morning-music-ig-version-60s-9651.mp3"
    s = player.music.load(song_file)
    song_meta = MP3(song_file)
    song_length = song_meta.info.length
    # Setting the volume
    player.music.set_volume(0.7)

    # Start playing the song
    player.music.play()
    # infinite loop
    user_controls()
    print(song_meta)
    # with Progress() as progress:
    #     # seek_bar = Progress()
    #     # seek_bar_task = seek_bar.add_task("song", total=int(song_length))
    #     task1 = progress.add_task("song", total=int(song_length))
    #     layout["seek_bar"].update(
    #         progress.update(task1, completed=int(player.music.get_pos() / 1000))
    #     )
    # layout["seek_bar"].update(
    #     # Panel.fit(
    #     #     seek_bar.update(seek_bar_task, completed=int(player.music.get_pos() / 1000))
    #     # )
    # )
    # layout["seek_bar"].update(Panel.fit(str(player.music.get_pos())))
    with Live(layout, refresh_per_second=25, screen=True) as live:
        while True:
            # layout["disk"].update(Panel("test " + str(frame)))
            # layout["disk"].update(disk_animate(layout, "playing"))
            # frame = frame + 1
            # layout["seek_bar"].update(
            #     Panel.fit(
            #         seek_bar.update(seek_bar_task, advance=player.music.get_pos())
            #     )
            #     # Panel.fit(seek_bar.advance(seek_bar_task))
            # )
            curr_pos = int(player.music.get_pos() / 1000)
            seek_percent = int(curr_pos * 100 / song_length)

            seek_bar_str = (
                "[green]━" * int(seek_percent)
                + "[white]|"
                + "[red]━" * (100 - int(seek_percent))
            )
            amp = []
            curr_ms = int(player.music.get_pos() * sampleRate / 1000)
            # amp = audioBuffer[-100 : curr_pos * sampleRate]
            # amp = amp[-25::]
            # for i in range(curr_ms, -100):
            # amp.append(audioBuffer[i])
            amp.append(audioBuffer[curr_ms])
            amp = [random.randint(10, 99) for _ in range(25)]
            amp = audioBuffer[curr_ms : curr_ms + 100 : 5]
            layout["spectro"].update(Panel(spectrogram(amp)))

            layout["media_buttons"].update(
                Panel(
                    f"{str(player.music.get_pos())}  {str(audioBuffer[curr_ms])} {str(time_w[curr_ms])}"
                )
            )

            layout["seek_bar"].update(
                # Panel.fit(print(f"{str(curr_pos)} {seek_bar_str} {str(song_length)}"))
                Panel(
                    Align.center(
                        f"{time_format(curr_pos)} {seek_bar_str} {time_format(song_length)}"
                    )
                )
            )
            disk_animate(layout, "playing")
            # layout["player"].update(Panel(all_spinners))
            # if kb.is_pressed("q"):
            #     player.music.stop()
            #     break


if __name__ == "__main__":
    main()
