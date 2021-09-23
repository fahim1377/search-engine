import fasttext
from elasticsearch import Elasticsearch

from settings import index_name, search_size, weights_path


class Search:

    def __init__(self):
        print("loading model ...")
        self.fasttext_model = fasttext.load_model(weights_path)
        print("model loaded")

        print("connecting to logstash ...")
        self.client = Elasticsearch(timeout=30)
        print("connected")

    def search(self,query):
        query_vector = self.fasttext_model.get_sentence_vector(query).tolist()
        print(type(query_vector))
        script_query = {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'content_vector') + 10.0",
                    "params": {"query_vector": query_vector}
                    }
            }
        }

        response = self.client.search(
            index=index_name,
            body={
                "size": search_size,
                "query": script_query,
                # "_source": {"includes": ["title", "content"]}
            }
        )

        for hit in response["hits"]["hits"]:
            print("id: {}, score: {}".format(hit["_id"], hit["_score"]))
            print(hit["_source"])
            print()

