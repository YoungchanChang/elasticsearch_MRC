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

- 엘라스틱서치 검색시 키워드, BM25, 코사인 유사도 기준으로 검색
- 엘라스틱서치 검색 결과와 질의문을 MRC에 삽입 후 나온 결과를 정답 후보 문장으로 추출 

# Test Result

- 결과 : 의미 기반을 추가한 경우 약 7% 향상
- 테스트 데이터 : 위키피디아에서 고조선, 조선, 고구려, 고려
- 키워드 기반 검색 + 코사인 유사도를 통해 추출한 값들 중 MRC에 매칭되는 문장 추출 

# Test Result Detail

- 하단 URL 참조

https://docs.google.com/spreadsheets/d/1rEZSJL4-MJ4ADrOcsktuSw6RsLpAXmDxfizNGBKzDwg/edit#gid=0

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