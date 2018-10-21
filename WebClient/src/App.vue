<template>
  <v-app dark>
     <router-view></router-view>
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
      errorText: null,
      route: null
      //
    };
  },
  created() {
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
        .post("https://carpooling.com.pl:4242/api/login-facebook/", {
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
    },
    submitRoute() {
      axios
        .post("https://carpooling.com.pl:4242/api/routes/", {
          userId: this.user.userId,
          token: this.user.token,
          end_point: this.route.destination,
          start_point: this.route.startPoint,
          type: this.role
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
