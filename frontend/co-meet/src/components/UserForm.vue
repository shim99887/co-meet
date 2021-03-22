<template>
  <v-container style="opacity:0.9;">
    <div class="form-wrap text-center" style="border-radius:10px;">
      <v-row align="center" justify="center" class="text-center mt-5">
        <v-btn-toggle>
          <v-btn
            outlined
            color="pink"
            style="border-top-left-radius:10px;border-bottom-left-radius:10px;"
            width="100px"
            @click="login"
          >
            Login
          </v-btn>
          <v-btn
            outlined
            color="pink"
            style="border-top-right-radius:10px;border-bottom-right-radius:10px;"
            width="100px"
            @click="register"
          >
            REGISTER
          </v-btn>
        </v-btn-toggle>
      </v-row>

      <form id="login" action="" class="input-group">
        <v-text-field label="Email" :rules="emailRules" />
        <v-text-field type="password" label="Password" />
        <v-row align="center">
          <v-col cols="1">
            <v-checkbox />
          </v-col>
          <v-col cols="6" style="font-size:13px;">
            Remember Password
          </v-col>
        </v-row>
        <v-row justify="center" align="center">
          <v-btn outlined color="pink">로그인</v-btn>
        </v-row>
      </form>
      <form id="register" action="" class="input-group">
        <v-row align="center">
          <v-col cols="10">
            <v-text-field label="Email" v-model="user.email" :rules="emailRules" />
          </v-col>
          <v-col cols="2">
            <v-btn width="40px" outlined color="pink">중복체크</v-btn>
          </v-col>
        </v-row>
        <v-text-field type="password" label="Password" v-model="user.pwd" :rules="pwdRules"/>
        <v-text-field type="password" label="Password Confirm" :rules="pwdChkRules" v-model="user.pwdChk" />
        <v-row align="center">
          <v-col cols="1">
            <v-checkbox />
          </v-col>
          <v-col cols="6" style="font-size:13px;">
            Terms and conditions
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-btn outlined color="pink">회원가입</v-btn>
        </v-row>
      </form>
    </div>
  </v-container>
</template>
<script>
export default {
  data(){
    return{
      user:{
        email:'',
        pwd:'',
        pwdChk:'',
      },
      emailRules:[
        v => !!v || 'Email is required',
        v => /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i.test(v) || 'Email must be valid',
      ],
      pwdRules:[
        v => !!v || 'Password is required',
        v => v.length >= 8 || 'Password must be over 8',
      ],
      pwdChkRules:[
        v => v == this.user.pwd || 'Password Check must be equal'
      ],
    }
  },
  props: {
    msg: {
      type: String,
    },
  },
  methods: {
    login() {
      var x = document.getElementById("login");
      var y = document.getElementById("register");
      var z = document.getElementById("btn");
      x.style.left = "50px";
      y.style.left = "450px";
      z.style.left = "0";
    },
    register() {
      var x = document.getElementById("login");
      var y = document.getElementById("register");
      var z = document.getElementById("btn");
      x.style.left = "-400px";
      y.style.left = "50px";
      z.style.left = "110px";
    },
  },
};
</script>
<style scoped>
* {
  margin: 0;
  padding: 0;
  font-family: sans-serif;
}

.wrap {
  height: 100%;
  width: 100%;
  background-position: center;
  opacity: 0.8;
  background-size: cover;
  /* position: absolute; */
}
.form-wrap {
  width: 380px;
  height: 480px;
  position: relative;
  /* margin: 6% auto; */
  background: #fff;
  padding: 5px;
  overflow: hidden;
}
.togglebtn {
  padding: 10px 30px;
  cursor: pointer;
  background: transparent;
  border: 0;
  outline: none;
  position: relative;
}
.input-group {
  top: 100px;
  position: absolute;
  width: 280px;
  transition: 0.5s;
}
.input-field {
  width: 100%;
  padding: 10px 0;
  margin: 5px 0;
  border: none;
  border-bottom: 1px solid #999;
  outline: none;
  background: transparent;
}
.submit {
  width: 85%;
  padding: 10px 30px;
  cursor: pointer;
  display: block;
  margin: auto;
  background: linear-gradient(to right, #ff105f, #ffad06);
  border: 0;
  outline: none;
  border-radius: 30px;
}
.checkbox {
  margin: 30px 10px 30px 0;
}
span {
  color: #777;
  font-size: 12px;
  bottom: 68px;
  position: absolute;
}
#login {
  left: 50px;
}
#register {
  left: 450px;
}
</style>
