## Project setup
```
yarn install
```

### Compiles and hot-reloads for development
```
yarn serve
```

### Compiles and minifies for production
```
yarn build
```

### Lints and fixes files
```
yarn lint
```

```bash
// installation

yarn global add @vue/cli
yarn global upgrade --latest @vue/cli
vue create co-meet
vue add router
yarn add vuex
yarn add vuetify
```

## 🤝 CO-MEET

> **Co-** (함께) + **Meet** (약속) = **CO-MEET**


## 프로젝트 개요

- **진행기간** : 2021.03.02 ~ (ing)
- **만든이** : 강세준, 김영록, 장덕인, 최낙훈, 한승엽
- **기획 배경**
   - **위드 코로나 시대**에 더 이상 집콕만 할 수 없는 우리들
   - 어떻게 하면 사람이 **밀집된** 지역이나 **위험 지역**을 피해서 친구들을 만날 수 있을까?
   - 유동인구, 카드 사용량을 바탕으로 비교적 사람이 적은 장소를 물색한다.
   - 지역별(동기준) 코로나 상승률을 분석하여 현재 위치를 기반으로 가장 안전한 장소를 찾아보자 !
   - **코로나 시대에 안전하게 만날 수 있는 약속 장소 추천 서비스!**
- **목표**
   - 코로나 확진자 발병 지역과 지역 별 확진자 변화 분석
   - 코로나 확진자 발병 지역을 참고하여 비교적 안전한 약속 장소를 추천
   - 현재 위치 정보 기준으로 일정 km 이내의 안전한 약속 장소를 찾아 추천.
   - 여러 명의 위치 기준으로 중간 지점을 추천하는 기능 추가 도입

## 📄 **활용 데이터 및 API**

> 유동 인구 데이터
   
[데이터 기본 설명](https://www.bigdatahub.co.kr/product/view.do?pid=1002348)
      
>  코로나 지역관리본부 크롤링
   
[코로나 실시간 서울시 구별 확진자 동향 데이터](https://www.seoul.go.kr/coronaV/coronaStatus.do)
      
> 카드 사용 데이터
   
[카드 사용 데이터](https://dacon.io/competitions/official/235618/data/)
      
> 현 사용자 위치 정보 (크롬 기반)
   
[Geolocation API](https://www.zerocho.com/category/HTML&DOM/post/59155228a22a5d001827ea5d)

   - 유동인구 & 카드 사용량 분석 ⇒ 사람 ⬇ 밀집도 ⬇
   
     지역별 코로나 상승률 분석 ⇒ 코로나 발생률 ⬇ 안정성 ⬆

     현재 위치 & 검색 위치 기반 ⇒ 편의성 ⬆

- Front-end 제작 환경 👨‍💻

  - Vue.cli
  - Sass(Scss)
  - vuetify

- 사용 툴 🔧

  - Visual Studio Code  -> 코드 에디터
  - Figma.com  -> 와이어 프레임
  - Notion  -> 문서화

- 2021-03-07 까지의 개발 현황

- Landing Page
![image](/uploads/2c4cca8f82c0aa85c3642681a869bc3e/image.png)
- 추천 페이지
![image](/uploads/913fd8f040cefff5869b98b3703815c4/image.png)

- 페이지 구축 🧩
  - Vue.cli의 SPA 특성상 총 크게 두개의 view가 존재한다

    > 웹의 느낌을 줄이고, 실제 소프트웨어의 느낌을 살리기 위해 에니메이션 효과를 사용함

    - 랜딩 페이지

      - 서비스의 첫 이미지를 담당하기 때문에 시각적인 효과에 집중함.
      - 봄의 만연한 꽃과 코로나 종식을 기원하는 마음을 담은 배경 화사한 느낌의 배경 선택
      - 프로젝트의 주된 색상 또한 이 배경에서 차용함.

      

    - 메인 기능을 하는 장소 추천 페이지

      - 실제 장소 추천 기능을 하는 페이지
      - 최대한 직관적인 느낌과 글을 사용하지 않아도 사용할 수 있게 스타일링하려고 노력함

## Document
<details>
    <summary> Convention </summary>
    <ul>
        <a href="Document/Convention/Python_Convention.md"><li> Python_Convention</li></a>
    </ul>
</details>
<details>
    <summary> Commit Rule</summary>
    <ul>
        <a href="Document/Commit Rule/Git Commit Rule.md"><li> Git Commit Rule</li></a>
    </ul>
</details>
<details>
    <summary> Data Modeling</summary>
    <ul>
        <a href="Document/Data Modeling/Data Modeling.md"><li> Data Modeling</li></a>
    </ul>
</details>
<details>
    <summary> Wireframe</summary>
    <ul>
        <a href="Document/Wireframe/Wireframe.md"><li> Wireframe</li></a>
    </ul>
</details>
<details>
    <summary> Implementation Part</summary>
    <ul>
        <a href="Document/Implementation part/Implmt.md"><li> Implementation Part</li></a>
    </ul>
</details>