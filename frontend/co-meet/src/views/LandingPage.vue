<template>
  <div>
    <div id="main">
      <video autoplay muted loop id="myVideo">
        <source src="../assets/sub2.mp4" type="video/mp4" />
      </video>
      <div id="box1"></div>

      <div id="box2">
        <div id="text">
          CO-MEET
        </div>
      </div>

      <div id="box3">
        <div id="container">
          <div id="logo">
            <img src="../assets/logo.png" alt="" />
          </div>
          <div id="menu">
            <ul>
              <li>HOME</li>
              <li>SERVICES</li>
              <li>ABOUT</li>
              <li>CONTACT</li>
              <li>HELP</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
body {
  margin: 0px;
}
#main {
  width: 100%;
  height: 100%;
  position: absolute;
  overflow: hidden;
}
#box1 {
  width: 530px;
  height: 625px;
  background-repeat: no-repeat;
  position: absolute;
  bottom: -100%;
  left: 30%;
  animation: anim 2s forwards, anim2 3s forwards 3s;
}
#box1::after {
  content: "";
  position: absolute;
  background-repeat: no-repeat;
  width: 530px;
  height: 625px;
  left: 0px;
  z-index: -1;
}
@keyframes anim {
  from {
    bottom: -100%;
  }
  to {
    bottom: 0%;
  }
}
@keyframes anim2 {
  from {
    left: 30%;
    width: 530px;
  }
  to {
    width: 0px;
    left: 50%;
  }
}
#box2 {
  width: auto;
  height: auto;
  font-family: "Bahnschrift Condensed";
  color: #1b1b1b;
  font-size: 10em;
  line-height: 130px;
  position: absolute;
  top: 250px;
  left: 100px;
  overflow: hidden;
}
#text {
  position: relative;
  left: -100%;
  animation: anim3 2s forwards 3s;
}
@keyframes anim3 {
  from {
    left: -100%;
  }
  to {
    left: 0%;
  }
}
#box3 {
  overflow: hidden;
}
#container {
  width: 100%;
  position: absolute;
  top: -100%;
  animation: anim4 2s forwards 2.5s;
}
#logo {
  float: left;
  margin-left: 100px;
  margin-right: 250px;
  margin-top: 20px;
}
#logo img {
  width: 50px;
}
#menu {
  font-family: "Behnschrift Condensed";
  font-size: 15px;
  color: black;
  letter-spacing: 2px;
  margin-right: 150px;
  margin-top: 40px;
}
#menu ul {
  list-style: none;
}
#menu ul li {
  display: inline-block;
  margin-left: 100px;
}
#myVideo {
  object-fit: cover;
  width: 100vw;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
}
@keyframes anim4 {
  from {
    top: -100%;
  }
  to {
    top: 0%;
  }
}
</style>
