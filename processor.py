import fasttext
from settings import preprocessed_data_path, weights_path


class Processor:

    def process(self):
        usage = "this method read data and process it with fasttext model and save the weights"

        # Build word embedding model and create one more with dim=3 for experimentation
        model = fasttext.train_unsupervised(preprocessed_data_path, model='skipgram', dim=300)
        print("saving model weights")
        model.save_model(weights_path)
        print("model weights saved")
