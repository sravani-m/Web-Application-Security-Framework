<template>
  <div id="uploadData">
    <br>
    <br>
    <b-container  class="rounded text-center" >
      <b-card bg-variant="light">
        <br>
        <br>
        <b-form-group horizontal
                      breakpoint="lg"
                      label="Choose Vulnerabilities"
                      label-size="lg"
                      label-class="font-weight-bold pt-0"
                      class="mb-0">

          <b-form-group horizontal
                        label="Enter URL:"
                        label-class="text-sm-right"
                        label-for="urlForScan">
            <b-form-input id="urlForScan" v-model="inputUrl" class="mb-3" />

          </b-form-group>

          <br>
          <br>

          <b-form-group horizontal
                        label="Choose URL Check type:"
                        label-class="text-sm-right"
                        label-for="testingType">
            <b-form-select  id="testingType" v-model="testingType" :options="testingTypeOptions" class="mb-3" />
          </b-form-group>

          <br/>
          <br/>

        <div v-if="testingType=='URL_TEST'">

            <b-form-group horizontal
                        label="Choose service:"
                        label-class="text-sm-right"
                        label-for="toolOptions">



              <b-form-checkbox-group id="toolOptions" name="toolOptions" v-model="vulnerabilitiesSelected">
                  <b-form-checkbox value="gsb">Google Safe Browsing </b-form-checkbox><br/><br/>
                  <b-form-checkbox value="netcraft">Netcraft</b-form-checkbox><br/><br/>


              </b-form-checkbox-group>

          </b-form-group>


        </div>


        <div v-if="testingType=='INFO_GATHER'">

          <b-form-group horizontal
                        label="Choose information to gather:"
                        label-class="text-sm-right"
                        label-for="toolOptions">



              <b-form-checkbox-group id="toolOptions" name="toolOptions" v-model="vulnerabilitiesSelected">
                  <b-form-checkbox value="ssl">SSL Information</b-form-checkbox><br/><br/>
                  <b-form-checkbox value="server-info">Server Information</b-form-checkbox><br/><br/>
                  <b-form-checkbox value="allowed-methods">Server Allowed Methods</b-form-checkbox><br/><br/>
              </b-form-checkbox-group>

          </b-form-group>

        </div>


        <div v-if="testingType=='VULNERABILITY_ANALYSE'">

          <b-form-group horizontal
                        label="Choose vulnerabilities to scan for:"
                        label-class="text-sm-right"
                        label-for="toolOptions">



              <b-form-checkbox-group id="toolOptions" name="toolOptions" v-model="vulnerabilitiesSelected">
                  <b-form-checkbox value="nikto">Server side vulnerabilities</b-form-checkbox><br/><br/>
                  <b-form-checkbox value="backdoor-info">Finding backdoors</b-form-checkbox><br/><br/>
                  <b-form-checkbox value="form-security">Form security check</b-form-checkbox><br/><br/>
                  <b-form-checkbox value="clickjacking">Clickjacking</b-form-checkbox><br/><br/>
                  <b-form-checkbox value="cookies">Cookies</b-form-checkbox><br/><br/>
                  <b-form-checkbox value="xss">XSS Check</b-form-checkbox><br/><br/>

              </b-form-checkbox-group>

          </b-form-group>

        </div>



        <div v-if="testingType=='FULL_SCAN'">

          <b-form-group horizontal
                        label="Choose scan type:"
                        label-class="text-sm-right"
                        label-for="toolOptions">



              <b-form-checkbox-group id="toolOptions" name="toolOptions" v-model="vulnerabilitiesSelected">
               
                  <b-form-checkbox value="genscan">General (Rapid Scan)</b-form-checkbox><br/><br/>


              </b-form-checkbox-group>

          </b-form-group>

        </div>


        </b-form-group>

          <br>
          <br/>
          <b-button @click="startWebsiteScan"> START SCAN </b-button>
          <br>
          <br>
        <br>

      </b-card>
    </b-container>

    <br>
    <br>

  </div>
</template>

<script>


  export default{

    mounted() {
     // feather.replace();
      this.loadNotebook()
    },
    data: function()
    {
      return {
      // stores file name   
      testingType: null,
      testingTypeOptions: [
        {value: null, text: 'Choose type',disabled:true},
        {value: 'URL_TEST', text: 'URL Check'},
        {value: 'INFO_GATHER', text: 'Information Gathering'},
        {value: 'VULNERABILITY_ANALYSE', text: 'Vulnerability Scans'},
        {value: 'FULL_SCAN', text: 'Full scans'},
        ],
      loadNotebookStatus: false,
      inputUrl: "",
      vulnerabilitiesSelected: [],
      username: this.$store.state.loggedUser,
      }
      
    },
    methods: {
      // Called on body load
      // Checks if notebook exists and populates UI if notebook exists
      loadNotebook(){
            
          this.$http.get('http://localhost:5000/load_existing_notebook/'+JSON.stringify({notebook_name:this.$route.params.notebook_name})).then((response) => {
            
          console.log("Loading notebook",typeof(response.data))

          let notebook_data = response.data['notebook_data']
          
          console.log(notebook_data)
          
          if('url' in notebook_data)
           {
            console.log("Loading notebook!")

            this.inputUrl = notebook_data['url']
            this.vulnerabilitiesSelected = notebook_data['vulnerabilities']
            this.$store.state.report = notebook_data['report']
           }
           
      })

      },
      startWebsiteScan(){
          console.log(this.inputUrl)
          console.log("Starting website scan",this.vulnerabilitiesSelected)
          let req_json = {"vulnerabilities":this.vulnerabilitiesSelected,"url":this.inputUrl,"notebook_name":this.$route.params.notebook_name, "username": this.username };

          console.log(req_json)


          this.$http.get('http://localhost:5000/get_scan_results/'+JSON.stringify(req_json)).then((response) => {
          
          console.log("response",response.data['report'],typeof(response.data['report']));
          this.$store.state.report = response.data['report'];
          this.$router.push("/notebook/"+this.$route.params.notebook_name+"/results");
          console.log("response");
            
         
        })


      }

    }

  }

</script>

<style>


</style>
