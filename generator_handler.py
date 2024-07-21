class GeneratorHandler:
    def __init__(self, total_rows):
        self.total_rows = total_rows
        self.level_cursor = 0
        self.current_line = 0
        self.level_ticket = None
        self.materi_ticket = None

    def progress(self):
        progress = self.current_line / self.total_rows * 100
        self.current_line += 1

        return progress

    def check_level(self, level):
        if self.level_cursor != level:
            self.level_cursor = level
            return True

        return False
