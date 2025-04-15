#!/usr/bin/python3
# HTML metapicture generator

import csv

# Files:
inputfile, outputfile = "filter/filtered_ids_and_dates.csv", "index.html"

# Data points:
dates, ids, keyframes = [], [], []

# Lines of HTML:
top, middle, bottom = [], [], []
page = [top, middle, bottom]

top.append("""<!DOCTYPE html>""")
top.append("""<html><head><title>Metapicture of keyframes</title></head><body>""")
top.append("""<table><caption>Metapicture of keyframes</caption>""")
top.append("""<thead><tr><th scope="col">Date</th><th scope="col">ID</th><th scope="col">Keyframe</th><tr></thead><tbody>""")

bottom.append("""</tbody></table>""")
bottom.append("""</body></html>""")

with open(inputfile, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # print(f"Processing {row}")
        dates.append(row[0])
        ids.append(row[1])

for i in ids:
    keyframes.append(f"only_keyframes/{i}-keyframes.jpg")

for d, i, k in zip(dates, ids, keyframes):
    middle.append(f"""<tr><td>{d}</td><td>{i}</td><td><img src="{k}"></td></tr>""")

with open(outputfile, "w") as file:
    for part in page:
        for line in part:
            file.write(f"{line}\n")

print("READY!")
