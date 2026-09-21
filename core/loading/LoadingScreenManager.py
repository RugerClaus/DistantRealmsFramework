

class LoadingScreenManager:

    def __init__(self, system):

        self.system = system
        self.font = self.system.font.get_font(25)
    def draw(
        self,
        text_string,
        progress=None,
        elapsed=None
    ):

        import math

        # ---------------------------------------------------------
        # Animated text
        # ---------------------------------------------------------

        t = self.system.time.get_current_time() / 500
        pulse = (math.sin(t) + 1) / 2

        dark = 40
        light = 255

        fade_color = (
            int(dark + (light - dark) * pulse),
            int(dark + (light - dark) * pulse),
            int(dark + (light - dark) * pulse),
        )

        # ---------------------------------------------------------
        # Main loading text
        # ---------------------------------------------------------

        text = self.font.render(
            text_string,
            True,
            fade_color
        )

        rect = text.get_rect(
            center=(
                self.system.window.get_width() // 2,
                self.system.window.get_height() // 2
            )
        )

        self.system.window.blit(
            text,
            rect
        )

        # ---------------------------------------------------------
        # Progress
        # ---------------------------------------------------------

        if progress is not None:

            progress = max(
                0.0,
                min(1.0, progress)
            )

            self.draw_progress_bar(
                progress,
                rect.bottom + 40
            )

        # ---------------------------------------------------------
        # Elapsed time
        # ---------------------------------------------------------

        if elapsed is not None:

            time_text = self.font.render(
                f"{elapsed:.2f}s",
                True,
                (160, 160, 160)
            )

            time_rect = time_text.get_rect(
                center=(
                    self.system.window.get_width() // 2,
                    rect.bottom + (
                        100 if progress is not None
                        else 50
                    )
                )
            )

            self.system.window.blit(
                time_text,
                time_rect
            )

    def draw_progress_bar(
        self,
        progress,
        y
    ):

        window_width = (
            self.system.window.get_width()
        )

        bar_width = int(
            window_width * 0.5
        )

        bar_height = 20

        x = (
            window_width - bar_width
        ) // 2

        # Background

        self.system.window.draw_rect(
            (
                x,
                y,
                bar_width,
                bar_height
            ),
            (60, 60, 60)
        )

        # Filled portion

        fill_width = int(
            bar_width * progress
        )

        if fill_width > 0:

            self.system.window.draw_rect(
                (
                    x,
                    y,
                    fill_width,
                    bar_height
                ),
                (220, 220, 220)
            )