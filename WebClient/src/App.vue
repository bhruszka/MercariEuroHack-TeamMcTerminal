<template>
  <v-app>
    <v-toolbar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>Vuetify</span>
        <span class="font-weight-light">MATERIAL DESIGN</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn flat @click-native="facebookLogout">
        <span class="mr-2">Latest Release</span>
        <v-icon>open_in_new</v-icon>
      </v-btn>
    </v-toolbar>

    <v-content>
      <!-- <Auth :user="user" /> -->
      <div v-if="user != null">
        User: {{user}}
        <SelectRole v-if="role == null" v-on:set-role="role = $event" />
        <h1 v-else>Role: {{role}} </h1>
        <DriverForm v-if="role == 'driver'"/>
        <PassangerForm v-if="role == 'passanger'"/>
        <WaitForRide />
      </div>
    </v-content>
  </v-app>
</template>

<script>
import Auth from "./components/Auth";
import SelectRole from "./components/SelectRole";
import DriverForm from "./components/DriverForm";
import PassangerForm from "./components/PassangerForm";
import WaitForRide from "./components/WaitForRide";

export default {
  name: "App",
  components: {
    Auth,
    SelectRole,
    DriverForm,
    PassangerForm,
    WaitForRide
  },
  data() {
    return {
      user: null,
      role: null
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
      console.log("test")
      FB.getLoginStatus(function(response) {
        console.log("getLoginStatus")
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
            console.log(response)
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
