# elasticsearch_chat

엘라스틱서치와 MRC를 활용한 문장 단위 검색
- 엘라스틱서치 키워드 기반 검색
- 엘라스틱서치 BM25 기반 검색
- 엘라스틱서치 코사인 유사도 기반 검색
- MRC 활용하여 엘라스틱 서치 검색 결과 필터링

# Required
- 엘라스틱서치 7.3.0 이상 설치

# Details

- 엘라스틱서치 검색시 키워드, BM25, 코사인 유사도 기준으로 검색
- 엘라스틱서치 검색 결과와 질의문을 MRC에 삽입 후 나온 결과를 정답 후보 문장으로 추출 

# UseCase

<figure>
<img src=https://i.imgur.com/3euBjA6.png" alt="views">
<figcaption>유스케이스 다이어그램</figcaption>
</figure>

# API문서

- 엘라스틱서치 문장 검색 API

RequestAPI: /mrc/search_sentence


| 파라미터     | 타입     | 필수여부 | 설명        |
|----------|--------|------|-----------|
| question | string | Y    | 사용자 발화 문장 |


ResponseAPI:

- 검색 문서 정보

| 파라미터                    | 타입      | 필수여부 | 설명              |
|-------------------------|---------|------|-----------------|
| best_proper_sentence    | Objects | Y    | 가장 적합한 문서 정보    |
| best_proper_sentence 속성 | -       | -    | -               |
| score                   | float   | Y    | 엘라스틱서치 검색 총합 점수 |
| title                   | string  | Y    | 제목              |
| first_header            | string  | Y    | 부제목             |
| second_header           | string  | Y    | 소제목             |
| content                 | string  | Y    | 검색 문서           |
| content_noun_tokens     | List    | Y    | 문서 명사 검색 키워드    |
| content_verb_tokens     | List    | Y    | 문서 동사 검색 키워드    |
| content_match_tokens    | List    | Y    | 텍스트 검색 키워드      |

# Test Result

- 결과 : 의미 기반을 추가한 경우 약 7% 향상
  - 테스트 데이터 : 위키피디아에서 고조선, 조선, 고구려, 고려

# Test Result Detail

- 상세 테스트 결과 : 하단 URL 참조

https://docs.google.com/spreadsheets/d/1rEZSJL4-MJ4ADrOcsktuSw6RsLpAXmDxfizNGBKzDwg/edit#gid=1395843693

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
  email = {san0558@naver.com},
  howpublished = {https://github.com/YoungchanChang/elasticsearch_MRC}
}
