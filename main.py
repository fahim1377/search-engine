from preprocessor import Preprocessor
from processor import Processor
from embed import Embed
from search import Search

if __name__ == '__main__':
    # print("preprocessing ...")
    # preprocessor = Preprocessor()
    # preprocessor.read()
    # print("preprocessed" + "\n")
    #
    # print("processing ...")
    # processor = Processor()
    # processor.process()
    # print("processed" + "\n")
    #
    # print("embedding ...")
    # embed = Embed()
    # embed.embed()
    # print("embedded ...")

    search = Search()
    while True:
        q = input("enter your query(for quit type q : ")
        if q == 'q':
            break
        search.search(q)



