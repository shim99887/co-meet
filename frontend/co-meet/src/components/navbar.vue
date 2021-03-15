<template>
<div>
  <div id="navbar">
    <div class="navbar__logo">
      <img src="@/assets/Logo.png" alt="logo">
      <!-- 이거 라우트 링크 써야됌 -->
      <a href="#">Co-Meet</a>
    </div>
    <ul class="navbar__menus">
      <router-link to="/recommendation" class="navbar__community__button">
        <li>지역 추천</li>
      </router-link>
    </ul>
    <ul class="navbar__community">
      <a class="navbar__community__button" href="#"><li>로그인</li></a>
      <a class="navbar__community__button" href="#"><li>회원 가입</li></a>
    </ul>
  </div>
  <!-- 이것도 라우터 링크 써야됌 -->
  <a href="#" 
   class="navbar__toggle"
   @click="onToggle"
  >
    <i class="fas fa-bars"></i>
  </a>
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
  },

}
</script>

<style scoped>
  :root {
    --navbar--text-color: #ffb6c1;
  }
  #navbar {
    z-index: 1;
    position: absolute;
    top: -100%;
    left: 2%;
    width: 95vw;
    display: flex;
    justify-content: space-between;
    padding: 0.6rem;
    margin-right: auto;
    margin-left: auto;
    background-color: rgba(0, 0, 0, 0.6);
    border-radius: 5px;
    animation: anim4 2s forwards 2.0s;
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
    position: relative;
    right: -88%;
    top: 1.35em;
    z-index: 1;
    display: none;
    font-size: 1.6rem;
    color: #ffb6c1;
    width: fit-content;
  }
  @media screen and (max-width: 48rem) {
    #navbar {
      flex-direction: column;
    }
    .navbar__toggle {
      display: block;

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