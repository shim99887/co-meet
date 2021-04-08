<template>
  <div class="graph" v-if="cities.length">
      <section class="graph__header">

        <h1 class="graph__title"><span style="color: #36a2eb">{{targets}}</span>의 검색 결과 안내</h1>
        <h4 class="graph__description">추천 받으신 장소는 다양한 데이터를 통해 연산되어 제공합니다</h4>
      </section>
      <section class="graph__reason ">
        <h4><b style="color:#A3A3FF; padding-left: 1rem; border-left: 6px solid pink">지난달 서울시 구별</b>에 대한 확진자 데이터입니다.</h4>
        <Barchart class="graph__chart" v-if="gugun.length"/>
        <h4><b style="color:#A3A3FF; padding-left: 1rem; border-left: 6px solid pink">추천 받은 장소</b>에 대한 확진자 데이터입니다.</h4>
        <Linechart class="graph__chart" v-if="cities.length"/>
      </section>
      <section class="graph__footer">
        <button class="graph-btn" @click="reRecom"> <b>새로운 장소 <br> 추천받기</b> </button>
        <!-- <h4 class="footer__description">장소를 재추천 받으시려면 버튼을 누르세요</h4> -->
      </section>
  </div>
</template>

<script>
import Barchart from "@/components/graph/Barchart.vue"
import Linechart from "@/components/graph/LineChart.vue"

export default {
  components: {
    Barchart,
    Linechart,
  },
  data() {
    return {
      searchResult: [],
    }
  },
  computed: {
    gugun() {
      return this.$store.getters.get_gugun
    },
    cities() {
      return this.$store.getters.get_result;
    },
    citiesDate() {
      return this.$store.getters.get_month;
    },
    citiesPatients() {
      return this.$store.getters.get_patients
    },
    citiesCoordinates() {
      return this.$store.getters.get_coordinates
    },
    targets() {
      return this.$store.getters.get_targets.join(', ')
    },
  },
  methods:{
    reRecom(){
      this.$store.commit('MAPCANCLE');
    }
  },
  destroyed() {
    this.$store.commit("MAPCANCLE")
    
  },


}
</script>

<style lang='scss' >
  $dark-blue: #839ba5;
  $inside-border: 2px solid $dark-blue;
  
  @mixin textLayout() {
    padding-bottom: 0.25em;
    // border-bottom: 2px solid $dark-blue;
  }

  @mixin borderLayout($color) {
    // border: 3px solid $color;
    border-radius: 5px;
    padding: 1rem;
  } 
  
  .graph {
    @include borderLayout(#41b6e6);
    margin-top: 1em;
    background: #FCFCEF;

    &__title {
      @include textLayout();
      border-bottom: 2px solid $dark-blue;
    }

    &__description {
      @include textLayout();
      margin-top: 0.5rem;
    }
    &__chart {
      width: 100%;
      padding: 1rem;
    }
    &__non-data {
      width: 100%;
      padding: 1rem 0;
    }
    &__footer {
      margin-top: 2em;
      // border-top: $inside-border;
      padding-top: 1em;
      display: flex;
      flex-direction: column;
      align-items: center;

      .graph-btn {
        padding: 10px 18px;
        background-color: #fcfcef;
        border-radius: 5px;
        width: 30vw;
        border: 2px solid #ffb6c1;
        box-shadow: 0.5px 0.5px grey;
        &:hover {
          background-color: #ffb6c1;
          box-shadow: 0.5px 0.5px grey;
          color: white;
        }
      }
      .footer__description {
        color: lightslategray;
        margin-top: 0.4rem;
      }
    }
  }
  @media screen and (max-width: 48rem) {
    .graph {
      border-radius: 0;
      &__footer{
        .graph-btn {
          width: 61vw;
        }
      }
    }
  }
</style>
