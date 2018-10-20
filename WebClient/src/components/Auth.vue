<template>
    <div>
        <h1>Auth</h1>
        <fb-signin-button :params="fbSignInParams" @success="onSignInSuccess" @error="onSignInError">
            Sign in with Facebook
        </fb-signin-button>
    </div>
</template>
<script>
export default {
  props: ["user"],
  data() {
    return {
      fbSignInParams: {
        scope: "email",
        return_scopes: true
      },
      myuser: null
    };
  },
  methods: {
    onSignInSuccess(response) {
      var self = this;
      FB.api("/me", user => {
        self.myuser = user;
        console.log(user);
        console.log(`Good to see you, ${user.name}.`);
      });
    },
    onSignInError(error) {
      this.user = null;
      console.log("OH NOES", error);
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