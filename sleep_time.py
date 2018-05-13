import matplotlib.pyplot as plt


class Message(object):
    def __init__(self, date, time, sender, text):
        self.date = date
        self.sender = sender
        self.text = text
        if "PM" in time:
            self.time = str(int(time[:2]) + 12) + time[2:8]
        else:
            self.time = time


class MessageList(object):
    def __init__(self, messages = [], amounts = {}):
        self.messages = messages
        self.amounts = amounts

    def scrape(self, csvfile, invalids=[",", ".", "*", "(", ")", "?", "[", "]", "'", "\""]):
        f = open(csvfile, "r", encoding="utf8")
        empties = 0
        while True:
            line = f.readline()
            if line == "":
                empties += 1
                if empties >= 20:
                    break
            else:
                empties = 0
                line = line.replace(",", "‼", 4)
                for i in invalids:   line = line.replace(i, "")
                line = line.lower()
                line = line[:-1]
                line = line.split("‼")
                if len(line) == 5:
                    self.messages.append(Message(line[0], line[1], line[2], line[4]))

    def word_amounts(self):
        for i in self.messages:
            words = i.text.split(" ")
            for i in words:
                if i in self.amounts.keys():
                    self.amounts[i] += 1
                else:
                    self.amounts[i] = 1


def reverse_dict(dic):
    ret = {}
    for i in dic.keys():
        if not dic[i] in ret.keys():
            ret[dic[i]] = [i]
        else:
            ret[dic[i]].append(i)
    return ret


filename = "Viki.csv"

main = MessageList()
main.scrape(filename)
date = main.messages[0].date
days = []
day_message = []
for i in main.messages:
    if i.date == date:
        day_message.append(i)
    else:
        days.append(day_message)
        date = i.date
        day_message = []

last_messages = []
for i in days:
    try:
        last_messages.append(i[-1])
    except IndexError:
        last_messages.append("ignore")
while True:
    try:
        last_messages.remove("ignore")
    except ValueError:
        break

last_messages_times = []
last_messages_times_seconds = []
for i in last_messages: last_messages_times.append(i.time)
for i in last_messages_times:
    seconds = 0
    seconds += int(i[0] + i[1])*3600
    seconds += int(i[3] + i[4])*60
    seconds += int(i[6] + i[7])
    if "pm" in i:
        seconds += 12*3600
    last_messages_times_seconds.append(seconds)
past_midnight = []
past_midnight_height = []
for i in range(len(last_messages_times_seconds)):
    if int(last_messages_times_seconds[i]) > 84000:
        past_midnight.append(i)
for i in past_midnight: past_midnight_height.append(86400)
averaged_last_messages_times_seconds = []
for i in range(len(last_messages_times_seconds)):
    divider = 1
    amount = 0
    amount += last_messages_times_seconds[i]
    for offset in range(0, 10):
        if not i + offset > len(last_messages_times_seconds) - 1:
            divider += 1
            amount += last_messages_times_seconds[i + offset]
        if not i - offset < 0:
            divider += 1
            amount += last_messages_times_seconds[i - offset]
    averaged_last_messages_times_seconds.append(amount / divider)

print(len(past_midnight) / len(last_messages_times_seconds))
plt.plot(last_messages_times_seconds)
plt.plot(averaged_last_messages_times_seconds)
plt.scatter([past_midnight], [past_midnight_height])
plt.show()
