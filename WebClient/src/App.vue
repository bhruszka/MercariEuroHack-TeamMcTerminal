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
        <Auth />
        <div v-if="user != null">
          <SelectRole v-if="role == null" v-on:set-role="role = $event" />
          <DriverForm v-if="role == 'driver'" @cancel="role = null"/>
          <PassengerForm v-if="role == 'passenger'" @cancel="role = null"/>
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
      userData: null
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
      console.log("test");
      FB.getLoginStatus(function(response) {
        console.log("getLoginStatus");
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
