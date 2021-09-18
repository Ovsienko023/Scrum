class EstimationTime:
    def __init__(self, seconds):
        self._seconds = seconds

    def make_estimation(self):
        month, week, day, hour, sec = 0, 0, 0, 0, 0
        for _ in range(1, self._seconds+1):
            sec += 1
            if sec == 3600:
                hour += 1
                sec = 0

            if hour == 8:
                day += 1
                sec, hour = 0, 0

            if day == 5:
                week += 1
                sec, hour, day = 0, 0, 0

            if week == 4:
                month += 1
                sec, hour, day, week = 0, 0, 0, 0

        return f"{month}m{week}w{day}d{hour}h"


a = EstimationTime(144_000)
print(a.make_estimation())
