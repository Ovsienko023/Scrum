class EstimationTime:
    def __init__(self, hours=0):
        self.hours = hours
        self.time_string = self.hours_to_string()

    def __add__(self, obj):
        sum_hours = self.hours + obj.hours
        return EstimationTime(sum_hours)

    def __repr__(self):
        return self.time_string

    def __str__(self):
        return self.time_string

    @staticmethod
    def _delete_zero_value(time_string):
        index = time_string.find('0')
        while index != -1:
            time_string = time_string[:index] + time_string[(index + 2):]
            index = time_string.find('0')
        return time_string

    @staticmethod
    def convert_to_hours(times: str) -> int:
        hours = 0
        numb = ""
        for ind, key in enumerate(times):
            if key.isdigit():
                numb += key
                continue
            if key == "h":
                hours += int(numb)
                numb = ""
                continue
            if key == "d":
                hours += int(numb) * 8
                numb = ""
                continue
            if key == "w":
                hours += int(numb) * 40
                numb = ""
                continue
            if key == "m":
                hours += int(numb) * 160
                numb = ""
                continue

        return hours

    def hours_to_string(self) -> str:
        month, week, day, hour = 0, 0, 0, 0
        for _ in range(1, self.hours + 1):
            hour += 1
            if hour == 8:
                day += 1
                count, hour = 0, 0

            if day == 5:
                week += 1
                count, hour, day = 0, 0, 0

            if week == 4:
                month += 1
                count, hour, day, week = 0, 0, 0, 0

        return self._delete_zero_value(f"{month}m{week}w{day}d{hour}h")


# work_time1 = EstimationTime(20) todo del comment
# work_time2 = EstimationTime()
# a = work_time2 + work_time1

# print(a)
# print(EstimationTime().convert_to_hours2("1m5d"))
