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
        <v-text-field
          label="Email"
          v-model="loginInfo.email"
          :rules="emailRules"
        />
        <v-text-field
          type="password"
          v-model="loginInfo.password"
          label="Password"
        />
        <v-row align="center">
          <v-col cols="1">
            <v-checkbox />
          </v-col>
          <v-col cols="6" style="font-size:13px;">
            Remember Password
          </v-col>
        </v-row>
        <v-row justify="center" align="center">
          <v-btn outlined color="pink" @click="loginComp">로그인</v-btn>
        </v-row>
      </form>
      <form id="register" action="" class="input-group">
        <v-row align="center">
          <v-col cols="10" style="padding:0px;">
            <v-text-field
              label="Email"
              v-model="user.email"
              :rules="emailRules"
            />
          </v-col>
          <v-col cols="2">
            <v-btn width="40px" outlined color="pink" @click="emailCheck"
              >중복체크</v-btn
            >
          </v-col>
        </v-row>
        <v-row align="center">
          <v-col cols="10" style="padding: 0px;">
            <v-text-field
              label="NickName"
              :rules="nameRules"
              v-model="user.nickname"
            />
          </v-col>
          <v-col cols="2">
            <v-btn width="40px" outlined color="pink" @click="nameCheck"
              >중복체크</v-btn
            >
          </v-col>
        </v-row>
        <v-text-field
          type="password"
          label="Password"
          v-model="user.password"
          :rules="pwdRules"
        />
        <v-text-field
          type="password"
          label="Password Confirm"
          :rules="pwdChkRules"
          v-model="pwdChk"
        />
        <v-row align="center">
          <v-col cols="1">
            <v-checkbox />
          </v-col>
          <v-col cols="6" style="font-size:13px;">
            Terms and conditions
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-btn outlined color="pink" @click="registComp">회원가입</v-btn>
        </v-row>
      </form>
    </div>
  </v-container>
</template>
<script>
import axios from "axios";
import { mapGetters } from "vuex";

const SERVER_URL = process.env.VUE_APP_SERVER_URL;

export default {
  data() {
    return {
      user: {
        email: "",
        nickname: "",
        password: "",
      },
      loginInfo: {
        email: "",
        password: "",
      },
      pwdChk: "",
      emailRules: [
        (v) => !!v || "Email is required",
        (v) =>
          /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i.test(
            v
          ) || "Email must be valid",
      ],
      nameRules: [(v) => !!v || "Name is required"],
      pwdRules: [
        (v) => !!v || "Password is required",
        (v) => v.length >= 8 || "Password must be over 8",
      ],
      pwdChkRules: [
        (v) => v == this.user.password || "Password Check must be equal",
      ],
      nameChecked: false,
      emailChecked: false,
    };
  },
  props: {
    msg: {
      type: String,
    },
  },
  computed: {
    ...mapGetters(["getUserName", "getAccessToken", "getUserEmail"]),
  },
  methods: {
    login() {
      var x = document.getElementById("login");
      var y = document.getElementById("register");
      // var z = document.getElementById("btn");
      x.style.left = "50px";
      y.style.left = "450px";
      // z.style.left = "0";
    },
    register() {
      var x = document.getElementById("login");
      var y = document.getElementById("register");
      // var z = document.getElementById("btn");
      x.style.left = "-400px";
      y.style.left = "50px";
      // z.style.left = "110px";
    },
    loginComp() {
      this.$store.dispatch("LOGIN", this.loginInfo);

      setTimeout(() => {
        if (!this.$store.getters.getAccessToken) {
          this.$fire({
            type: "error",
            title: "로그인 실패",
            timer: 3000,
          });
          } else {
            this.$fire({
              type: "success",
              title: "로그인 성공",
              timer: 3000,
            }).then(() => {
              location.reload();
            })
        }

      }, 1500);
    },
    registComp() {
      if (
        this.nameChecked &&
        this.emailChecked &&
        this.user.password &&
        this.user.password == this.pwdChk
      ) {
        axios
          .post(`${SERVER_URL}/user/`, this.user)
          .then(() => {
            this.$fire({
              type: "success",
              title: "회원가입 성공",
              text:
                "회원가입을 성공했습니다. 가입하신 아이디로 이메일을 발송했으니 인증 후 이용가능합니다.",
              timer: 3000,
            });
          })
          .catch((error) => {
            this.$fire({
              type: "error",
              title: "회원가입 오류 발생",
              text: error,
              timer: 3000,
            });
          });
      } else {
        if (!this.nameChecked) {
          this.$fire({
            type: "error",
            title: "닉네임 중복 미체크",
            timer: 3000,
          });
        }
        if (!this.emailChecked) {
          this.$fire({
            type: "error",
            title: "이메일 중복 미체크",
            timer: 3000,
          });
        }
        if (!this.user.password) {
          this.$fire({
            type: "error",
            title: "비밀번호를 입력해주세요",
            timer: 3000,
          });
        }
        if (this.user.password != this.pwdChk) {
          this.$fire({
            type: "error",
            title: "비밀번호가 일치하지 않습니다.",
            timer: 3000,
          });
        }
      }
    },
    emailCheck() {
      if (
        /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i.test(
          this.user.email
        )
      ) {
        axios
          .get(`${SERVER_URL}/user/email/` + this.user.email)
          .then(() => {
            this.$fire({
              title: "이메일 중복체크",
              text: "성공",
              type: "success",
              timer: 3000,
            });
            this.emailChecked = true;
          })
          .catch(() => {
            this.$fire({
              title: "이메일 중복체크",
              text: "실패",
              type: "error",
              timer: 3000,
            });
            this.emailChecked = false;
          });
      } else {
        this.$alert("이메일 양식을 확인해주세요.");
      }
    },
    nameCheck() {
      axios
        .get(`${SERVER_URL}/user/nickname/` + this.user.nickname)
        .then(() => {
          this.$fire({
            title: "닉네임 중복체크",
            text: "성공",
            type: "success",
            timer: 3000,
          });
          this.nameChecked = true;
        })
        .catch(() => {
          this.$fire({
            title: "닉네임 중복체크",
            text: "실패",
            type: "error",
            timer: 3000,
          });
          this.nameChecked = false;
        });
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
  height: 510px;
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
