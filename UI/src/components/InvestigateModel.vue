<template>
  <div id="investigate-model">
    <b-container class="text-center">
    <b-button variant="primary" @click="investigate_model">Investigate Model</b-button>
    </b-container>
    <br>
    <br>
    <b-container  class="rounded text-center" >
      <img :src="original_image">
      <img :src="constructed_image">
      <b-embed type="iframe" id="explanation_embed" aspect="16by9" allowfullscreen :src="explanation_embed"></b-embed>
    </b-container>

  </div>
</template>
<script>
export default {
  mounted() {
    feather.replace()
    this.loadNotebook()
  },
  data: function() {
      return {
        original_image: null,
        constructed_image: null,
        explanation_embed: null
      }
  },
  methods: {
      // Called on body load
      // Checks if notebook exists and populates UI if notebook exists
     loadNotebook(){

          console.log("Loading notebook!")
              
          this.$http.post('http://localhost:5000/load_existing_notebook',JSON.stringify({notebook_name:this.$route.params.notebook_name}), { headers: {  'Content-Type': 'application/json' } }).then((response) => {

          console.log("Loads exisitng notebook",response.data)
          
          let notebook_data = response.data["notebook_data"]
          if('explanation' in notebook_data)
          {
            console.log("Loading explanation")
            this.explanation_embed = "/src/assets/" + notebook_data['explanation']

          }

              
        })
      },
    // Loads investigate model image 
    investigate_model: function() {
      let final_obj = {
          notebook_name: this.$route.params.notebook_name,
        }
      this.$http.get('http://localhost:5000/investigate_model/' + JSON.stringify(final_obj)).then((response) => {
        console.log(response.data)
        this.explanation_embed = "/src/assets/" + response.data['explanation']
      })
    }
  }
}
</script>

<style>
.explanation_embed
{
  position: relative;
  width: 500%;
  height: 500%;
}

</style>
