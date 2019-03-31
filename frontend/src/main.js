// Importing packages
import Vue from 'vue'
import VueDragDrop from 'vue-drag-drop';
import VueRouter from 'vue-router';
import BootstrapVue from 'bootstrap-vue'
import VeeValidate from 'vee-validate';
import axios from 'axios'
import VueAxios from 'vue-axios'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// Importing components
import App from './App.vue'
import Login from './components/Login.vue'
import Register from './components/Register.vue'
import Dashboard from './Dashboard.vue'
import Notebook from './components/Notebook.vue'

import UploadData from './components/UploadData.vue'
import BuildModel from './components/BuildModel.vue'
import TrainModel from './components/TrainModel.vue'
import Results from './components/Results.vue'
import InvestigateModel from './components/InvestigateModel.vue'

// VueX store
import {store} from './store/store';


// Registering plugins
Vue.use(VeeValidate);
Vue.use(BootstrapVue);
Vue.use(VueRouter);
Vue.use(VueAxios, axios)
Vue.use(VueDragDrop);


// Defining routes for application
const router = new VueRouter({

  routes : [
  {path:'',redirect:'/login'},
  {path:'/login',component:Login},
  {path:'/register',component:Register},
  {path:'/dashboard',component: Dashboard},
  {path:'/notebook/:notebook_name',component: Notebook,
children: [
  {path:'',redirect:'upload-data'},
  {path:'upload-data',component: UploadData},
  {path:'build-model',component:BuildModel},
  {path:'train-model',component: TrainModel},
  {path:'results',component: Results},
  {path:'investigate-model',component: InvestigateModel}
        ]
        },
],
  mode: 'history'
});



new Vue({
  el: '#app',
  router: router,
  store: store,
  render: h => h(App)
})
