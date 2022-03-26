# elasticsearch_MRC

엘라스틱서치에서 문장 단위 검색
- 엘라스틱서치 키워드 기반 검색
- 엘라스틱서치 BM25 기반 검색
- 엘라스틱서치 코사인 유사도 기반 검색
- MRC 활용하여 엘라스틱 서치 검색 결과 필터링

# Required
- 엘라스틱서치 7.9.1 이상 설치
- app/infrastructure/database/http_ca.crt 변경 필수(ref : https://chatbottalk.tistory.com/244)

# Details

- 엘라스틱서치 검색 시 키워드 점수에 문장 유사도 점수 합산
- 나온 문장들 중 MRC를 이용하여 질의 문에 대해 답이 있는 곳 추출
- 추출한 단어가 있는 문장 재추출

# Installation

1. 필수 라이브러리 설치

```
pip install -r requirements.txt
```

2. 인덱스 추가

```
python scripts/elastic_vector_index.py
```

3. fastapi 실행

```
python main.py
```


# example

- 사용하지 않았을 경우에 비해 약 7% 향상

- 테스트 시나리오 : 위키피디아에서 고조선, 조선, 고구려, 고려의 내용을 넣은 뒤 키워득 기반 검색과 키워드 및 의미 기반 검색 결과 비교 

```
https://docs.google.com/spreadsheets/d/1rEZSJL4-MJ4ADrOcsktuSw6RsLpAXmDxfizNGBKzDwg/edit#gid=0`
```


<img width="1456" alt="Screen Shot 2022-03-17 at 2 55 46 PM" src="https://user-images.githubusercontent.com/40015958/158746631-a07b9655-0de6-4127-bb3f-6669087abe2d.png">


- return

<img width="1534" alt="Screen Shot 2022-03-17 at 2 55 52 PM" src="https://user-images.githubusercontent.com/40015958/158746646-e8aef997-99a7-4c5a-aec3-07e7fcbd28dc.png">

# License

The code is made available under the GNU Affero General Public License v3.0.

#Reference
If you find this code useful, please refer it in publications as:

@misc{elasticsearch_MRC,
  author = {Youngchan Chang},
  title = {elasticsearch_MRC},
  year = {2022},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/YoungchanChang/elasticsearch_MRC}}
}