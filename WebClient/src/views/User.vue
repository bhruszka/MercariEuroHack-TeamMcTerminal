<template>
  <div style="height: 100%">
    <v-toolbar height="64px" style="z-index: 5">
      <v-toolbar-title class="headline text-uppercase">
        <span class="font-weight-light">CARPOOL APP</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="user != null" @click.native="facebookLogout"> Log out </v-btn>
      <img v-if="user != null" class="circle-avatar" :src="'https://carpooling.com.pl:4242'+user.avatar" />
    </v-toolbar>

    <v-alert :value="errorText != null" type="error">
      {{errorText}}
    </v-alert>
    <v-layout row wrap d-flex v-if="user == null" class="tall">
      <v-flex xs12 style="height: 100%">
        <v-card style="height: 100%" class="login-background">
          <!-- <img src="./assets/background.jpg" style="width: 100%;" /> -->
          <v-layout column d-flex style="height: 100%">
            <div style="flex-grow: 10;"></div>
            <v-card-title primary-title style="flex-grow: 0 !important; margin-left: 11px;">
              <div class="headline" style="text-shadow: 2px 2px 2px rgb(0, 0, 0);font-size: 40px !important;"><b>Stop driving alone - Start carpooling and battle traffic with us</b></div>
            </v-card-title>
            <v-card-actions style="flex-grow: 0 !important; margin-bottom: 150px;  margin-top: 20px; margin-left: 15px;">
              <v-btn :disabled="!facebookInit" @click.native="facebookLogin" color="blue"> Sign in with Facebook </v-btn>
            </v-card-actions>
          </v-layout>
        </v-card>
      </v-flex>
    </v-layout>
    <div class="tall" v-else>
      <div v-if="addRoute" style="height: 100%">
        <SelectRole v-if="role == null" v-on:set-role="role = $event" />
        <div v-if="route == null">
          <DriverForm v-if="role == 'driver'" @cancel="role = null" @submit="submitRoute($event)" />
          <PassengerForm v-if="role == 'passenger'" @cancel="role = null" @submit="submitRoute($event)" />
        </div>
        <!-- <div v-else>
          <v-btn @click.native="submitRoute">Submit Route</v-btn>
          <v-btn @click.native="addRoute=false">Cancel</v-btn>
        </div> -->
      </div>
      <div v-else style="height: 100%; display: flex">
        <v-flex xs3>
          <v-btn @click.native="addRoute = true" class="ma-0" style="width: 100%" color="red">Add Route</v-btn>
        </v-flex>
        <v-flex xs9>
          <PolyMap :path="path" :full_path="full_path" :users="users" />
        </v-flex>
      </div>
    </div>
  </div>
</template>
<script>
import Auth from "../components/Auth";
import SelectRole from "../components/SelectRole";
import DriverForm from "../components/DriverForm";
import PassengerForm from "../components/PassengerForm";
import WaitForRide from "../components/WaitForRide";
import PolyMap from "../components/PolyMap";

import axios from "axios";

export default {
  name: "App",
  components: {
    Auth,
    SelectRole,
    DriverForm,
    PassengerForm,
    WaitForRide,
    PolyMap
  },
  data() {
    return {
      user: null,
      role: null,
      userData: null,
      facebookInit: false,
      errorText: null,
      route: null,
      addRoute: false,
      existingRoutes: [],
      path: null,
      full_path: null,
      users: []
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
      var self = this;
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
          self.getMyRoutes();
          self.getMyProfile();
        })
        .catch(function(error) {
          self.errorText = error.message;
        });
    },
    submitRoute(event) {
      this.route = event;
      var self = this;

      axios
        .get(
          `https://carpooling.com.pl:4242/api/routes/clear_my_path/?userId=${
            this.user.userId
          }&token=${this.user.token}`
        )
        .then(function(response) {
          console.log(response);
          self.errorText = null;
          self.submitRoute2(event);
        })
        .catch(function(error) {
          self.errorText = error.message;
        });
    },
    submitRoute2(event) {
      this.route = event;
      var self = this;

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
          self.getMyRoutes();
          self.getMyProfile();
        })
        .catch(function(error) {
          self.errorText = error.message;
        });
      this.role = null;
      this.route = null;
    },
    getMyRoutes() {
      var self = this;
      axios
        .get(
          `https://carpooling.com.pl:4242/api/routes/path/?userId=${
            this.user.userId
          }&token=${this.user.token}`
        )
        .then(function(response) {
          self.full_path = response.data.full_path;
          self.path = response.data.path;
          self.users = response.data.users;
          console.log(response);
          self.addRoute = false;
          self.errorText = null;
        })
        .catch(function(error) {
          self.errorText = error.message;
        });
    },
    getMyProfile() {
      var self = this;
      axios
        .get(
          `https://carpooling.com.pl:4242/api/user/your_profile/?userId=${
            this.user.userId
          }&token=${this.user.token}`
        )
        .then(function(response) {
          self.path = response.data.path;
          console.log(response);
          self.user = {
            ...self.user,
            avatar: response.data.avatar,
            first_name: response.data.first_name,
            last_name: response.data.last_name
          };
          self.addRoute = false;
          self.errorText = null;
        })
        .catch(function(error) {
          self.errorText = error.message;
        });
    }
  }
};
</script>
<style>
.tall {
  height: calc(100% - 64px);
}
.circle-avatar {
  border-radius: 25px;
}
.login-background {
  background-image: url("https://carpooling.com.pl:4242/static/gangsta.jpg");
  background-size: cover;
}
</style>
