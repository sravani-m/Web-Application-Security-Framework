<template>
  <div id="train-model">
    <br>
    <br>
    <b-container  class="rounded text-center" >

      <b-card bg-variant="light">
          <b-form-group horizontal
                        breakpoint="lg"
                        :label="model"
                        label-size="lg"
                        label-class="font-weight-bold pt-0 text-dark"
                        class="mb-0">
            <div v-for="(item,index) in form_structure">

            <b-form-group horizontal
                          :label="item.item_label"
                          label-class="text-sm-right"
                          label-for="index">
              <component :is="item.item_type" :type="item.data_type" v-model="form_data[item.data_el]" id="index"  :options="item.opts" class="mb-3" />

            </b-form-group>

            </div>
            <b-button variant="primary" @click="send_parameters">Train Model</b-button>
            <br><br><br>

          </b-form-group>

          <img :src="accuracy_history_curve">
          <img :src="loss_history_curve">
          
      </b-card>
    </b-container>

  </div>
</template>

<script>
    
  import sklearnJSON from './sklearn_structured.json'

  export default {
    mounted() {
      feather.replace()
      this.loadNotebook()
    },
    computed: {
    nnModelOpt () {
      return this.$store.state.nonNeuralModelSelected
    }
  },
  // Watching change of non-neural/neural network model type from Build Model page
  // And accordingly parses JSON and displays the hyperparameters
  watch: {
    nnModelOpt:{
    immediate: true, 
    deep:true,
    handler (newVal, oldVal) {

    console.log("check",newVal);
    this.modelTypeJson = null;

    // For non-neural network models
    if(newVal != 'neural'){   
        let i;
        for(var key in this.sklearnJSON)
        {
          i=0
          for(var key2 in this.sklearnJSON[key])
          {
            i++
            if(key2==newVal){
              this.module = key;
              this.class = key2;
              console.log("key1",key,"key2",key2)
              let obj = {[key2]:this.sklearnJSON[key][newVal]}
              console.log("Object in watch: ",obj)
              this.modelTypeJson = JSON.stringify(obj)
              console.log("obj af stringy",JSON.stringify(obj),typeof(JSON.stringify(obj)))
            }
          }
        }
        this.parse_json()
        this.modelType = "NNN"
      }
      //For neural network model
      else{
        
        // To change form details, must change modelTypeJson and must be of this structure
        this.modelTypeJson = '{"Neural Network":{"loss":"mse","learning_rate":0.001,"momentum":0.9,"nesterov":"True", "epochs":10}}' 
        this.parse_json()
        this.modelType = "NN"
      }

      }
    }
    },
    data: function () {
      return {
        model: null,
        module: '',
        class:'',
        // Comes from Build Model component
        modelTypeJson: null,
        // Stores the UI structure of form
        form_structure : [],
        // Stores hyperparameter details
        form_data : {},
        form: null,
        accuracy_history_curve: null,
        loss_history_curve: null,
        sklearnJSON
      }
    },
    methods: {
      // Called on body load
      // Checks if notebook exists and populates UI if notebook exists
      loadNotebook(){
              
              this.$http.post('http://localhost:5000/load_existing_notebook',JSON.stringify({notebook_name:this.$route.params.notebook_name}), { headers: {  'Content-Type': 'application/json' } }).then((response) => {

              console.log("Load notebook data",response.data);
              
              let notebook_data = response.data["notebook_data"]
              
              if('hyperparameters' in notebook_data)
              {
                this.form_structure = []
                this.form_data = {} 
                if(notebook_data['model_type']=="NON NEURAL NETWORK")
                {
                console.log("model hyperparameters",notebook_data["hyperparameters"])

                let hyperparameters = notebook_data["hyperparameters"]
                this.module = hyperparameters["module"]
                this.class = hyperparameters["class"]

                console.log("class is:",this.class)
                console.log("module is:",this.module)
                let obj = {[this.class]:hyperparameters["hyperparameters"]}
                console.log("hyperparameters 2 ",obj)
                this.modelTypeJson = JSON.stringify(obj)
                this.parse_json()
              }
              else
              {
                console.log("neural network hyperparameters",notebook_data["hyperparameters"])
                let obj = {"Neural Network":notebook_data["hyperparameters"]}
                this.modelTypeJson = JSON.stringify(obj)
                this.parse_json()
              }
            }
          })
      },
      // Parsing modelTypeJson to dynamically create the train model form
      // Based on the value of the hyperparameters creates the form UI elements
      parse_json: function() {
       
        this.form_structure = [];
        this.form_data = {};
        console.log("To check",this.modelTypeJson,typeof(this.modelTypeJson));
        let form = JSON.parse(this.modelTypeJson);
        console.log("Parsed json",form)

        let model_name;
        for (let m_name in form) {
          model_name = m_name;
        }

        console.log("model name",model_name,form[model_name])
        this.model = model_name;
        let labels = []
        let default_values = []

        for(var key in form[model_name]){
            labels.push(key)
            default_values.push(form[model_name][key])
        }
        
        console.log("labels",labels,default_values)

        for(let i=0;i<default_values.length;i++)
        {
          if(default_values[i]==null)
            this.form_data[labels[i]]='None';
          else
            this.form_data[labels[i]]=default_values[i];
          console.log(typeof(default_values[i]));
          if(typeof(default_values[i])=='number')
          {
            this.form_structure.push({
              item_label:labels[i],
              item_type: 'b-input',
              opts: null,
              def_val: default_values[i],
              data_type: 'number',
              data_el: labels[i]
            });

            console.log("form structure is:",this.form_data);
          }
          else if((typeof (default_values[i]) == 'boolean')||default_values[i]=="True"||default_values[i]=="False")
          {
            this.form_structure.push({
              item_label:labels[i],
              item_type: 'b-select',
              opts: [
                {value:'True',text:'True'},
                {value:'False',text:'False'}
              ],
              def_val: default_values[i],
              data_type: null,
              data_el: labels[i]

            });
          }
          else if(typeof(default_values[i])=='string')
          {
            this.form_structure.push({
              item_label:labels[i],
              item_type: 'b-input',
              opts: null,
              def_val: default_values[i],
              data_type: 'text',
              data_el: labels[i]

            });
          }
          else if(typeof(default_values[i])=='object')
          {
            this.form_structure.push({
              item_label:labels[i],
              item_type: 'b-input',
              opts: null,
              def_val: default_values[i],
              data_type: 'text',
              data_el: labels[i]

            });
          }


        }
        console.log(this.form_structure,this.form_data);
      },
      // Sends model hyperparameters to backend
      send_parameters: function(){
        
        let model_parameters_obj = {

          module: this.module,
          class: this.class,
          hyperparameters: this.form_data
        }

        let final_obj = {
          notebook_name: this.$route.params.notebook_name,
          model_parameters : model_parameters_obj
        }

        // Set train test data
        let obj = {test_size:0.3,notebook_name: this.$route.params.notebook_name}

        this.$http.post('http://localhost:5000/set_train_test_data',JSON.stringify(obj), { headers: { 'Content-Type': 'application/json' } }).then((response) => { 
                console.log("set_train_test_data",response.data);
              })

        //Build non-neural model
        if (this.modelType == "NNN")
        {
        this.$http.post('http://localhost:5000/create_non_neural_network_model',JSON.stringify(final_obj), { headers: { 'Content-Type': 'application/json' } }).then((response) => { 
                console.log("create_non_neural_network_model",response.data);

                if(response.data["message"]=="Success")
                {
                  alert("Model trained!")
                }
          })
        }
        else
        {
          let final_obj = {
            notebook_name: this.$route.params.notebook_name,
            hyperparameters : this.form_data
          }
          console.log(final_obj)
          this.$http.post('http://localhost:5000/compile_sequential_model',JSON.stringify(final_obj), { headers: { 'Content-Type': 'application/json' } }).then((response) => { 
                console.log("compile_neural_network_model",response.data);

                if(response.data["message"]=="Success"){
           			alert("Model has been compiled and trained")
                }

              
              })

          // Fetches epoch details
          let notebook_name = {notebook_name: this.$route.params.notebook_name}
          let eventSource = new EventSource("http://localhost:5000/get_epoch_details/"+JSON.stringify(notebook_name))
          
          eventSource.addEventListener('EPOCH_END', event => {
          	console.log("RECEIVED EVENT EPOCH_END")
          	this.accuracy_history_curve = "/src/assets/" + "NOTEBOOK_" + this.$route.params.notebook_name + "_accuracy_history_curve.jpg" + "?" + Math.random()
          	this.loss_history_curve = "/src/assets/" + "NOTEBOOK_" + this.$route.params.notebook_name + "_loss_history_curve.jpg" + "?" +  Math.random()
          })
          
        }         
      }
    },
    beforeMount(){
      this.parse_json();
    }

  }
</script>

<style>


</style>
