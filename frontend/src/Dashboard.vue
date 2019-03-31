<template>

    <div id="dashboard">
      <!-- The top header -->
      <b-container fluid class="rounded bg-primary">
        <br>
        <b-row class="header ">
          <b-col class="text-white h5"><img :src="imgSRC" width=40px height=40px></img>Web App Vulnerability <span class="font-weight-bold">Scanner</span></b-col>
          <b-col cols="7" class="text-center h4 font-weight-bold text-white" id="notebook_name"> DASHBOARD</b-col>
          <b-col class="text-right">
            <b-button variant="primary" class="glyphicon glyphicon-pencil text-right text-white" >  Welcome {{this.$store.state.loggedUser}} <i data-feather="user"></i></b-button>
            <b-button variant="primary" @click="logOutUser">  Logout <i data-feather="log-out"></i></b-button>

          </b-col>
        </b-row>
      </b-container>

      <!-- Right sidebar_dashboard -->
      <div class="sidebar_dashboard  bg-light text-center">
        <br>
        <br>
        <br>
        <div class="text-dark">
          Reports
        </div>

        <br>
        <br>
        <br>
        <div v-for="notebook in userNotebooks" class="notebookInfo">
            <a @click="openSavedNotebook(notebook.notebook_name)">{{notebook.notebook_name}}  </a>
        </div>

      </div>

<!-- Body of page -->
  <br>
  <br>
  <br>
    <b-container class="rounded text-center light-bg" style="margin-left:450px">

      <b-card bg-variant="light">
        <b-form-group horizontal
                      breakpoint="lg"
                      label="Report name"
                      label-size="lg"
                      label-class="font-weight-bold pt-0 text-dark"
                      class="mb-0">

          <b-form-group horizontal
                        label=""
                        label-class="text-sm-right"
                        label-for="enterNotebookBook">
            <b-form-input id="enterNotebookBook" v-model="notebookInfo.notebook_name"></b-form-input>
          </b-form-group>
        </b-form-group>
        <br>
        <br>
        <br>
        <b-form-group horizontal
                      breakpoint="lg"
                      label="Select CPUs"
                      label-size="lg"
                      label-class="font-weight-bold pt-0 text-dark"
                      class="mb-0">

        <b-form-group horizontal
                      label=""
                      label-class="text-sm-right"
                      label-for="selectCPUS">
          <b-form-input type="range" id="selectCPUS" min='0' v-bind:max='maxCPUs' v-model="notebookInfo.CPU_count"></b-form-input>
        </b-form-group>
      </b-form-group>
      selected: {{notebookInfo.CPU_count}} available: {{this.maxCPUs}}
      <br>
      <br>
      <br>
<br>
<br>
<br>
    <b-button variant="primary" @click="createNotebookHandler()">Create Report</b-button>

      </b-card>
  </b-container>
    </div>

</template>

<script>
export default {
  mounted() {
    feather.replace()
  },
  beforeMount(){
    // Invoked before page loads
    this.getDevices()
    this.getNotebooks()
  },
    data: function(){
      return {
        imgSRC : require("./assets/company-logo.png"),
        minCPUs: 1,
        maxCPUs: 1,
        minGPUs: 0,
        maxGPUs: 0,
        userNotebooks: [
          ],
        notebookInfo :{
          username: this.$store.state.loggedUser,
          notebook_name: '',
          GPU_count: 0,
          CPU_count: 1
        }
      }
    },
    methods: {
      // Creates new notebook
      createNotebookHandler(){

        this.$http.get('http://localhost:5000/check_notebook_name_exists/'+JSON.stringify(this.notebookInfo)).then((response) => {
            
            console.log("Check notebook name exists",response.data);

            if(response.data.comment=="Notebook name exists"){
              alert("notebook name exists!")
            }
            else {
              this.$http.post('http://localhost:5000/add_notebook',JSON.stringify(this.notebookInfo), { headers: { 'Content-Type': 'application/json' } }).then((response) => {
                
                console.log("notebook added",response.data)
                this.userNotebooks = []
                this.getNotebooks()
                
                // To open in another tab
                // Redirects to '/notebook/<notebook-name>' and invokes Notebook.vue
                console.log("notebook name",this.notebookInfo.notebook_name)

                this.$store.state.currentNotebook = this.notebookInfo.notebook_name

                let route = this.$router.resolve({path: '/notebook/'+this.notebookInfo.notebook_name+'/'});
                window.open(route.href, '_blank');
                
                this.notebookInfo["notebook_name"] = ''
                this.notebookInfo["GPU_count"] = 0
                this.notebookInfo["CPU_count"] = 0
                
              })
            }
        })

      },
      // Opens saved notebooks
      openSavedNotebook(notebook_name){
        console.log("Open saved Notebook: "+notebook_name)
        let route = this.$router.resolve({path: '/notebook/'+notebook_name+'/'});
        window.open(route.href, '_blank');
      },
      // Logouts user
      logOutUser(){
        // Redirects to login page on logout
        this.$store.state.loggedUser = null;
        this.$router.push('/login');
      },
      // Gets number of CPUs and GPUs from computer
      getDevices(){
        this.$http.get('http://localhost:5000/get_devices').then((response) => {
          
          console.log("Exisitng devices:",response.data);

          this.maxCPUs = 1;
          this.maxGPUs = response.data.GPU_available;

        })
      },
      // Gets exisiting notebooks for the particular user 
      getNotebooks(){
        let usernameObj = {username:this.$store.state.loggedUser}
        console.log("get notebook",usernameObj)

        this.$http.get('http://localhost:5000/get_user_notebooks/'+JSON.stringify(usernameObj)).then((response) => {

          for(var i=0;i<response.data["notebook_names"].length;i++)
          {
            this.userNotebooks.push({notebook_name: response.data["notebook_names"][i]})
          }
        })

      },
    }
}


</script>

<style>

#dashboard{
  font-family: 'Raleway', sans-serif;
}

.notebookInfo{

}
/* Border of header */
.header{
  border-bottom: 1px solid rgb(222, 224, 229);
}


/* START - STYLING FOR sidebar_dashboard */

.sidebar_dashboard {
  margin: 0;
  padding: 0;
  width: 300px;
  background-color: #f1f1f1;
  position: fixed;
  height: 100%;
  overflow: auto;
  border: 1px solid rgb(222, 224, 229);

}

/* sidebar_dashboard links */
.sidebar_dashboard a {
  display: block;
  color: black;
  padding: 16px;
  text-decoration: none;
}

/* Active/current link */
.sidebar_dashboard a.active {
  background-color: #4CAF50;
  color: white;
}

/* Links on mouse-over */
.sidebar_dashboard a:hover:not(.active) {
  background-color: #555;
  color: white;
}

/* Page content. The value of the margin-left property should match the value of the sidebar_dashboards width property */
div.content {
  margin-left: 300px;
  padding: 1px 16px;
  height: 1000px;
}

/* On screens that are less than 700px wide, make the sidebar_dashboard into a topbar */
@media screen and (max-width: 700px) {
  .sidebar_dashboard {
    width: 100%;
    height: auto;
    position: relative;
  }
  .sidebar_dashboard a {float: left;}
  div.content {margin-left: 0;}
}

/* On screens that are less than 400px, display the bar vertically, instead of horizontally */
@media screen and (max-width: 400px) {
  .sidebar_dashboard a {
    text-align: center;
    float: none;
  }
}

</style>
