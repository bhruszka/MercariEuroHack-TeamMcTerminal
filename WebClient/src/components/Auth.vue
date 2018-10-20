<template>
  <div>
    <v-btn> Log in with Facebook </v-btn>
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-alert :value="errorText != null" type="error">
        {{errorText}}
      </v-alert>
      <v-btn-toggle v-model="toggleMode" mandatory>
        <v-btn flat>
          Log in
        </v-btn>
        <v-btn flat>
          Sign up
        </v-btn>
      </v-btn-toggle>
      <v-text-field v-model="email" :rules="emailRules" label="E-mail" required></v-text-field>
      <v-text-field v-model="password" :rules="passwordRules" :counter="8" label="Password" type="password" required></v-text-field>
      <v-btn :disabled="!valid" @click="signIn">{{toggleMode == 0 ? "log in" : "sign up"}}</v-btn>
    </v-form>
  </div>
</template>
<script>
import axios from "axios";

export default {
  props: ["user"],
  data() {
    return {
      fbSignInParams: {
        scope: "email",
        return_scopes: true
      },
      myuser: null,
      valid: false,
      password: "",
      passwordRules: [
        v => !!v || "Password is required",
        v => (v && v.length >= 8) || "Password must be at least 8 characters"
      ],
      email: "",
      emailRules: [
        v => !!v || "E-mail is required",
        v => /.+@.+/.test(v) || "E-mail must be valid"
      ],
      errorText: null,
      toggleMode: 0
    };
  },
  methods: {
    signIn() {
      if (this.$refs.form.validate()) {
        var self = this;

        axios
          .request({
            url: `https://carpooling.com.pl:4242/api/${
              this.toggleMode == 0 ? "login" : "sign-in"
            }/`,
            method: "post",
            // headers: {
            //   "Access-Control-Allow-Origin": "*"
            // },
            // withCredentials: true,
            data: {
              email: this.email,
              username: this.email,
              password: this.password
            }
          })
          .then(function(response) {
            console.log(response);
            self.errorText = null;
          })
          .catch(function(error) {
            self.errorText = error.message;
          });
      }
    },
    authStatusChangeCallback(response) {
      var self = this;
      FB.login(
        function(response) {
          console.log(response);
          if (response.status == "connected") {
            console.log(response);
            self.user = response.authResponse.userID;
          }
        },
        { scope: "public_profile,email" }
      );
    },
    facebookLogout() {
      var self = this;
      FB.logout(function(response) {
        self.user = null;
      });
    }
  }
};
</script>
<style>
.fb-signin-button {
  /* This is where you control how the button looks. Be creative! */
  display: inline-block;
  padding: 4px 8px;
  border-radius: 3px;
  background-color: #4267b2;
  color: #fff;
}
</style>