# URL 단축 서비스 구현 

---

## 프로젝트 설치방법
1. 프로젝트 repository 설치  
>git clone https://github.com/gosu4285/Backend_Assginment.git
2. 파이썬 환경 설치  
pyenv, virtualenv 가상환경에서 파이썬 3.12 버전 설치
3. 프로젝트 필요 패키지 설치  
>pip install -r requirements.txt

---

## 프로젝트 실행방법
### 서버 실행 명령어  
>uvicorn main:app --reload

### Swagger 페이지 접속  
서버 실행 후 브라우저에서 아래 주소로 접속  
>http://127.0.0.1:8000/docs

### 테스트 실행 명령어  
프로젝트 root 경로에서 pytest 입력
>pytest

---


## 프로젝트 관련 설명

### 프로젝트 요구사항 구현 리스트
1. 필수기능
- [X] 단축 URL 생성 API
- [X] 원본 URL 리디렉션 API
2. 추가 요구사항
- [X] Swagger 문서 생성 
3. 보너스 기능
- [X] URL 키 만료 기능
- [X] 통계 기능
- [X] 테스트 코드

### 프로젝트 구조
├─README.md : 프로젝트 설명 문서   
├─main.py : API 구현부   
├─requirements.txt : 필요 패키지 파일 리스트  
├─schemas.py : API 요청값 스키마  
├─sql_app   
│├─database.py : db연동설정  
│├─db_api.py : db쿼리    
│└─models.py : db스키마, orm  
├─sql_app.db : sqlite db파일  
└─test
 └─test_api.py : 테스트 코드

### db 선택 이유
sqlite를 선택했습니다.  
본 구현 프로젝트에서는 실서비스 운영이 목적이 아닌  
구현여부를 확인하기 위한 가벼운 db사용이므로   
별도 도커등으로 dbms를 세팅하지 않고  
파일만으로 처리할 수 있는 sqlite를 선택하여 구현했습니다.

만약 실 서비스를 운영하는 어떤 케이스인지에 따라  
PostgreSQL, MongoDB 선택을 하는게 좋아보입니다.  
데이터 쌓이는 요청이 많지 않게 예상되는 경우에는 일반적인 RDBMS인  
PostgreSQL을 선택하여 안정적으로 운영하는게 좋은 선택이며  
데이터가 많이 쌓이게 될 것으로 예상되는 경우에는 대용량 데이터를 처리할 때  
우수한 성능을 발휘하는 NoSQL 데이터베이스 MongoDB를 선택하는게 좋아보입니다.


### url_mapping 테이블 스키마
| column       | type     | description     |
|--------------|----------|-----------------|
| original_url | String   | 원본 url          |
| short_url    | String   | 단축 url key      |
| expired_time | DateTime | 단축 url key 만료시간 |
| count        | Integer  | url 조회 수        |

