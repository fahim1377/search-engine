from settings import number_of_records, original_data_path, preprocessed_data_path
import json
import hazm
import nltk
from nltk.corpus import stopwords



class Preprocessor:

    def __init__(self):
        self.fromtxt = original_data_path
        self.tocsv = preprocessed_data_path
        self.number_of_lines = number_of_records
        self.normalizer = hazm.Normalizer()
        try:
            self.stopwords = stopwords.words('english') + stopwords.words('persian')
        except LookupError:
            nltk.download('stopwords')
            self.stopwords = stopwords.words('english') + stopwords.words('persian')
        self.tokenizer = hazm.WordTokenizer()


    def read_row(self,file):
        usage = "this function read each row from original data in form of multiline json"
        row = ''
        opens = 0

        while True:
            readed = file.readline()
            if ('{\n' in readed) or ('": {\n' in readed):
                opens += 1
            if ('},\n' in readed) or ('}\n' in readed):
                opens -= 1

            row = row + readed

            if opens == 0:
                break
        row_json = json.loads(row)
        return row_json

    def preprocess(self, content):
        normed_content = self.normalizer.normalize(content)
        tokens = self.tokenizer.tokenize(normed_content)
        non_stop_text = ''
        for token in tokens:
            if token not in self.stopwords:
                non_stop_text += token + ' '
        return non_stop_text

    def read(self):
        usage = "this method read the data and preprocess it and store it in another file containing one preprocessed content in each line"

        with open(self.fromtxt, 'r') as of:
            with open(self.tocsv, 'w') as csvf:
                # create the csv writer
                for line_row in range(self.number_of_lines):
                    row = self.read_row(of)
                    # write a row to the csv file
                    content = row['_source']['content']
                    preprocessed_content = self.preprocess(content)
                    csvf.write(preprocessed_content)
                    csvf.write('\n')
                    if line_row % 1000 == 0:
                        print(line_row)


