import json
import csv
import base64
import re
import argparse
from shapely import Polygon


parser = argparse.ArgumentParser()
parser.add_argument('filename', help='input json file name or a list of them', nargs='*')
parser.add_argument('-p', '--path', help='input path to files', nargs=1, default=[''])
FILE_NAMES = parser.parse_args().filename
FILE_PATH = parser.parse_args().path[0]


def convert(file_name):
    file = open(file_name)
    data = json.load(file)

    with open(file_name[:-5] + '.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # fields = data['data'][0].keys()
        fields = ['name', 'polygon']
        csv_writer.writerow(fields)

        for dp in (data['data']):
            nums = re.findall(r'-?\d+', base64.b64decode(dp['polygon']).decode('utf-8'))
            coords = list(zip(*[iter(nums)] * 2))

            for j in range(len(coords)):
                coord1 = int(coords[j][0]) / 5000
                coord2 = int(coords[j][1]) / 5000

                coords[j] = (coord1, coord2)

            row = []
            for field_name in fields:
                if field_name == 'polygon':
                    row.append(Polygon(coords))
                else:
                    row.append(dp[field_name])
            csv_writer.writerow(row)

    file.close()


if __name__ == '__main__':
    for f in FILE_NAMES:
        convert(FILE_PATH + f + '.json')
