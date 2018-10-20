<template>
  <v-app>
    <v-toolbar app>
      <v-toolbar-title class="headline text-uppercase">
        <span class="font-weight-light">CARPOOL APP</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <span>
        User: {{user}}
      </span>
    </v-toolbar>
    <v-container>

      <v-content>
        <!-- <Auth :user="user" /> -->
        <!-- <Auth /> -->
        <v-btn v-if="user == null" :disabled="!facebookInit" @click.native="facebookLogin"> Log in with Facebook </v-btn>
        <v-btn v-else @click.native="facebookLogout"> Log out </v-btn>
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
      facebookInit: false
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
      } else {
        this.facebookLogin();
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
    }
  }
};
</script>
