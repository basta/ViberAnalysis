class Message(object):
    def __init__(self, date, time, sender, text):
        self.date = date
        self.sender = sender
        self.text = text
        if "PM" in time:
            self.time = str(int(time[:2]) + 12) + time[2:8]
        else:
            self.time = time
test = Message("05/02/2018", "01:52:47 PM", "Viki", "118? Tady je to lepší...")

class MessageList(object):
    def __init__(self):
        messages = []
        amounts = {}
    def scrape(self, csvfile):
        pass


def FileLength(fname):
    f = open(fname, "r", encoding="utf8")
    empties = 0
    length = 0
    while True:
        length += 1
        try:    line = f.readline()
        except UnicodeDecodeError:  line = ""
        if line == "":
            empties += 1
            if empties >= 20:
                return length - 20
        else:
            empties = 0

print(FileLength("Viki.csv"))
