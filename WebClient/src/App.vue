<template>
  <v-app>
    <v-toolbar app>
      <v-toolbar-title class="headline text-uppercase">
        <span class="font-weight-light">CARPOOL APP</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="user != null" @click.native="facebookLogout"> Log out </v-btn>
      <span v-else>
        User: {{user}}
      </span>
    </v-toolbar>
    <v-container>

      <v-content>
        <v-container>
          <v-layout row wrap>
            <v-flex xs12 v-if="user == null" fill-height>
              <v-card>
                <img src="./assets/background.jpg"/>
                
                <v-card-title primary-title>
                  <div class="headline">To start carpooling sign in with Facebook</div>
                  <!-- <div>Listen to your favorite artists and albums whenever and wherever, online and offline.</div> -->
                </v-card-title>
                <v-card-actions>
                  <v-btn :disabled="!facebookInit" @click.native="facebookLogin"> Sign in with Facebook </v-btn>
                </v-card-actions>
              </v-card>
            </v-flex>
          </v-layout>
          <v-alert :value="errorText != null" type="error">
            {{errorText}}
          </v-alert>
        </v-container>
        <!-- <Auth :user="user" /> -->
        <!-- <Auth /> -->
        <v-alert :value="errorText != null" type="error">
          {{errorText}}
        </v-alert>
        <div v-if="user != null">
          <SelectRole v-if="role == null" v-on:set-role="role = $event" />
          <DriverForm v-if="role == 'driver'" @cancel="role = null" />
          <PassengerForm v-if="role == 'passenger'" @cancel="role = null" />
          <WaitForRide v-if="userData != null" />
        </div>
      </v-content>
    </v-container>
  </v-app>
</template>

<script>
import Auth from "./components/Auth";
import SelectRole from "./components/SelectRole";
import DriverForm from "./components/DriverForm";
import PassengerForm from "./components/PassengerForm";
import WaitForRide from "./components/WaitForRide";
import axios from "axios";

export default {
  name: "App",
  components: {
    Auth,
    SelectRole,
    DriverForm,
    PassengerForm,
    WaitForRide
  },
  data() {
    return {
      user: null,
      role: null,
      userData: null,
      facebookInit: false,
      errorText: null
      //
    };
  },
  created() {
    var self = this;

    window.fbAsyncInit = function() {
      FB.init({
        appId: "162998601309144",
        autoLogAppEvents: true,
        xfbml: true,
        version: "v3.1"
      });
      FB.getLoginStatus(function(response) {
        self.authStatusChangeCallback(response);
      });
    };

    (function(d, s, id) {
      var js,
        fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) {
        return;
      }
      js = d.createElement(s);
      js.id = id;
      js.src = "https://connect.facebook.net/en_US/sdk.js";
      fjs.parentNode.insertBefore(js, fjs);
    })(document, "script", "facebook-jssdk");
  },
  methods: {
    authStatusChangeCallback(response) {
      this.facebookInit = true;
      if (response.status == "connected") {
        this.user = {};
        this.user.userId = response.authResponse.userID;
        this.user.token = response.authResponse.accessToken;
        this.serverLogin();
      }
    },
    facebookLogin() {
      this.user = null;
      var self = this;
      FB.login(
        function(response) {
          // console.log(response);
          if (response.status == "connected") {
            self.user = {};
            self.user.userId = response.authResponse.userID;
            self.user.token = response.authResponse.accessToken;
            self.serverLogin();
          }
        },
        { scope: "public_profile,email" }
      );
    },
    facebookLogout() {
      var self = this;
      FB.logout(function(response) {
        self.user = null;
        window.location.reload();
      });
    },
    serverLogin() {
      axios
        .post("https://carpooling.com.pl:4242/login-facebook", {
          userId: this.user.userId,
          token: this.user.token
          // headers: {
          //   "Access-Control-Allow-Origin": "*"
          // }
        })
        .then(function(response) {
          console.log(response);
          self.errorText = null;
        })
        .catch(function(error) {
          self.errorText = error.message;
        });
    }
  }
};
</script>
