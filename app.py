from pygame import mixer
import keyboard as kb
import sys
from rich.layout import Layout
from rich.align import Align
from rich.panel import Panel
from rich.live import Live

player = mixer
default_config = {"graph_width": 70, "panel_border": "#d600ff"}


def exit_player():
    player.music.stop()
    sys.exit()


def user_controls():
    kb.add_hotkey("p", lambda: player.music.pause())

    kb.add_hotkey("r", lambda: player.music.unpause())

    # kb.add_hotkey("q", exit_player)


def draw_ui(layout):

    layout.split(
        Layout(name="header", size=3),
        Layout(
            name="main",
            size=7,
        ),
        Layout(name="footer", size=3),
    )

    layout["header"].update(
        Panel(
            Align.center("[bold][yellow]Python CLI Audio Player[/yellow][/bold]"),
            border_style=default_config["panel_border"],
        )
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


def main():
    layout = Layout()
    draw_ui(layout)
    # Starting the mixer
    player.init()

    # Loading the song
    player.music.load("./sample-music/my-lofi-morning-music-ig-version-60s-9651.mp3")

    # Setting the volume
    player.music.set_volume(0.7)

    # Start playing the song
    player.music.play()
    # infinite loop
    with Live(layout, refresh_per_second=10, screen=True):
        while True:
            user_controls()
            if kb.is_pressed("q"):
                player.music.stop()
                break


if __name__ == "__main__":
    main()
