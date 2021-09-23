import json

import fasttext

from preprocessor import Preprocessor
from settings import original_data_path, number_of_records, preprocessed_data_path, weights_path, embedded_data_path


class Embed:

    def __init__(self):
        self.origin_path = original_data_path
        self.preprocessed_path = preprocessed_data_path
        self.number_of_lines = number_of_records
        self.weights_path = weights_path
        self.embedded_path = embedded_data_path

    def read_row(self, f):
        usage = "this function read each row from original data in form of multiline json"
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
        row_json = json.loads(row)
        return row_json

    def embed(self):
        usage = "this method embed data from original data with pretrained weights of fasttext model and save it in another file"

        print("loading model ...")
        fasttext_model = fasttext.load_model(self.weights_path)
        print("model loaded")

        # read from original data
        with open(self.origin_path, 'r') as odf:
            with open(self.preprocessed_path, 'r') as ppd:
                with open(self.embedded_path, 'w') as ed:
                    for line_row in range(self.number_of_lines):
                        origin_line = self.read_row(odf)
                        preprocessed_content = ppd.readline()
                        preprocessed_content = preprocessed_content.replace("\n", " ")
                        content_vector = fasttext_model.get_sentence_vector(preprocessed_content)
                        if preprocessed_content != ' ':
                            origin_line['content_vector'] = content_vector.tolist()
                            origin_line['normed_content'] = preprocessed_content
                            row = json.dumps(origin_line) + '\n'
                            ed.write(row)


