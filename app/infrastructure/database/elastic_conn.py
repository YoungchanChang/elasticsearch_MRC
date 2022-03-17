from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['https://localhost:9200'],
    basic_auth=("elastic", "6bXz4stf_*78WWZgiDPH"),
    ca_certs="/Users/youngchan/Desktop/MRC/app/infrastructure/database/http_ca.crt",
)
