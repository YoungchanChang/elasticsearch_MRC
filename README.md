# elasticsearch_MRC

- 엘라스틱서치 knn알고리즘을 사용하여 MRC 답변 향상

- 엘라스틱서치 8.0 이상
- database/http_ca.crt 변경 필수
- 

# 실행 순서

1. 필수 라이브러리 설치

```
pip install -r requirements.txt
```

2. 인덱스 추가
elastic_index.py


3. main.py 실행

## example

- `위키피디아에서 데이터 검색 후 답변 insert기간이 길 수 있음`

- request

![](../Screen Shot 2022-03-17 at 2.55.46 PM.png)

- return

![](../Screen Shot 2022-03-17 at 2.55.52 PM.png)