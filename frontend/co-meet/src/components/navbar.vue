<template>
<div>
  <div id="navbar">

      <div class="navbar__logo">
        <img src="@/assets/logo.png" alt="logo">
        <!-- 이거 라우트 링크 써야됌 -->
        <a @click="$router.push('/')">Co-Meet</a>
        <!-- <div>Co-Meet</div> -->

      <a href="#" 
      class="navbar__toggle"
      @click="onToggle"
      >
        <i class="fas fa-bars"></i>
      </a>

      </div>


    <ul class="navbar__menus">
      <router-link v-if="$store.getters.getUserEmail" to="/recommendation" class="navbar__community__button">
        <li>지역 추천</li>
      </router-link>
      <router-link to="/faq" class="navbar__community__button">
        <li>FAQ</li>
      </router-link>
    </ul>
  <!-- 이것도 라우터 링크 써야됌 -->
    <ul class="navbar__community" v-if="!$store.getters.getAccessToken">
      <a class="navbar__community__button" href="#" @click="loginToggle"><li>로그인</li></a>
      <a class="navbar__community__button" href="#" @click="registToggle"><li>회원 가입</li></a>
    </ul>
    <ul class="navbar__community" v-else>
      <span class="navbar__community__button">{{$store.getters.getUserName}}님</span>
      <a class="navbar__community__button" href="#" @click="logout"><li>로그아웃</li></a>
    </ul>
  </div>
</div>
</template>

<script>

export default {
  name: "navbar",
  methods: {
    onToggle () {
      const menus = document.querySelector(".navbar__menus")
      const community = document.querySelector(".navbar__community")
      menus.classList.toggle("active")
      community.classList.toggle("active")
    },
    loginToggle(){
      this.$emit("msg", 'login');
    },
    registToggle(){
      this.$emit("msg", 'regist');
    },
    logout(){
      this.$store.dispatch('LOGOUT', this.$store.getters.getUserEmail);
      this.$fire({
        type:'success',
        title:'로그아웃',
        text:'성공',
        timer: 3000,
      })
    }
  },

}
</script>

<style scoped>

  :root {
    --navbar--text-color: #ffb6c1;
  }
  #navbar {
    z-index: 1;
    display: flex;
    justify-content: space-between;
    padding: 0.6rem;
    margin-right: auto;
    margin-left: auto;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 5px;
    animation: anim4 2.0s forwards 1.0s;
    position: absolute;
    left: 9.5%;
    width: 81%;
    font-family: 'Gugi', cursive;
  }
  @keyframes anim4 {
  from {
    top: -100%;
  }
  to {
    top: 2%;
  }
}
  .navbar__logo {
    display: flex;
    align-items: center;

  }
  .navbar__logo img {
    display: inline-block;
    height: 3em;
  }
  .navbar__logo a {
    display: inline-block;
    text-decoration: none;
    font-size: 30px;
    color: #ffb6c1;
  }
  .navbar__menus {
    list-style: none;
    padding-left: 0;
    display: flex;
    align-items: center;
  }
  .navbar__community {
    list-style: none;
    padding-left: 0;
    display: flex;
    align-items: center;
  }
  .navbar__community__button {
    text-decoration: none;
    padding: 8px 12px;
    font-weight: 700;
    opacity: 1;
    color: #ffb6c1;
  }
  .navbar__community__button:hover{
    background-color: rgb(241, 223, 239);
    border-radius: 5px;
    color: #1b1b1b;
  }
  .navbar__community__button:nth-child(2) {
    margin-left: 2em;
  }
  .navbar__toggle {
    /* color: var(--navbar--text-color); */
    text-decoration: none;
    position: absolute;
    right: 5%;
    display: none !important;
    
    z-index: 1;
    font-size: 1.6rem;
    color: #ffb6c1;
    /* width: fit-content; */
  }
  @media screen and (max-width: 48rem) {
    #navbar {
      flex-direction: column;
      background-color: rgba(0, 0, 0, 0.9);
      width: 96%;
      left: 2%;
    }
    .navbar__toggle {
      display: block !important;

    }
    .navbar__community__button {
      width: 100%;
      text-align: center;
      margin: 2px 0;
      border: 2px solid rgb(241, 223, 239);
      border-radius: 5px;
    }

    .navbar__menus {
      display: none;
    }
    .navbar__community {
      margin-top: 1vh;
      display: none;
    }
    .navbar__menus.active,
    .navbar__community.active {
      display: flex;
    }
  }

</style>