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
daily_messages = []
for i in days:
    daily_messages.append(len(i))

averaged_daily_messages = []
for i in range(len(daily_messages)):
    divider = 1
    amount = 0
    amount += daily_messages[i]
    for offset in range(0, 10):
        if not i + offset > len(daily_messages) - 1:
            divider += 1
            amount += daily_messages[i + offset]
        if not i - offset < 0:
            divider += 1
            amount += daily_messages[i - offset]
    averaged_daily_messages.append(amount / divider)

plt.plot(daily_messages)
plt.plot(averaged_daily_messages)
plt.show()
