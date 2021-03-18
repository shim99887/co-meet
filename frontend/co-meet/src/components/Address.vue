<template>
  <div class="address">
      <section class="location">
        <div class="explain">
          <h2 class="explain__title">약속장소에 적합한 장소를 추천해드립니다</h2>
          <h4 class="explain__description">현재 위치 또는<br>직접 현재 위치를 입력하실 수 있습니다.</h4>
        </div>
        <!-- 둘중에 하나의 버튼을 누르면 나머지 하나는 사라짐 -->
        <button href="#" class="location__my-location text-bold"   >내 현재 위치</button>
        <div class="search-location">
          <input type="text" disabled class="location-text" v-model="location">

    <v-dialog
      v-model="dialog"
      width="500"
    >
      <template v-slot:activator="{ on, attrs }">
        <input type="button"
          class="btn text-bold"
          v-bind="attrs"
          v-on="on"
          value="위치 입력"
        >
      </template>

      <v-card>
        <DaumPostcode :on-complete="handleAddress"/>
      </v-card>
    </v-dialog>

        </div>
        <div></div>
        <div class="terms">
          <button class="location__terms btn text-bold">개인 정보 이용 동의서</button>
          <input id="agree" type="checkbox" class="terms-checkbox">
          <label for="agree">동의</label>
        </div>
          <button href="#" class="btn terms__recom text-bold">약속 장소 추천 받기 !</button>
      </section>

      <section class="location-list">
        <div class="list__header">
          약속 장소 리스트
        </div>
        <div class="list__contents">
          <div class="contents__title">서초동</div>
          <div class="contents__description">서울시 서초구 서초3동 방배역</div>
        </div>
        <div class="list__contents">
          <div class="contents__title">명동</div>
          <div class="contents__description">서울시 중구 명동역</div>
        </div>
      </section>
  </div>
</template>
<script src="//t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js"></script>
<style>
  .explain__title, .explain__description,
  .search-location, .terms {
    padding: 2%;
    border-bottom:  2px solid #ffb6c1;
  }
  .text-bold {
    font-weight: 600;
  }
  .address {
    margin-top: 100px;
    display: flex;
    justify-content: space-between;
  }
  .location {
    padding: 10px 22px;
    width: 50%;
    border: 3px solid #ffb6c1;
    border-radius: 5px;
    
  }
  .location__terms {
    margin-right : 3%;
  }
  .location__my-location {
    display: block;
    width: 60%;
    border: 1px solid #41b6e6;
    border-radius: 5px;
    margin: 10px auto;
    padding: 10px 0;
  }
  .location__my-location:hover {
    background-color: #41b6e6;
    color: #eeeeee;
    box-shadow: 0.5px 0.5px grey;
  }
  .search-location {
    display: flex;
    justify-content: space-evenly;
  }
  .location-text {
    background-color: gainsboro;
    border-radius: 5px;
    width: 65%;
  }
  .btn {
    border: 1px solid #001871;
    border-radius: 5px;
    padding: 8px 16px;
  }
  .btn:hover {
    background-color: #001871;
    color: #eeeeee;
    box-shadow: 0.5px 0.5px grey;
  }
  .terms {
    padding: 12px
  }
  .terms__recom {
    display: block;
    margin: 3% auto 0 auto;
  }
  /* 로케이션 리스트 ! */
  .location-list{
    width: 40%;
    border: 3px solid #ec8a8a;
    border-radius: 5px;
  }

  .list__header {
    font-size: 12px;
    color: lightslategray;
    padding: 9px;
  }
  .list__contents {
    padding: 9px;
    border-bottom: 1px solid #ec8a8a;
  }
  .list__contents:hover {
    color: #eeeeee;
    background-color: #ec8a8a;
    box-shadow: 0.5px 0.5px grey;
  }
  .contents__title {
    font-weight: 600;
    font-size: 1.2em;
  }
  .contents__description {
    font-size: 0.9em;
  }
  @media screen and (max-width: 48rem) {
    .address {
      margin-top: 100px;
      display: flex;
      flex-direction: column;
    }
    .location {
      width: 100%;
      margin-bottom: 5%;
    }
    .location-list {
      width: 100%;
    }
  }
</style>

<script>
import DaumPostcode from "vuejs-daum-postcode";

export default {
  created(){
  },
    data(){
      return{
        location: '',
        dialog: false,
      }
    },
    components:{
      DaumPostcode,
    },
 methods:{
      handleAddress: function(data) {
        this.location = data.jibunAddress;
        this.dialog = false;
      },
    },

}
</script>
