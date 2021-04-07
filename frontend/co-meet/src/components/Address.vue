<template>
  <div class="recom-body">
    <div class="banner">
      <h3>장소 추천 페이지</h3>
      <br />
      <p>
        서울시의 장소들을 입력하시면, 안전한 장소를 추천해드립니다. <br />
        장소의 대한 자료는 하단에 안내해드립니다.
      </p>
    </div>
  <div class="address">
    <section class="location">
      <MglMap
        id="map"
        :accessToken="accessToken"
        :mapStyle.sync="mapStyle"
        v-if="mapToggle"
        @load="onMapLoaded"
      >
        <!-- 마커를 반복문을 돌면서 coordinate의 좌표를 넣는다. -->
        
        <div class="" v-for="(item, idx) in citiesCoordinates" :key="idx">
          <mglMarker :coordinates="citiesCoordinates[idx]" color="#ffb6c1">
            <MglPopup>
              <Vcard class="pa-0">
                만날 장소 추천지: {{ cities[idx] }}
              </Vcard>
            </MglPopup>
          </mglMarker>
        </div>

      </MglMap>
      <div class="location__wrapper" v-show="!mapToggle">
        <div class="explain">
          <h2 class="explain__title">
            약속장소에 적합한 장소를 추천해드립니다
          </h2>
        </div>
        <!-- 둘중에 하나의 버튼을 누르면 나머지 하나는 사라짐 -->
        <section class="location__selection">

        <div class="text-center or-text">
          <img src="../assets/map.gif" alt="map gif" class="map-gif">
        </div>
          <div class="chips" v-if="addrList.length > 0">
            <v-chip
              color="#ffb6c1"
              style="margin: 8px 10px;"
              close
              close-icon="mdi-close-outline"
              v-for="(addr, index) in addrList"
              :key="index"
              @click:close="temp(index)"
              >{{ addr }}
            </v-chip>
          </div>
        <div class="search-location">
          <v-dialog v-model="dialog" width="500">
            <template v-slot:activator="{ on, attrs }">
              <input
                type="button"
                class="btn text-bold mt-2"
                v-bind="attrs"
                v-on="on"
                value="위치 입력"
                @click="findInputLocation"
              />
            </template>
            <v-card>
              <DaumPostcode :on-complete="handleAddress" />
            </v-card>
          </v-dialog>
        </div>
        </section>
                <div class="terms">
          <v-dialog
            v-model="dialogTerms"
            fullscreen
            hide-overlay
            transition="dialog-bottom-transition"
          >
            <template v-slot:activator="{ on, attrs }">
              <a
                v-bind="attrs"
                v-on="on"
                class="location__terms"
              >
                개인 정보 이용 동의서</a>
            </template>
            <v-card>
              <v-toolbar dark color="#ffb6c1">
                <v-btn icon dark @click="dialogTerms = false">
                  <v-icon>mdi-close</v-icon>
                </v-btn>
                <v-toolbar-title>개인 정보 수집 이용 동의서</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>

              <v-container class="terms__body">
                <b>Ⅰ. 개인정보의 수집 및 이용 동의서 </b> <br />
                - 이용자가 제공한 모든 정보는 다음의 목적을 위해 활용하며, 하기
                목적 이외의 용도로는 사용되지 않습니다.<br />
                ① 개인정보 수집 항목 및 수집·이용 목적<br />
                가) 수집 항목 (필수항목)<br />
                - 주소, 전화번호(자택, 휴대전화), 이메일, 신청서에 기재된 정보
                또는 신청자가 제공한 정보<br />
                나) 수집 및 이용 목적<br />
                - 현재 위치 파악과 안전 지역 추천 진행<br />
                - 이용자의 위치 및 자격확인<br />
                - 회원 정보 자원관리<br />
                ② 개인정보 보유 및 이용기간<br />
                - 수집·이용 동의일로부터 개인정보의 수집·이용목적을 달성할
                때까지<br />
                ③ 동의거부관리<br />
                - 귀하께서는 본 안내에 따른 개인정보 수집, 이용에 대하여 동의를
                거부하실 권리가 있습니다. 다만,<br />
                귀하가 개인정보의 수집/이용에 동의를 거부하시는 경우에 서비스
                서비스 이용 과정에 있어 불이익이 발생할 수<br />
                있음을 알려드립니다<br />
                <br />
                <b>Ⅱ. 고유식별정보 처리 동의서</b><br />
                ① 고유식별정보 수집 항목 및 수집·이용 목적<br />
                가) 수집 항목 (필수항목)<br />
                - 이메일<br />
                나) 수집 및 이용 목적<br />
                - 현재 위치 파악과 안전 지역 추천 진행<br />
                - 이용자의 위치 및 자격확인<br />
                - 회원 정보 자원관리<br />
                ② 개인정보 보유 및 이용기간<br />
                - 수집·이용 동의일로부터 개인정보의 수집·이용목적을 달성할
                때까지<br />
                ③ 동의거부관리<br />
                - 귀하께서는 본 안내에 따른 개인정보 수집, 이용에 대하여 동의를
                거부하실 권리가 있습니다. 다만,<br />
                귀하가 개인정보의 수집/이용에 동의를 거부하시는 경우에 서비스 이용
                과정에 있어, 불편함이 발생할 수<br />
                있음을 알려드립니다.<br />
              </v-container>
            </v-card>
          </v-dialog>

            <input
              id="agree"
              type="checkbox"
              value="agreed"
              class="terms-checkbox"
              v-model="agreed"
            />
            <label for="agree" class="checkbox-label">동의</label>
          </div>
          <button href="#" class="btn terms__recom text-bold" @click="getRecom">
            약속 장소 추천 받기 !
          </button>
        </div>
      </section>

      <section class="location-list" v-if="cities.length">
        <div class="list__header">
          약속 장소 리스트
        </div>
        <div v-if="cities.length">
          <div class="list__contents" v-for="(item, idx) in cities" :key="idx">
            <div class="contents__title">{{ item }}</div>
            <div class="contents__description">서울시 {{ item }}</div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script src="//t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js"></script>
<script src="https://api.mapbox.com/mapbox-gl-js/v2.1.1/mapbox-gl.js"></script>
<script>
import DaumPostcode from "vuejs-daum-postcode";
import Mapbox from "mapbox-gl";
import { MglMap, MglMarker, MglPopup, Vcard } from "vue-mapbox";
import axios from "axios";
import VueGeolocationApi from "vue-geolocation-api";

const SERVER_URL = process.env.VUE_APP_SERVER_URL;

export default {
  components: {
    DaumPostcode,
    MglMap,
    MglMarker,
    MglPopup,
  },
  data() {
    return {
      accessToken:
        "pk.eyJ1IjoiaHN5MTE4IiwiYSI6ImNrbWxibWNueDByeGkycGxzMXZmZHJ5eGUifQ.MN9N94gheL1y_QPLj1vm7w",
      mapStyle: "mapbox://styles/hsy118/ckmlk2yhknikz17qsc283g4yj",
      coordinates: [],
      // mapToggle: false,
      agreed: false,
      dialogTerms: false,
      location: [],
      dialog: false,
      selectMethod: "",
      //여기에 주소가 저장되서 이걸로 getRecom함수에 넣어야함. (03-31일 현재, location에 보낼 '구' 하나만 저장되어서 요청 보냄)
      addrList: [],
      //1등 후보 찍는 곳
      latitude: "",
      longitude: "",
      textContent: "",
      //temp
      sending: {},
      reset: false,
    };
  },

  methods: {
    temp(index) {
      console.log(index);
      // this.addrList.pop(index);
      this.$delete(this.addrList, index);
    },
      async getRecom () {
          if (this.agreed === true && this.addrList.length > 0) {
            this.$store.commit("ON_SEARCHING")
            // 주소를 카카오 api로 보내서 좌표로 만들기
              await this.addrList.forEach(item => {
                this.putLatLng(item)
              });
            // 장소 리스트
            setTimeout(() => {
              // 추천 장소 받기
              this.$store.dispatch("GET_RECOM")
              // 지난 달 구별 코로나
              this.$store.dispatch("GET_CORONA_PER_CITY")
            }, 500)

                  var log = {};
        log.email = this.$store.getters.getUserEmail;
        const geocoder = new kakao.maps.services.Geocoder();
        var data = [];
        this.addrList.forEach((element) => {
          geocoder.addressSearch(element, function(result, status) {
            if (status === kakao.maps.services.Status.OK) {
              const coord = new kakao.maps.LatLng(result[0].y, result[0].x);
              var inputData = {
                juso: element,
                lat: coord.Ma,
                lng: coord.La,
              };
              console.log("inputData: ", inputData);
              data.push(inputData);
            }
          });
        });
        log.searchList = data;
        console.log("data : ",data);

        setTimeout(() => {
          axios
            .post(`${SERVER_URL}/user/searchlog`,   {
              email:this.$store.getters.getUserEmail,
              searchList:data,
            })
            .then((response) => {
              console.log(response);
            })
            .catch((error) => {
              alert(error);
            });

        }, 500)

          } else {
            alert("정보 이용에 동의, 혹은 주소를 입력해주세요")
          }
       },
    async onMapLoaded(event) {
      // 도시 받은거 입력
      const data = this.citiesCoordinates;
      const asyncActions = event.component.actions;
      // 1순위 보여주는 비동기 함수
      const newParams = await asyncActions.flyTo({
        center: data[0],
        zoom: 12.5,
        speed: 1,
      });
    },
    async putLatLng(data) {
      var self = this;
      const geocoder = new kakao.maps.services.Geocoder();
      await geocoder.addressSearch(data, function(result, status) {
        if (status === kakao.maps.services.Status.OK) {
          const coord = new kakao.maps.LatLng(result[0].y, result[0].x);
          const juso = data.split(" ")[1];
          var inputData = {
            juso: juso,
            lat: coord.Ma,
            lng: coord.La,
          };
          self.$store.commit("PUT_TARGETCITIES", inputData);
        }
      });
    },
    handleAddress: function(data) {
      if(data.jibunAddress === "") {
        this.addrList.push(data.autoJibunAddress);
      } else {
        this.addrList.push(data.jibunAddress);
      }
      this.dialog = false;
    },
    findCurrentLocation() {
      console.log("click cur location");
      this.selectMethod = "currentLocation";
      if (!("geolocation" in navigator)) {
        this.textContent = "Geolocation is not available";
        return;
      }
      this.textContent = "Locating...";
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          this.latitude = pos.coords.latitude;
          this.longitude = pos.coords.longitude;
          this.textContent =
            "Your location data is " + this.latitude + ", " + this.longitude;
        },
        (err) => {
          this.textContent = err.message;
        }
      );
    },
    findInputLocation() {
      console.log("click input location");
      this.selectMethod = "inputLocation";
    },
  },
  computed: {
    mapToggle() {
      return this.$store.getters.get_mapToggle;
    },
    cities() {
      return this.$store.getters.get_result;
    },
    citiesDate() {
      return this.$store.getters.get_month;
    },
    citiesPatients() {
      return this.$store.getters.get_patients;
    },
    citiesCoordinates() {
      return this.$store.getters.get_coordinates;
    },
    targets() {
      return this.$store.getters.get_targets;
    },
    gugun() {
      return this.$store.getters.get_gugun;
    },
  },
  watch: {
    selectMethod: function() {
      const inputLocation = document.querySelector(".search-location");
      const currentLocation = document.querySelector(".location__my-location");
      const or = document.querySelector(".or-text");
      if (this.selectMethod === "currentLocation") {
        inputLocation.style.display = "none";
        or.style.display = "none";
      } else {
        currentLocation.style.display = "none";
        or.style.display = "none";
      }
    },
  },
  created() {
    this.mapbox = null;
  },
};
</script>

<style>
.banner {
  margin-top: 110px;
  padding: 18px 22px;
  background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.5)),
    url("../assets/banner_map.webp");
  color: #ffffff;
  text-align: center;
  border-radius: 3px;
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  word-break: keep-all;
  white-space: normal;
}
.explain {
  font-family: "Do Hyeon", sans-serif;
  font-size: 30px;
  border-left: 5px solid #e0958d;
  padding-left: 12px;
  word-break: keep-all;
  white-space: normal;
}
.explain__description {
  margin: 16px 0;
}
.chips {
  display: flex;
  flex-direction: column;
  align-content: center;
}
.map-gif {
  display: block;
  border-radius: 10px;
  width: 18vw;
  height: auto;
}
.terms {
  padding: 2%;
}
.text-bold {
  font-weight: 600;
}
.address {
  display: flex;
  justify-content: space-between;
}
.location {
  margin-top: 20px;
  padding: 10px 22px;
  width: 100%;
  border: 3px solid #ffb6c1;
  border-radius: 5px;
  background: #FEFCFC;
}
.location__terms {
  margin-right: 3%;
  text-decoration: underline;
  color: grey !important;
}
.location__selection {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  margin-bottom: 46px;
  margin-top: 32px;
}
.location__my-location {
  display: block;
  border: 2px solid #41b6e6;
  padding: 8px 16px;
  border-radius: 5px;
}
.or-text {
  display: inline-block;
}
.location__my-location:hover {
  background-color: #41b6e6;
  color: #eeeeee;
  box-shadow: 0.5px 0.5px grey;
}
.search-location {
  display: inline-block;
}
.location-text {
  background-color: gainsboro;
  border-radius: 5px;
  width: 65%;
  margin-right: 1em;
}
.btn {
  border: 2px solid #ffb6c1;
  padding: 8px 16px;
  border-radius: 5px;
}
.btn:hover {
  background-color: #ffb6c1;
  color: #fff;
  box-shadow: 0.5px 0.5px grey;
}
.terms {
  padding: 12px;
  text-align: center;
}
input[type="checkbox"] {
  display: none;
}
.checkbox-label {
  position: relative;
  margin-left: 28px;
  font-size: 16px;
}
.checkbox-label:hover {
  cursor: pointer;
}
.checkbox-label::before {
  content: "";
  background-image: url("../assets/check-circle.svg");
  background-position: center;
  background-size: contain;
  width: 24px;
  height: 24px;
  position: absolute;
  left: -26px;
  top: -3px;

  transform: scale(0) rotateZ(180deg);
  transition: all 0.4s cubic-bezier(0.54, 0.01, 0, 1.49);
}
input[type="checkbox"]:checked + .checkbox-label::before {
  transform: scale(1) rotateZ(0deg);
}
.checkbox-label::after {
  content: "";
  border: 2px solid #27ae60;
  width: 22px;
  height: 22px;
  position: absolute;
  left: -25px;
  top: -2px;
  border-radius: 50%;
}

.terms__recom {
  display: block;
  margin: 1.5% auto 3% auto;
}
.terms__body {
  padding: 2rem;
}
#map {
  width: 100%;
  height: 25em;
  border-radius: 5px;
}

/* 로케이션 리스트 ! */
.location-list {
  margin-top: 20px;
  width: 40%;
  border: 3px solid #ffb6c1;
  border-radius: 5px;
  margin-left: 1.5rem;
  background: #FCFCEF;
  margin-top: 20px;
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
    display: flex;
    flex-direction: column;
  }
  .location {
    width: 100%;
    margin-bottom: 5%;
    padding: 0;
    margin-top: 5%;
    border: 3px solid #ffb6c1;
    border-left: none;
    border-right: none;
    border-radius: 0;
  }
  .explain {
    border-left: none;
    padding: 0 8px;
  }
  .map-gif {
    width: 45vw;
  }
  .location__selection {
    display: flex;
    flex-direction: column;
    justify-items: center;
    margin: 10px 0;
  }
  .chips {
    display: flex;
    flex-direction: column;
    align-content: center;
  }
  .location-list {
    width: 100%;
    margin-left: 0;
    border-radius: 0;
    border-left: none;
    border-right: none;
  }
}
</style>
