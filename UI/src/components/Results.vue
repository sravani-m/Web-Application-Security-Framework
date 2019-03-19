<template>
  <div id="results">
    <br>
    <br>
    <b-container  class="rounded text-center" >
      <!-- Gets results on button click -->
      <b-button @click="getResults()" > Get results </b-button>
      <br>
      <br>
      <b-card bg-variant="light">
        <b-form-group horizontal
                      breakpoint="lg"
                      label="Results"
                      label-size="lg"
                      label-class="font-weight-bold pt-0 text-dark"
                      class="mb-0">
          <!-- Prints accuracy -->
          <b-form-group horizontal
                        label="ACCURACY"
                        label-class="text-sm-right font-weight-bold text-dark"
                        label-for="accuracy">
            <label id="accuracy"> {{accuracy}} %</label>
          </b-form-group>
          <br>
          <!-- Prints true positive -->
          <b-form-group horizontal
                        label="TRUE POSITIVE"
                        label-class="text-sm-right font-weight-bold text-dark"
                        label-for="true-positive">
            <label id="true-positive"> {{true_positive}} </label>
          </b-form-group>
          <br>
          <!-- Prints true negative -->
          <b-form-group horizontal
                        label="TRUE NEGATIVE"
                        label-class="text-sm-right font-weight-bold text-dark"
                        label-for="true-negative">
            <label id="true-negative"> {{true_negative}} </label>
          </b-form-group>
          <br>
          <!-- Prints false positive -->
          <b-form-group horizontal
                        label="FALSE POSITIVE"
                        label-class="text-sm-right font-weight-bold text-dark"
                        label-for="false-positive">
            <label id="false-positive"> {{false_positive}} </label>
          </b-form-group>
          <br>
          <!-- Prints false negative -->
          <b-form-group horizontal
                        label="FALSE NEGATIVE"
                        label-class="text-sm-right font-weight-bold text-dark"
                        label-for="false-negative">
            <label id="false-negative"> {{false_negative}} </label>
          </b-form-group>
          <br>
          <!-- Prints recall -->
          <b-form-group horizontal
                        label="RECALL"
                        label-class="text-sm-right font-weight-bold text-dark"
                        label-for="recall">
            <label id="recall"> {{recall}} </label>
          </b-form-group>
          <br>
          <!-- Prints precision -->
          <b-form-group horizontal
                        label="PRECISION"
                        label-class="text-sm-right font-weight-bold text-dark"
                        label-for="precision">
            <label id="precision"> {{precision}} </label>
          </b-form-group>
          <br>
    
        </b-form-group>
      </b-card>
      <br>
      <br>

      <img id="precision_recall_curve" :src="precision_recall_curve">
      <img id="roc_curve" :src="roc_curve">

    </b-container>

  </div>
</template>
<script>
  export default {
    data : function(){

      return {
        accuracy : 0,
        true_positive: 0,
        true_negative: 0,
        false_positive: 0,
        false_negative: 0,
        recall: 0,
        precision: 0,
        precision_recall_curve: null,
        roc_curve: null
      }
    },
    mounted() {
      feather.replace()
      this.loadNotebook()
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
      // Call to get results
      getResults:function(){

        let obj = {notebook_name:this.$route.params.notebook_name}

        // Accuracy
         this.$http.get('http://localhost:5000/get_accuracy/'+JSON.stringify(obj)).then((response) => {
            console.log("get accuracy",response.data);
            this.accuracy = Math.ceil(response.data["accuracy"]*100)
        }
      )
         // Gets confusion matrix
         this.$http.get('http://localhost:5000/get_confusion_matrix/'+JSON.stringify(obj)).then((response) => {
            console.log("get confusion matrix", response.data)

            this.true_negative = response.data['confusion_matrix'][0]
            this.false_positive = response.data['confusion_matrix'][1]
            this.false_negative = response.data['confusion_matrix'][2]
            this.true_positive = response.data['confusion_matrix'][3]
         })

         // Gets precision recall curve
         this.$http.get('http://localhost:5000/get_precision_recall_curve/'+JSON.stringify(obj)).then((response) => {
            console.log("get precision recall curve matrix", response.data)

            this.precision = response.data['average_precision_score']
            this.recall = response.data['recall']
            this.precision_recall_curve = "/src/assets/" + response.data['precision_recall_curve']
         })

         // Gets ROC curve
         this.$http.get('http://localhost:5000/get_roc_curve/'+JSON.stringify(obj)).then((response) => {
            console.log("get precision recall curve matrix", response.data)

            this.roc_curve = "/src/assets/" + response.data['roc_curve']
          
         })
     }
  }
}
</script>

<style>


</style>
