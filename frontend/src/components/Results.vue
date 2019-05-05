<template>
  <div id="results">
    <br>
    <br>
    <b-container  class="rounded text-center whitespace" >
      <!-- Gets results on button click -->
      <br>
      <br>
      <b-card bg-variant="light">
        <b-form-group horizontal
                      breakpoint="lg"
                      label="Scan Results"
                      label-size="lg"
                      label-class="font-weight-bold pt-0 text-dark"
                      class="mb-0">
          <!-- Prints accuracy -->
          {{scanResults}}
         
          <br>
      
        </b-form-group>
      </b-card>
      <br>
      <br>


    </b-container>

  </div>
</template>
<script>
  export default {
    data : function(){

      return {
        scanResults: this.$store.state.report
      }
    },
    mounted() {
      feather.replace()
      // this.loadNotebook()
    },
    methods:{
      // Called on body load
      // Loads existing notebook 
      loadNotebook: function(){

        this.$http.post('http://localhost:5000/load_existing_notebook',JSON.stringify({notebook_name:this.$route.params.notebook_name}), { headers: {  'Content-Type': 'application/json' } }).then((response) => {

                console.log("Loading existing notebook",response.data)
                
                let notebook_data = response.data["notebook_data"]

                if('accuracy' in notebook_data)
                {
                  console.log("Results present")
                  this.accuracy = Math.ceil(notebook_data["accuracy"]*100)
                  this.true_positive = notebook_data["true_positive"]
                  this.true_negative = notebook_data["true_negative"]
                  this.false_positive = notebook_data["false_positive"]
                  this.false_negative = notebook_data["false_negative"]
                  this.recall = notebook_data["recall"]
                  this.precision = notebook_data["average_precision_score"]
                  this.precision_recall_curve = "/src/assets/" + notebook_data["precision_recall_curve"]
                  this.roc_curve = "/src/assets/" + notebook_data["roc_curve"]
                }
          }
        )
      },
  }
}
</script>

<style>
.whitespace{

  white-space:pre-wrap;
}

</style>
