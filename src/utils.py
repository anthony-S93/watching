import time
import curses
import textwrap
import subprocess
from typing import List

# 10000 x 300 should be enough for most use cases
MAX_LINES = 10000
MAX_COLS  = 300


class Session:
    def __init__(self, cmd: List[str], interval: float, *, no_title=False, wrap=True) -> None:
        # Data
        self.__cmd = cmd
        self.__active = True
        self.__interval = interval
        self.__no_title = no_title
        self.__wrap = wrap
        
        # The main screen
        self.__stdscr = curses.initscr()
        self.__stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0) # Hide cursor

        # Create a pad large enough to hold all contents
        self.__content_pad = curses.newpad(MAX_LINES, MAX_COLS)

        if not self.__no_title:
            # Create a pad to hold the heading
            self.__title_pad = curses.newpad(1, 1000)

            # Initialize heading string
            self.__title_pad.addstr(f"Every {self.__interval}s: {' '.join(self.__cmd)}")
        
        # Initial top position is at line 0 of the pad
        self.__top = 0
    
    def deactivate(self) -> None:
        self.__active = False

    def terminate(self) -> None:
        self.deactivate()
        # Restore terminal properties
        self.__stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def get_key_press(self):
        return self.__content_pad.getch()

    def get_interval(self):
        return self.__interval

    def refresh_screen(self) -> None:
        height, width = self.__stdscr.getmaxyx()
        if not self.__no_title:
            self.__title_pad.refresh(0, 0, 0, 0, 1, width - 1)
            content_pad_start_row = 2
        else:
            content_pad_start_row = 0
        self.__content_pad.refresh(self.__top, 0, content_pad_start_row, 0, height - 1, width - 1)

    def scroll(self, line_increment: int) -> None:
        if self.__active:
            pad_height, _ = self.__content_pad.getmaxyx()
            newtop = self.__top + line_increment
            if (newtop >= 0) and (newtop < pad_height):
                self.__top = newtop
                self.refresh_screen()

    def update_content(self) -> None:
        try:
            if self.__active:
                p = subprocess.run(self.__cmd, capture_output=True)
                if p.returncode == 0:
                    _, width = self.__stdscr.getmaxyx()
                    output_lines = p.stdout.decode().splitlines(True)
                    printed_lines = Session.get_lines_to_be_displayed(output_lines, width=width, wrap=self.__wrap)
                    self.__content_pad.erase() # Clear previous contents
                    self.__content_pad.addstr(0, 0, "".join(printed_lines))
                    self.refresh_screen()
                else:
                    raise Exception()
        except Exception:
            self.deactivate()
            self.__content_pad.erase() # Clear previous contents
            self.__content_pad.addstr(0, 0, f"Something went wrong. The command has a non-zero exit code.\nPress 'q' to quit.")
            self.refresh_screen()

    @staticmethod
    def get_lines_to_be_displayed(output_lines: List[str], *, width: int, wrap=True) -> List[str]:
        lines = []
        if wrap:
            for line in output_lines:
                if line != "\n":
                    # Must add "\n" to each line because textwrap.wrap() removes them.
                    lines.extend([s + "\n" for s in textwrap.wrap(line.rstrip(), width=width)])
                else:
                    lines.append(line) # Keep empty lines
        else:
            lines = output_lines
        return lines


def refresh_cmd(session: Session) -> None:
    while True:
        session.update_content()
        time.sleep(session.get_interval())


def is_float(s) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False
