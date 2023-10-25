class Scheduler:
    def __init__(self):
        self.schedule = {}

    def add_event(self, date, event):
        if date in self.schedule:
            self.schedule[date].append(event)
        else:
            self.schedule[date] = [event]

    def get_events(self, date):
        return self.schedule.get(date, [])