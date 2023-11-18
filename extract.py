from datetime import datetime
import re
import pandas as pd

initial_data = {"date": datetime(23, 2, 2, 18, 25), "e": 5, "r": 4, "f": 2}


def extract_nums(match):
    res = {}
    for i in range(1, 4):
        token = match.group(i)
        who = token[-1]
        what = int(token[:-1])
        res[who] = what
    return res


def extract_date(line):
    date_end = line.find(" - ")
    date_str = line[:date_end]
    return datetime.strptime(date_str, "%m/%d/%y, %I:%M\u202f%p")


lines = open('data.txt', 'r').readlines()

times_list = [initial_data]

# lines look like
# 2/6/23, 5:39 PM - Francesco Dondi: 8e4r3f
points_pattern = re.compile(r'(?=.*r)(?=.*e)(?=.*f)(\d+[ref])(\d+[ref])(\d+[ref])')
for line in lines:
    msg_start = line.find(": ")
    match = points_pattern.search(line, msg_start)
    if match:
        res = extract_nums(match)
        res["date"] = extract_date(line)
        times_list.append(res)

print(pd.DataFrame.from_records(times_list).to_string())

