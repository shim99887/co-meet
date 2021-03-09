## Data Modeling

### Reference data

- 포스트 코로나 데이터 시각화 경진대회
[포스트 코로나 데이터 시각화 경진대회](https://dacon.io/competitions/official/235618/data/)

- 서울 자치구별 코로나 확진자 현황
[서울 자치구별 확진자 현황](https://www.seoul.go.kr/coronaV/coronaStatus.do)

- 서울시 유동인구 데이터 : 2019.03 ~ 2021.01
[서울시 유동인구 데이터](https://www.bigdatahub.co.kr/product/list.do?menu_id=1000157)


### Table 

1. SKT 유동인구 데이터

- 일자 : ex) 20210115
- 시간 : ex) 01 ~ 23
- 나이대 : ex) 70 → 70대
- 성별 : ex) 남성,여성
- 지역 : ex) 서울 default
- 구 이름 : ex) 성북구, 동대문구
- 유동인구수 : ex) 38000명

2. adstrd_master.csv : 8자리 행정동 코드 데이터

- adstrd_code(행정동 코드) : ex) 110111
- adstrd_nm(행정동명) :  ex) 영등포구
- brtc_nm(시도명) : ex) 서울특별시
- signgu_nm(시군구명) : ex) 관악구,구로구

3. card.csv : 업종 별 결제금액 데이터(카드내역)

- receipt_dttm : 카드사용내역을 접수한 일자
- adstrd_code : 가맹점 위치 기준 행정동 코드
- adstrd_nm : 가맹점 위치 기준 행정동명
- mrhst_induty_cl_code : 가맹점 업종코드
- mrhst_induty_cl_nm : 가맹점 업종명
- selng_cascnt : 매출발생건수
- salamt : (하루기준)매출발생금액

4. index.csv : 품목 별 소비지수 데이터

- period : 기준월
- catl : 대분류
- catm : 중분류
- age : 나이대
- gender : 성별
- sido : 지역
- sigungu : 세부지역
- cgi : 카테고리성장지수 (2018년 월평균 대비 매출 성장 비율, 100을 기준으로 이상이면 매출 상승, 이하면 하락)

5. corona :서울 자치구별 코로나 확진자 현황(개인정보의 이유로 확진자 동선은 2주뒤에 삭제됩니다.)

- brtc-nm : 시도명
- signgu_nm : 시군구명
- date : 걸린 날짜
- status : 퇴원 여부

* 파싱 주기 : 12시에 업데이트되므로 매일 12시 마다 일괄 업데이트 

6. score : 점수 부여 기준

- 시군구명
- 점수

* 점수 가중치 요소

- 퇴원여부 : 사망, 퇴원, 빈칸(퇴원X, 치료중)
- 확진자수
    - 상대값 가중치 : 하루 전 혹은 일주일 전을 기준으로 현재 확진자 수의 추이 변화를 기준으로가중치를 둔다.
                      ( 구마다 걸린 확진자 수의 평균을 잡아서 평균보다 많으면 위험지역, 적으면 안전지역 )
    - 절대값 가중치 : 5명 단위로 끊어서 현재 확진자 수를 기준으로 가중치를 둔다. (구 별 확진자 기준)

- 유동인구 : 유동인구 대비 확진자 수를 고려하여 비율이 상대적으로 작으면,
             (예측 유동인구를 두어 예상추이를 생각해본다.)
- 카드사용량 - 매출발생건수를 기준으로 유동인구 대비 비율의 높고 낮음을 판별하여 가중치를 둔다.

7. user : 회원 

- _id : ex) 1234
- email : ex) "test@test.com"
- password : ex) "password"
- nickname : ex) comeet
- address : ex) "서울특별시 강남구"
- emailToken(이메일 인증을 위한 토큰) : ex) "19ADVC3DS"
- flag(인증을 받은 사용자인지 아닌지 판단) : ex) true
- quitFlag(탈퇴여부) : ex) false
- shortcuts(회원 검색 로그) : ex) [
                    				{"_id" : "Object_id("602d0fc3628e395b21169645")","nickname" : "낙훈", "address" : "경기도 고양시 일산동구"},
                    				{"_id" : "Object_id("602d0fc3628e395b21167645")","nickname" : "세준", "address" : "서울특별시 관악구"},
                    				{"_id" : "Object_id("602d0fc3628e395b21163645")","nickname" : "덕인", "address" : "서울특별시 영등포구"}
                    		      ]