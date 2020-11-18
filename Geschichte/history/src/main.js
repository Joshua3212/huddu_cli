import Vue from 'vue'
import VueRouter from 'vue-router';
import App from './App.vue'
import home from './routes/home.vue'
Vue.use(VueRouter);
Vue.config.productionTip = false

const routes = [
  {
    path: '/',
    component: home
  }

]


const router = new VueRouter({
  routes,
  mode: 'history',
});


new Vue({router,
  render: h => h(App),
}).$mount('#app')
