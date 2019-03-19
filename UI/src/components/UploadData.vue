<template>
  <div id="uploadData">
    <br>
    <br>
    <b-container  class="rounded text-center" >
      <b-card bg-variant="light">
      <!--   <div v-if="uploadedFileType=='csv'">
        <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/> Uploaded file:   {{this.uploadedFile}}
        </div> -->
        <br>
        <br>
        <b-form-group horizontal
                      breakpoint="lg"
                      label="Choose Vulnerabilities"
                      label-size="lg"
                      label-class="font-weight-bold pt-0"
                      class="mb-0">
          <b-form-group horizontal
                        label="Upload own dataset/existing:"
                        label-class="text-sm-right"
                        label-for="nestedDataType">
            <b-form-select  id="nestedDataType" v-model="uploadedFileType" :options="UploadedFileOptions" class="mb-3" />
          </b-form-group>
        </b-form-group>

        <!--Rendering content for pre-defined datasets-->
        <div v-if="uploadedFileType=='pre-defined'">
       
       <b-form-group horizontal
                        breakpoint="lg"
                        label=""
                        label-size="lg"
                        label-class="font-weight-bold pt-0"
                        class="mb-0">

           <b-form-group horizontal
                          label="Select options:"
                          label-class="text-sm-right"
                          label-for="pre-proc-options">
              <b-form-select :options="preDefinedOptions" id="pre-def-options" v-model="predefinedSelected" :select-size="1"></b-form-select>
            </b-form-group>
            
          </b-form-group>

          </b-form-group>
          <br>
          <br>
          <b-button type="primary" @click='handlePreDefined()'> Choose Dataset</b-button>

        </div>
        <br>
        <div v-if="uploadedFileType=='csv'">
          <b-form-group horizontal
                        breakpoint="lg"
                        label=""
                        label-size="lg"
                        label-class="font-weight-bold pt-0"
                        class="mb-0">

             <b-form-group horizontal
                          label="Does dataset contain columns?"
                          label-class="text-sm-right"
                          label-for="contains-cols">
      
               <b-form-radio-group v-model="containsColumnsSelected"
                          :options="containsColumnsOptions"
                          name="radioInline">
              </b-form-radio-group>

            </b-form-group>


            <b-form-group horizontal
                          label="Select options:"
                          label-class="text-sm-right"
                          label-for="pre-proc-options">
              <b-form-select :options="preprocessingOptions" id="pre-proc-options" v-model="preprocessingSelected" :select-size="4"></b-form-select>
            </b-form-group>
            
          </b-form-group>

        <br>
        <br>
        <br>
        <b-button type="primary" @click='handlePreProcess()'> START SCAN </b-button>
      </div>
      </b-card>
    </b-container>

    <br>
    <br>

  </div>
</template>

<script>

  import sklearnStructuredJSON from './sklearn_structured.json'

  export default{

    mounted() {
     // feather.replace();
      this.parseJSONHandler()
      this.loadNotebook()
    },
    data: function()
    {
      return {
      // stores file name
      uploadedFile: '',
      uploadFileName:'null',
      uploadedFileType: 'csv',
      loadNotebookStatus: false,
      predefinedSelected: 'BOSTON_HOUSING',
      // Predefined dataset options
      preDefinedOptions: [
        {value: null, text: 'Choose dataset',disabled:true},
        {value: 'BOSTON_HOUSING', text: 'BOSTON_HOUSING'},
        {value: 'MNIST', text: 'MNIST'},
        {value: 'CIFAR10', text: 'CIFAR10'},
        {value: 'CIFAR100', text: 'CIFAR100'},
        {value: 'IRIS', text: 'IRIS'},
        {value: 'OXFORD17_FLOWERS', text: 'OXFORD17_FLOWERS'}
        ],
      preprocessingSelected:'',
      preprocessingOptions:[
      {value: null, text: 'Choose pre-processing technique(s)',disabled:true},
        ],
        UploadedFileOptions: [
          {value: 'csv', text: 'CSV File(s)'},
          {value: 'pre-defined', text: 'Choose pre-defined dataset'}
        ],
      containsColumnsSelected:'',
      containsColumnsOptions:[
      {value: 'yes',text:'yes'},
      {value: 'no', text:'no'}
      ],
      sklearnStructuredJSON,
      }
      
    },
    methods: {
      // Called on body load
      // Checks if notebook exists and populates UI if notebook exists
      loadNotebook(){
            
          this.$http.post('http://localhost:5000/load_existing_notebook',JSON.stringify({notebook_name:this.$route.params.notebook_name}), { headers: {  'Content-Type': 'application/json' } }).then((response) => {
            
          console.log("Loading notebook",typeof(response.data))

          let notebook_data = response.data['notebook_data']
          console.log(notebook_data)
            if('preprocessing_applied' in notebook_data||'predefined_dataset' in notebook_data)
           {
            console.log("Loading notebook!")

            if(notebook_data['uploaded_file_type'] == 'csv')
            {
            this.uploadedFileType = 'csv'
            console.log("preprocessing existing: ",notebook_data["preprocessing_applied"])
            this.loadNotebookStatus = true
            this.preprocessingSelected = notebook_data["preprocessing_applied"]
            this.containsColumnsSelected = notebook_data["has_columns"]
            console.log("Upload file name:",notebook_data["file_name"])
            this.uploadedFile = notebook_data["file_name"]
          }
          else
          {
            console.log("Loading pre-defined dataset")
            this.uploadedFileType = 'pre-defined'
            this.predefinedSelected = notebook_data["predefined_dataset"]
           }
        }
      })

      },
      // Used to display preprocessing options after parsing through JSON
      parseJSONHandler(){

         for(var moduleKey in this.sklearnStructuredJSON['preprocessing'])
         {
          let opt = {value: moduleKey, text: moduleKey}
          this.preprocessingOptions.push(opt);
         }
      },
      // Stores file details on file upload
      handleFileUpload(){

          this.uploadFileName = this.$refs.file.files[0]
          console.log("Handling file upload:", this.uploadFileName,this.uploadFileName['name'])
          this.uploadedFile = this.uploadFileName['name']
          this.loadNotebookStatus = false
      },
      // Selects predefined dataset
      handlePreDefined(){

        this.$http.post('http://localhost:5000/upload_predefined',JSON.stringify({dataset_name:this.predefinedSelected,notebook_name:this.$route.params.notebook_name}), { headers: {  'Content-Type': 'application/json' } }).then((response) => {
            
            console.log("Setting pre-defined dataset",response.data);
            if(response.data["message"]=="Success"){
              alert("Dataset chosen!")
            }
          })
      },
      //Sends pre-processing details to the server - for CSV Files
      handlePreProcess(){      
      console.log("notebook name: ",this.$route.params.notebook_name);

      var formData = new FormData();
      formData.append('file', this.uploadFileName);
      formData.append('notebook_name',this.$route.params.notebook_name);
      formData.append('has_header', this.containsColumnsSelected)
      formData.append('file_name',this.uploadFileName['name']);
      formData.append('load_notebook_status',this.loadNotebookStatus);

      console.log("Upload table",formData);
      
      // Upload file
      if(this.uploadedFileType=='csv')
      {
        this.$http.post('http://localhost:5000/upload_table',formData, { headers: {  'Content-Type': 'multipart/form-data' } }).then((response) => {
            console.log("Upload table:",response.data);
          })
       }

      let preprocessHyperparameters;

      // Populating preprocess options after parsing sklearn JSON

      for (var moduleKey in this.sklearnStructuredJSON){
          for (var classKey in this.sklearnStructuredJSON[moduleKey]){
              if(classKey==this.preprocessingSelected)
              {
                console.log("hyperparameters",this.sklearnStructuredJSON[moduleKey][classKey]);
                preprocessHyperparameters = this.sklearnStructuredJSON[moduleKey][classKey];
              }
          }
      }

      let model_parameters = {
          module: 'preprocessing',
          class: this.preprocessingSelected,
          hyperparameters: preprocessHyperparameters
      }

      console.log("contains columns",this.containsColumnsSelected)
      
      let preprocDetails = {notebook_name:this.$route.params.notebook_name,model_parameters:model_parameters,has_columns:this.containsColumnsSelected,uploaded_file_type:'csv'}

      // Object being sent to the server is of the form:
      // {notebook_name:<name>,model_parameters:{module:'preprocessing',class:<class-key>,hyperparameters:{}}}

      console.log("preprocessing details",preprocDetails)

      this.$http.post('http://localhost:5000/preprocessing',JSON.stringify(preprocDetails), { headers: { 'Content-Type': 'application/json' } }).then((response) => {
            console.log("preprocessing",response.data);

            if(response.data["message"]=="Success"){
              alert("preprocessing applied!")
            }

          })

      }

    }

  }

</script>

<style>


</style>
