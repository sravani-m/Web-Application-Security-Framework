<template>
  <div>

     <div id="notebook-app">
    <!-- The top header -->
    <b-container fluid class="rounded bg-primary">
      <br>
      <b-row class="header ">
        <b-col class="text-white h5"><img src="./../assets/company-logo.png" width=40px height=40px></img>Web App Vulnerability <span class="font-weight-bold">Scanner</span></b-col>
        <b-col cols="7" class="text-center h4 font-weight-bold text-white" id="notebook_name"> {{notebook_name}}</b-col>
        <b-col class="text-right">
          <b-button variant="primary" class="glyphicon glyphicon-pencil text-right text-white">  Welcome {{this.$store.state.loggedUser}} <i data-feather="user"></i></b-button>
        <!--   <b-button variant="primary" @click="logOutUser">  Logout <i data-feather="log-out"></i></b-button> -->

        </b-col>
      </b-row>

      <b-modal id="change_notebook_name" title="Enter notebook name">
        <b-form-input type="text" :value="notebook_name" placeholder="Enter notebook name" v-model="notebook_name"></b-form-input>
      </b-modal>
    </b-container>

    <!-- Right sidebar -->
    <div class="sidebar  bg-light text-white">
      <a class="bg-dark" @click="goToDashboard()"><i data-feather="home"></i></a>
      <a href="#" @click="exportPDF()"><i data-feather="save"></i></a>
    </div>

    <!-- Top navbar -->
      <b-nav fill tabs class="bg-light font-weight-bold" style="font-family: 'Roboto', sans-serif;">
        <b-nav-item :to="{path:'/notebook/'+notebook_name+'/upload-data'}">SELECT TOOLS</b-nav-item>
        <b-nav-item :to="{path:'/notebook/'+notebook_name+'/results'}" >SCAN REPORT</b-nav-item>
        <!-- <b-nav-item :to="{path:'/notebook/'+notebook_name+'/train-model'}">TRAIN </b-nav-item>
        <b-nav-item :to="{path:'/notebook/'+notebook_name+'/results'}">RESULTS</b-nav-item> -->
        <!-- <b-nav-item :to="{path:'/notebook/'+notebook_name+'/investigate-model'}">INVESTIGATE MODEL</b-nav-item> -->
      </b-nav>
      <br>

  </div>

    <keep-alive>
      <router-view></router-view>
    </keep-alive>

  </div>
</template>

<script>

  export default {
    mounted() {
      feather.replace()
    },

    data: function(){
      return {
        notebook_name: this.$route.params.notebook_name
      }
    },
    methods:{
      // Goes to dashboard page
      goToDashboard(){
        this.$router.push('/dashboard');
        this.$store.state.currentNotebook=null;
      },
      // Logs out user
      logOutUser(){
        this.$store.state.loggedUser = null;
        this.$router.push('/login');
      },
      // Export notebook to PDF
      exportPDF(){
        /*
        let dct = {notebook_name: this.$route.params.notebook_name}
        window.location.href = "http://localhost:5000/export_pdf/"+JSON.stringify(dct)
        */
        window.print()
      }
    }
  }


</script>

<style>

  /* Default font of entire app */
  #notebook-app{
    font-family: 'Raleway', sans-serif;
  }

  /* Border of header */
  .header{
    border-bottom: 1px solid rgb(222, 224, 229);
  }


  /* START - STYLING FOR SIDEBAR */

  .sidebar {
    margin: 0;
    padding: 0;
    width: 55px;
    background-color: #f1f1f1;
    position: fixed;
    height: 100%;
    overflow: auto;
    border: 1px solid rgb(222, 224, 229);

  }

  /* Sidebar links */
  .sidebar a {
    display: block;
    color: black;
    padding: 16px;
    text-decoration: none;
  }

  /* Active/current link */

  /* Links on mouse-over */
  .sidebar a:hover:not(.active) {
    background-color: #555;
    color: white;
  }

  /* Page content. The value of the margin-left property should match the value of the sidebar's width property */
  div.content {
    margin-left: 55px;
    padding: 1px 16px;
    height: 1000px;
  }

  /* On screens that are less than 700px wide, make the sidebar into a topbar */
  @media screen and (max-width: 700px) {
    .sidebar {
      width: 100%;
      height: auto;
      position: relative;
    }
    .sidebar a {float: left;}
    div.content {margin-left: 0;}
  }

  /* On screens that are less than 400px, display the bar vertically, instead of horizontally */
  @media screen and (max-width: 400px) {
    .sidebar a {
      text-align: center;
      float: none;
    }
  }

  /* END - STYLING FOR SIDEBAR */

</style>
