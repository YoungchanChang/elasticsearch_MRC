from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['https://localhost:9200'],
    basic_auth=("elastic", "Gv0QarYgz5da0Frv_cH*"),
    ca_certs="/Users/youngchan/Desktop/MRC/database/http_ca.crt",
)
