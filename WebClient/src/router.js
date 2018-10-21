import Vue from "vue";
import Router from "vue-router";
import User from "./views/User";
import Test from "./views/Test";
import City from "./views/City";

Vue.use(Router);

export default new Router({
  routes: [
    { path: "/", component: User },
    { path: "/test", component: Test },
    { path: "/city", component: City }
  ]
});
