#!/usr/bin/env python
# coding: utf-8

# imports###############
import json
import sys
###############################


class NewsDataReader:
    def __init__(self, fromtxt, tocsv, number_of_lines=None, row_lines=None):

        self.number_of_lines = 1000000  # number of rows to read
        self.row_lines = 16  # number of lines containing one row
        self.fromtxt = fromtxt
        self.tocsv = tocsv

    # read a multiple lines in txt file and convert it to a dictionary in python
    def read_row(self, f):
        row = ''
        opens = 0

        while True:
            readed = f.readline()
            if ('{\n' in readed) or ('": {\n' in readed):
                opens += 1
            if ('},\n' in readed) or ('}\n' in readed):
                opens -= 1

            row = row + readed

            if opens == 0:
                break
        try:
            row_json = json.loads(row)
        except Exception as e:
            print(row)
            raise e
        return row_json

    def read(self):
        # load txt file row by row and extract each row from json format, then converts to csv format
        with open(self.fromtxt, 'r') as f:
            with open(self.tocsv, 'w') as csvf:
                # create the csv writer
                row = self.read_row(f)

                for line_row in range(self.number_of_lines):
                    try:
                        row = self.read_row(f)
                        # write a row to the csv file
                        row = json.dumps(row) + '\n'
                        csvf.write(row)
                        if line_row % 1000 == 0:
                            print(line_row)

                    except Exception as e:
                        print(e)
                        break


if __name__ == '__main__':

    fromtxt = '../resources/ferdowsi-data/Spad/ferdowsi-data.txt'
    tocsv = '../resources/ferdowsi-data/Spad/out.log'
    if len(sys.argv) > 1:
        fromtxt = sys.argv[1]
        tocsv = sys.argv[2]

    reader = NewsDataReader(fromtxt=fromtxt, tocsv=tocsv)
    print("started")
    reader.read()
    print("successfully was read")
