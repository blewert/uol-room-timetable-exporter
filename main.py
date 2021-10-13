# how to use
# -----------
# edit config.json with details or run
# main.py with desired room number. make sure
# json files in json folder are up to date with raw
# json spat from timetabling api. check dump folder
# afterwards.

# timetable id -> room id 
# -----------------------
# 2 = 1102
# 3 = 1301
# 4 = 1101
# 5 = 2102
# 6 = 2305

import json
import datetime
import sys 
from dateutil import parser

config = {};

with open('config/config.json', 'r') as f:
	config = json.load(f);

room = config["default_room"];

if len(sys.argv) >= 2:
	room = sys.argv[1];

timetable_id = config["timetable_ids"][room];

current_week_date = parser.parse(config["current_week_start_date"]);
current_week = config["current_week"];
cell_colour = config["colors"]["default"];


f = open(f'json/{room}.json', 'r');
obj = json.load(f);
f.close();

data = obj["returned"]["timetableEntries"];

items = []

for entry in data:
	if entry["weeksMap"][current_week] == "1":
		items.append(entry)

rows = ["name", "start", "end", "cell_colour", "timetable_id", "created_at", "updated_at"]

sql_rows = []

lecture_color = config["colors"]["lecture"];
works_color = config["colors"]["workshop"];

for item in items:
	event = item['eventType'];

	if event == "WORKS": 
		event = "Workshop";
		# cell_colour = works_color;

	elif event == "LECTURE": 
		event = "Lecture";
		# cell_colour = lecture_color;

	elif event == "LEC/SEM":
		event = "Lecture/Seminar";

	elif event == "PRACTICAL":
		event = "Practical";

	name = f"{event}: {item['moduleTitle']}";
	day_num = item["weekDay"] - 1
	start_time = item["startTime"];
	duration_mins = item["duration"];

	start_dt = current_week_date + datetime.timedelta(days=day_num);

	split = start_time.split(":");
	hrs = int(split[0]);
	mins = int(split[1]);

	start_dt = start_dt + datetime.timedelta(hours=hrs);
	start_dt = start_dt + datetime.timedelta(minutes=mins);

	end_dt = start_dt + datetime.timedelta(minutes=duration_mins);

	created_at = datetime.datetime.now();

	print(created_at);
	print(name);
	print(start_dt);
	print(end_dt);
	print("");

	sql_rows.append({
		"name": f"'{name}'",
		"start": f"'{start_dt}'",
		"end": f"'{end_dt}'",
		"cell_colour": f"'{cell_colour}'",
		"timetable_id": str(timetable_id),
		"created_at": f"'{created_at}'",
		"updated_at": f"'{created_at}'"
	});

print("-" * 16);

f = open('dump/' + room + ".sql", 'w+');

f.write(f"DELETE FROM `mimir_bookings` WHERE `timetable_id` = {timetable_id};\n");


for row in sql_rows:
	s = "INSERT INTO `mimir_bookings` (";
	s += ",".join([ f"`{x}`" for x in row ]);
	s += ") VALUES (";

	s += ",".join([ row[x] for x in row ]);
	s += ");";

	print(s);
	f.write(s + "\n");

f.close();

print("")