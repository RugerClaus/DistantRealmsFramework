from core.ui.lefttext import LeftAlignedText
from core.ui.scrollabletext import ScrollableText
from systemlogging import log_error, log_event


class ChangeLog(LeftAlignedText):

    def __init__(self, system):

        super().__init__(
            system,
            font_size=25
        )

        self.system = system

        self.changelog_text = []

        self.max_char_count = 90
        self.max_visible_lines = 15

        changelog_text = self.load_changelog_from_file(
            "changelog.txt"
        )

        self.total_length = (
            sum(len(line) for line in changelog_text)
            if changelog_text
            else 0
        )

        self.scrollable = ScrollableText(
            system,
            font_size=25,
            anchor=(0.05, 0.35),
            width=0.9,
            height=0.45,
            align="left",
            line_spacing=0.01
        )

        self.scrollable.set_text(
            [
                [
                    (
                        line,
                        0.05,
                        (255,255,255)
                    )
                ]
                for line in self.changelog_text
            ]
        )


        log_event(
            f"Changelog loaded successfully. Total length: {self.total_length} characters."
        )


    def load_changelog_from_file(self, file_path):

        try:

            with open(file_path, "r") as f:

                raw_lines = [
                    line.strip()
                    for line in f.readlines()
                ]


                for line in raw_lines:

                    self.changelog_text.extend(
                        self._break_line_into_chunks(line)
                    )


        except FileNotFoundError:

            self.changelog_text = [
                "Changelog not found. Please email dev@snowblitz.net with your error.log,",
                "and event.log from /logs as well as a description of your issue."
            ]

            log_error(
                "Changelog file not found, please send your error and event log files in /logs"
            )


        return self.changelog_text


    def _break_line_into_chunks(self, line):

        words = line.split(" ")

        current_line = ""

        lines = []


        for word in words:

            if len(current_line) + len(word) + 1 > self.max_char_count:

                lines.append(
                    current_line
                )

                current_line = word

            else:

                if current_line:

                    current_line += " " + word

                else:

                    current_line = word


        if current_line:

            lines.append(
                current_line
            )


        return lines


    def draw(self):

        if not self.changelog_text:

            self._draw_left_aligned_text(
                "No changelog available."
            )

            return


        if len(self.changelog_text) > self.max_visible_lines:

            self.scrollable.draw()

        else:

            changelog_content = "\n".join(
                self.changelog_text
            )

            self._draw_left_aligned_text(
                changelog_content
            )


    def scroll(self, amount):

        if len(self.changelog_text) > self.max_visible_lines:

            self.scrollable.scroll(
                amount
            )


    def handle_event(self, event):

        if len(self.changelog_text) > self.max_visible_lines:

            if event.type == self.system.input.mouse_scroll_event():

                self.scroll(
                    -event.y
                )


    def rescale(self):

        self.scrollable.scale()