<template>
  <v-app>
    <v-toolbar height="64px">
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
      <v-layout row wrap d-flex v-if="user == null">
        <v-flex xs12>
          <v-card>
            <!-- <img src="./assets/background.jpg" style="width: 100%;" /> -->
            <v-card-title primary-title>
              <div class="headline">To start carpooling sign in with Facebook</div>
            </v-card-title>
            <v-card-actions>
              <v-btn :disabled="!facebookInit" @click.native="facebookLogin"> Sign in with Facebook </v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
      <div v-else>
        <v-layout row wrap d-flex v-else>
          <SelectRole v-if="role == null" v-on:set-role="role = $event" />
          <div v-if="route == null">
            <DriverForm v-if="role == 'driver'" @cancel="role = null" @submit="route = $event" />
            <PassengerForm v-if="role == 'passenger'" @cancel="role = null" @submit="route = $event" />
          </div>
          <div v-else>
            <v-btn @click.native="submitRoute">Submit Route</v-btn>
          </div>
        </v-layout>
        <v-layout row wrap d-flex>
          <v-flex xs12 v-if="user == null">
            <v-card>
              <!-- <img src="./assets/background.jpg" style="width: 100%;" /> -->

              <v-card-title primary-title>
                <div class="headline">To start carpooling sign in with Facebook</div>
              </v-card-title>
              <v-card-actions>
                <v-btn :disabled="!facebookInit" @click.native="facebookLogin"> Sign in with Facebook </v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
          <div v-else>
            <SelectRole v-if="role == null" v-on:set-role="role = $event" />
            <div v-if="route == null">
              <DriverForm v-if="role == 'driver'" @cancel="role = null" @submit="route = $event" />
              <PassengerForm v-if="role == 'passenger'" @cancel="role = null" @submit="route = $event" />
            </div>
            <div v-else>
              <v-btn @click.native="submitRoute">Submit Route</v-btn>
            </div>
          </div>
        </v-layout>
      </div>
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
      errorText: null,
      route: null
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
