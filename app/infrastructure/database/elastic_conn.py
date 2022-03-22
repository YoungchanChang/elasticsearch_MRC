from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['https://localhost:9200'],
    basic_auth=("elastic", "O*hTYJDverJ48HLGTQr7"),
    ca_certs="/Users/youngchan/Desktop/MRC/app/infrastructure/database/http_ca.crt",
)
