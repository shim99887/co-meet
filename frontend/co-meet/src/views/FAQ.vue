<template>
  <v-container>
    <navbar />
    <video autoplay muted loop id="myVideo">
        <source src="../assets/sub2.mp4" type="video/mp4" />
    </video>
    <v-card
      style="margin-top: 80px;width:100%;"
      class="text-center"
    >
    <div class="banner" style="height:250px;">
      
    </div>
    <div style="margin-top:20px;margin-bottom:20px;">

        <div style="font-family: 'Do Hyeon', sans-serif;font-size:30px;">
          궁금한 것을 검색해보세요
        </div>
        <v-text-field
          v-model="search"
          style="width:290px;margin:0px auto;"
          placeholder="검색할 사항 입력"
        ></v-text-field>
        <div style="font-family: 'Do Hyeon', sans-serif;">
          아래의 목록에서 자세한 답변을 얻을 수 있습니다.
        </div>

    </div>
      <v-data-table
      class="text-lg"
        :headers="headers"
        :items="items"
        show-expand
        item-key="no"
        @click:row="(item, slot) => slot.expand(!slot.isExpanded)"
        :search="search"
      >
        <template v-slot:expanded-item="{ headers, item }">
          <td :colspan="headers.length">{{item.내용}}</td>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>
<script>
import navbar from "@/components/navbar.vue";

export default {
  components: {
    navbar,
  },
  data() {
    return {
      search: "",
      headers: [
        { text: "no", value: "no" },
        { text: "구분", value: "구분" },
        { text: "제목", value: "제목" },
      ],
      items: require("@/data/data.json"),
    };
  },
};
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Do+Hyeon&display=swap');
/* .banner{
  background-image: url("https://img.freepik.com/free-photo/business-man-hand-holding-wooden-cube-with-faq-text_42256-1160.jpg?size=626&ext=jpg");
  width:100%;
  height: 100px;
} */
.banner{
  margin-top: 120px;
  padding: 18px 22px;
  background-image: linear-gradient( rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.5) ), url("../assets/faq.png");
  color:#ffffff;
  text-align: center;
  border-radius: 2px;
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}
</style>