<template>
<div>
  <div style="overflow-x: hidden; overflow-y: hidden">

    <b-row >

      <b-col cols="3">

    <b-container class="left_sidebar text-center bg-white text-dark">
      <br>
      <!-- Selects model type: neural-network OR non-neural model  -->
      <label class="font-weight-bold text-dark">SELECT MODEL TYPE:</label>
      <br>
      <br>
      <b-row>

        <b-col></b-col>
        <b-col cols="9">
          <b-form-select :options="leftSidebarOptions" v-model="leftSidebarModelSelected"></b-form-select>
        </b-col>
        <b-col></b-col>
      </b-row>
        
      <br>
      <br>

      <!-- Displays neural network layers on the left hand side -->
      <div  class=" text-dark" v-if="leftSidebarModelSelected=='neural'">

          <b-card v-b-toggle.inputOutputLayer_options class="bg-light font-weight-bold text-primary">
            INPUT/OUTPUT LAYERS &nbsp;
          </b-card>

        <b-collapse id="inputOutputLayer_options">
          <div v-for="layer in inputOutputLayers"  class="bg-light text-center font-weight-bold text-dark leftSidebarOptions">
            <drag class="drag" :transfer-data="{'type': layer.layer_name}">{{layer.layer_name}}</drag>
          </div>
        </b-collapse>


          <b-card v-b-toggle.core_layer_options class="bg-light font-weight-bold text-primary">
            CORE LAYERS &nbsp;
          </b-card>

          <b-collapse id="core_layer_options">
            <div v-for="layer in coreLayers"  class="bg-light text-center font-weight-bold text-dark leftSidebarOptions">
            <drag class="drag" :transfer-data="{'type': layer.layer_name}">{{layer.layer_name}}</drag>    
             </div>
          </b-collapse>

        <b-card v-b-toggle.convolution_layer_options class="bg-light font-weight-bold text-primary">
          CONVOLUTION LAYERS &nbsp;
        </b-card>

        <b-collapse id="convolution_layer_options">
          <div v-for="layer in convLayers"  class="bg-light text-center font-weight-bold text-dark leftSidebarOptions">
          <drag class="drag" :transfer-data="{'type': layer.layer_name}">{{layer.layer_name}}</drag>
        </div>

        </b-collapse>

        <b-card v-b-toggle.pooling_layer_options class="bg-light font-weight-bold text-primary">
          POOLING LAYERS &nbsp;
        </b-card>

        <b-collapse id="pooling_layer_options">
          <div v-for="layer in poolingLayers"  class="bg-light text-center font-weight-bold text-dark leftSidebarOptions">
          <drag class="drag" :transfer-data="{'type': layer.layer_name}">{{layer.layer_name}}</drag>
        </div>

        </b-collapse>

        <b-card v-b-toggle.recurrent_layer_options class="bg-light font-weight-bold text-primary">
          RECURRENT LAYERS &nbsp;
        </b-card>

        <b-collapse id="recurrent_layer_options">
          <div v-for="layer in recurrentLayers"  class="bg-light text-center font-weight-bold text-dark leftSidebarOptions">
          <drag class="drag" :transfer-data="{'type': layer.layer_name}">{{layer.layer_name}}</drag>
        
        </div>

        </b-collapse>
        <b-card v-b-toggle.normalisation_layer_options class="bg-light font-weight-bold text-primary">
          NORMALIZATION LAYERS &nbsp;
        </b-card>

        <b-collapse id="normalisation_layer_options">
          <div v-for="layer in normalisationLayers"  class="bg-light text-center font-weight-bold text-dark leftSidebarOptions">
          <drag class="drag" :transfer-data="{'type': layer.layer_name}">{{layer.layer_name}}</drag>
        </div>

        </b-collapse>

        <b-card v-b-toggle.other_layer_options class="bg-light font-weight-bold text-primary">
          OTHER LAYERS &nbsp;
        </b-card>

        <b-collapse id="other_layer_options">
          <div v-for="layer in otherLayers"  class="bg-light text-center font-weight-bold text-dark leftSidebarOptions">
          <drag class="drag" :transfer-data="{'type': layer.layer_name}">{{layer.layer_name}}</drag>
        </div>
        </b-collapse>

      </div>

    </b-container>

      </b-col>

      <!--Drop area of the neural network model -->
      <b-col cols="7">
        <b-container class="text-center" v-if="leftSidebarModelSelected=='neural'">
          <b-button @click="sendModelToBackend()" variant="primary"> SAVE MODEL </b-button>
        </b-container>
        <br>
        <b-container class="rounded text-center build_model_body" v-if="leftSidebarModelSelected=='neural'">

          <!--Drop area-->
          <drop class="drop" :class="{over}" @dragover="over=true" @dragleave="over=false" @drop="addLayer">

            <!--Input layer is fixed-->
          <b-card class="dropArea bg-light" style="overflow-y: auto; overflow-x: hidden;">
               
            <div v-for="(item,index) in modelLayers">
                <b-button variant="outline-primary" style="border-radius: 25px; background-color: rgb(236,249,255); margin-bottom: 10px; margin-top:10px; "
                          class="font-weight-bold text-primary" @click="updatedSelectedLayer(item.layer_id)">
                  <p><span class="inputOutputLayer"> {{item.layer_id}} : {{item.layerType}} </span> <span v-if="index!=0" @click="deleteLayer(item.layerType,item.layer_id)" class="deleteLayerOption"> x </span></p>
                </b-button>

            </div>

          </b-card>

          </drop>

        </b-container>

        <!-- Displays non-neural network model options -->
        <b-container class="rounded text-center build_model_body" v-if="leftSidebarModelSelected=='non-neural'">
          <b-card class="dropArea bg-light" style="overflow-y: auto; overflow-x: hidden;">

            <div class=" text-dark" v-if="leftSidebarModelSelected=='non-neural'">
              <br>
              <label class="font-weight-bold text-dark">SELECT MODEL:</label>
              <br>
              <br>
              <b-row>
                <b-col></b-col>
                  <b-col cols="9">
                    <b-form-select size="5" :options="nonNeuralModelOptions" v-model="nonNeuralModelSelected" :select-size="20"></b-form-select>
                  </b-col>
                <b-col></b-col>
              </b-row>
            </div>
          </b-card>
        </b-container>
      </b-col>

    <!--Right side bar (contains information about each layer)-->

      <b-col cols="2">

        <b-card bg-variant="light" class="dropArea" style="overflow-y: auto; overflow-x: hidden;" v-if="leftSidebarModelSelected=='neural'">


        <div v-for="(modelLayer,index) in modelLayers">


          <div v-if="rightSidebarSelectedLayer==modelLayer.layer_id">

            {{modelLayer.layerName}}
            <br>
            <div v-for="(options,index) in modelLayer.defaultOptions">

              <div class="text-dark font-weight-bold" style="font-size: 14px">
                <br>
              {{options.name}}
                <component :is="options.componentType" :type="options.dataType" id="options.layerName"  :options="options.selectOpts" v-model="options.defaultValue" mb-3/>

              </div>

            </div>

          </div>

        </div>

        </b-card>

        <!-- Sidebar for non-neural network model - empty -->
        <b-card bg-variant="light" class="dropArea" style="overflow-y: auto; overflow-x: hidden;" v-if="leftSidebarModelSelected=='non-neural'">
        </b-card>

      </b-col>
    </b-row>

  </div>

</div>
</template>
<script>

  import sklearn_json from './sklearn_structured.json'
  import keras_json from './keras_structured.json'

  export default {
    // On body load
    mounted() {
      feather.replace()
      this.populateBuildModel()
      this.populateLayers()
      this.loadNotebook()
    },
    // Used to access nonNeuralModelSelected variable in Vuex store
    computed:{
      nonNeuralModelSelected:{
        get(){
          return this.$store.state.nonNeuralModelSelected;
        },
        set(value){
          this.$store.commit('updateNonNeuralModelSelected',value);
        }
      }
    },
    // Putting a watch to see if model selected is neural/non-neural network model
    watch : {

        leftSidebarModelSelected : {
          immediate: true, 
          deep:true,
          handler(val){
          if(val=='neural'){
            this.nonNeuralModelSelected = 'neural'
            console.log("Build model watch:",this.$store.state.nonNeuralModelSelected);
          }
        }
      }
    },
    data: function () {
      return {
        over:false,
        // Check if model selected is neural network or non-neural 
        leftSidebarModelSelected:'neural',
        leftSidebarOptions: [
          {value: null,text:'Select model type',disabled:true},
          {value: 'neural',text:'Neural network'},
          {value: 'non-neural',text:'Non-neural network'}
        ],
        // Contains all neural network models after parsing sklearn.json
        nonNeuralModelOptions: [
          {value: null,text:'Select model',disabled:true},         
        ],
        // Keeps track of number of layers which acts as layer ID
        layers:1,
        // Displays hyperparameters of currently selected neural network layer in the right side bar.
        rightSidebarSelectedLayer:'',
        inputOutputLayers : [],
        coreLayers : [],
        convLayers: [],
        poolingLayers: [],
        recurrentLayers: [],
        normalisationLayers:[],
        otherLayers:[],
        modelLayers: [
        ],
        keras_json,
        sklearn_json,
      }
    },
    methods: {
      // Called on body load
      // Checks if notebook exists and populates UI if notebook exists
      loadNotebook(){

          console.log("Loading notebook!")

          // Call to get existing notebook details

          this.$http.post('http://localhost:5000/load_existing_notebook',JSON.stringify({notebook_name:this.$route.params.notebook_name}), { headers: {  'Content-Type': 'application/json' } }).then((response) => {
            
            console.log("loadNotebook",response.data);
            
            let notebook_data = response.data["notebook_data"]

            // If model_type is present in notebook details, load the notebook details

            if('model_type' in notebook_data)
            {  
              console.log("Loading exisitng model")  
              console.log("Model type",notebook_data["model_type"])

              // Loading details for neural network model
              if(notebook_data["model_type"]=="NEURAL NETWORK")
              {
                  this.leftSidebarModelSelected = 'neural'
                  this.modelLayers = notebook_data["modelLayers"]
                  this.layers = notebook_data["numLayers"]
              }
              else
              {
                  this.leftSidebarModelSelected = 'non-neural'
                  console.log(notebook_data["model_name"])
                  this.nonNeuralModelSelected = notebook_data["hyperparameters"]["class"]
              }
            }
          })
      },
      // Called on body load
      // Parses sklearn_json for non-neural network models and populates nonNeuralModelOptions
      populateBuildModel(){

        for (var moduleKey in this.sklearn_json)
        {
          for (var classKey in this.sklearn_json[moduleKey])
          {
            this.nonNeuralModelOptions.push({value:classKey, text:classKey})
          }
        }
      },
      // Called on body load
      // Parses kerasJSON and populates left sidebar with keras layers
      populateLayers(){

          this.modelLayers = []

          // Fixing input layer
          let def_ip = []
          for(let key in keras_json['Input'])
          {
             def_ip.push({name:key,defaultValue:keras_json['Input'][key],selectOpts:null})
          }

          this.modelLayers.push({
            layer_id: 0,
            layerType: 'Input',
            outputDim : null,
            defaultOptions : this.createDefaultOptsDynamic(def_ip),
          })

          console.log("Populating layers")
          
          // Populating left sidebar layers based on keras_json
          // And segregating into core layers,conv layers

          for(let layerName in keras_json){
            if(layerName.toLowerCase().includes("input")||layerName.toLowerCase().includes("output"))
            {
                this.inputOutputLayers.push({layer_name:layerName});
            }
            else if(layerName.toLowerCase().includes("dense")||layerName.toLowerCase().includes("dropout")||layerName.toLowerCase().includes("flatten"))
            {
                this.coreLayers.push({layer_name:layerName});
            }
            else if(layerName.toLowerCase().includes("conv")||layerName.toLowerCase().includes("convolution"))
            {
                this.convLayers.push({layer_name:layerName});
            }
            else if(layerName.toLowerCase().includes("pool"))
            {
                this.poolingLayers.push({layer_name:layerName});
            }
            else if(layerName.toLowerCase().includes("rnn")||layerName.toLowerCase().includes("lstm"))
            {
                this.recurrentLayers.push({layer_name:layerName});
            }
            else if(layerName.toLowerCase().includes("normalization"))
            {
                this.normalisationLayers.push({layer_name:layerName});
            }
            else
            {
              this.otherLayers.push({layer_name:layerName});
             }
            }

        console.log("Populating layers",this.inputOutputLayers);
      },
      // Called each time a layer is dropped from the left side bar
      addLayer(data) {
        this.over = false;
        console.log(data['type']);

        // Call to get output dimension
        let defParams = []
        let opDim = null

        for(let layerName in keras_json){
          for(let params_key in keras_json[layerName]){

              if(layerName==data['type']){
              console.log(params_key,keras_json[layerName][params_key])
              defParams.push({name:params_key,defaultValue:keras_json[layerName][params_key],selectOpts:null})
            }
          }
        }

        // Creates options dynamically
        let newDefaultOpts = this.createDefaultOptsDynamic(defParams)

        this.modelLayers.push({layer_id:this.layers,layerType:data['type'],outputDim:opDim,defaultOptions:newDefaultOpts})

        this.rightSidebarSelectedLayer = this.layers;
        this.layers = this.layers+1

        console.log("Model layers",this.modelLayers);
      },
      // Creates neural network hyperparameters options dynamically (on the right sidebar)
      // Generates UI based on value of the hyperparameter
      createDefaultOptsDynamic(defaultOpts){

        for(let opt = 0; opt < defaultOpts.length; opt++) {

          if ((typeof(defaultOpts[opt].defaultValue) == 'number')&&(defaultOpts[opt].selectOpts==null))
          {
            defaultOpts[opt].componentType = 'b-input';
            defaultOpts[opt].dataType = 'number';
            defaultOpts[opt].selectOpts = null;
          }
          else if ((typeof(defaultOpts[opt].defaultValue) == 'number')&&(defaultOpts[opt].selectOpts!=null))
          {
            let opts = defaultOpts[opt].selectOpts;
            let selectedOptionsForm = []
            for(let value=0;value<opts.length;value++)
            {
              selectedOptionsForm.push({value: opts[value], text: opts[value]});
            }

            defaultOpts[opt].componentType = 'b-select';
            defaultOpts[opt].dataType = 'number';
            defaultOpts[opt].selectOpts = selectedOptionsForm;
          }
          else if(typeof(defaultOpts[opt].defaultValue) == 'boolean')
          {
            defaultOpts[opt].componentType = 'b-select';
            defaultOpts[opt].dataType = null;
            defaultOpts[opt].selectOpts = [
              {value:'true',text:'True'},
              {value:'false',text:'False'}
            ]
          }
          else if ((typeof(defaultOpts[opt].defaultValue) == 'string')&&(defaultOpts[opt].selectOpts!=null)) {
            defaultOpts[opt].componentType = 'b-select';
            defaultOpts[opt].dataType = null;
            let opts = defaultOpts[opt].selectOpts;
            let selectedOptionsForm = []
            for(let value=0;value<opts.length;value++)
            {
              selectedOptionsForm.push({value: opts[value], text: opts[value]});
            }
            defaultOpts[opt].selectOpts = selectedOptionsForm;
          }
          else if ((typeof(defaultOpts[opt].defaultValue) == 'string')&&(defaultOpts[opt].selectOpts==null)) {
            defaultOpts[opt].componentType = 'b-input';
            defaultOpts[opt].dataType = 'text';
            defaultOpts[opt].selectOpts = null;
          }
          else if ((typeof(defaultOpts[opt].defaultValue) == 'object')&&(defaultOpts[opt].selectOpts==null)) {
            defaultOpts[opt].componentType = 'b-input';
            defaultOpts[opt].dataType = 'text';
            defaultOpts[opt].selectOpts = null;
          }

          console.log("Options",defaultOpts[opt].selectOpts);

        }

        return defaultOpts;
      },
      // Deletes layer based on layer ID
      deleteLayer(layerType,layer_id){

        for(let i=0;i<this.modelLayers.length;i++)
        {
            if(this.modelLayers[i]['id']==layer_id)
              this.modelLayers.splice(i,1)
        }
          
        console.log("After delete, model layers:",this.modelLayers)
        
        this.rightSidebarSelectedLayer = '';
        this.modelLayers.splice(layer_id, 1);
        
        console.log("deleting layer id",layer_id)

        },
      // Updates hyperparameters on right sidebar based on layerID
      updatedSelectedLayer(layer_id){
        this.rightSidebarSelectedLayer = layer_id;
      },
      // Sends model to backend
      sendModelToBackend(){
        console.log(JSON.stringify(this.modelLayers))
        this.toSend = {notebook_name: this.$route.params.notebook_name, layers: this.modelLayers,numLayers:this.layers}
        this.$http.post('http://localhost:5000/create_sequential_model', JSON.stringify(this.toSend), { headers: { 'Content-Type': 'application/json' } }).then((response) => {
          
          console.log("Create sequential model",response)
        })

      }

    }

  }

</script>

<style>

  .inputOutputLayer{
    margin: 10px;
    padding-top: 10px;
    padding-bottom: 10px;
    padding-right: 70px;
    padding-left: 70px;
  }

  .deleteLayerOption{
    color: crimson;
  }

  .deleteLayerOption:hover{
    color: brown;

  }

  .drop.over{
    background: #ccc;
  }

  .dropArea{
    height: 650px;

  }

  .leftSidebarOptions{
  margin: 7px;
  padding: 5px;
  border: 1px solid rgb(222, 224, 229);
  }
  /* Default font of entire app */
  #build-model{
    font-family: 'Raleway', sans-serif;
  }

  /* Border of header */
  .header{
    border-bottom: 1px solid rgb(222, 224, 229);
  }


  /* START - STYLING FOR SIDEBAR */

  .left_sidebar {
    margin-top: 40px;
    margin-left: 55px;
    padding: 0;
    width: 260px;
    background-color: #f1f1f1;
    position: fixed;
    height: 70%;
    overflow-x: hidden;
    overflow-y: auto;
    border: 1px solid rgb(222, 224, 229);

  }

  /* Sidebar links */
  .left_sidebar a {
    display: block;
    color: black;
    padding: 10px;
    text-decoration: none;
  }

  /* Active/current link */
  .left_sidebar a.active {
    background-color: #4CAF50;
    color: white;
  }

  /* Links on mouse-over */
  .left_sidebar a:hover:not(.active) {
    background-color: #555;
    color: white;
  }

   /*Page content. The value of the margin-left property should match the value of the sidebar width property*/
  .build_model_body{
    /*margin-left: 340px;*/
    padding: 1px 16px;
    height: 650px;
    margin-right: 200px;
  }

  /* On screens that are less than 700px wide, make the sidebar into a topbar */
  @media screen and (max-width: 700px) {
    .left_sidebar {
      width: 100%;
      height: auto;
      position: relative;
      margin-left: 0px;
    }
    .left_sidebar a {float: left;}
    div.content {margin-left: 0;}

    .build_model_body{
      position: relative;
      margin: 0px;
    }

  }

  /* On screens that are less than 400px, display the bar vertically, instead of horizontally */
  @media screen and (max-width: 400px) {
    .left_sidebar a {
      text-align: center;
      float: none;
    }

    .left_sidebar{
      position: relative;
      margin-left: 0px;

    }

    .build_model_body{
      position: relative;
      margin: 0px;
    }

  }

  /* END - STYLING FOR SIDEBAR */

</style>
