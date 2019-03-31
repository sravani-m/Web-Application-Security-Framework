<template>
  <div id="loginUser">
    <b-container class="loginUser">
      <b-row>
        <b-col></b-col>
        <b-col cols="7">
          <b-container class="bg-light">
          <br>
          <br>
          <h2>Login</h2>
          <br>
          <form @submit.prevent="handleSubmit">
              <div class="form-group">
                  <label for="username">Username</label>
                  <input type="text" v-model="loginUser.username" name="username" class="form-control" :class="{ 'is-invalid': loginSubmitted && !username }" />
                  <div v-show="loginSubmitted && !loginUser.username" class="invalid-feedback">Username is required</div>
              </div>
              <div class="form-group">
                  <label htmlFor="password">Password</label>
                  <input type="password" v-model="loginUser.password" name="password" class="form-control" :class="{ 'is-invalid': loginSubmitted && !password }" />
                  <div v-show="loginSubmitted && !loginUser.password" class="invalid-feedback">Password is required</div>
              </div>

              <br>
              <div class="form-group">
                  <button class="btn btn-primary" @click="loginUserHandler()">Login</button>
                  <button class="btn btn-white" @click="goToRegisterPage()" >Register</button>
              </div>
          </form>
          <br>
          <br>
      </b-container>
    </b-col>
    <b-col> </b-col>
  </b-row>
  </b-container>
</div>

</template>


<script>
  export default {

    mounted() {
      feather.replace()
    },

    data: function(){
      return {
        loginSubmitted:false,
        loginUser:{
          username: '',
          password: ''
        },
        message: null,
      }
    },
    methods: {
      handleSubmit : function(){
        console.log("Handling!");
      },
      // Handles login user
      loginUserHandler: function(){
 
          this.$http.post('http://localhost:5000/check_username_and_password_matches',JSON.stringify(this.loginUser), { headers: { 'Content-Type': 'application/json' } }).then((response) => {
          console.log("here",response)
          if(response.data.comment=="Username and password match"){

                // Setting the currently logged in user in the Vuex store
                this.$store.state.loggedUser = this.loginUser.username;
                
                console.log("Logged in username",this.$store.state.loggedUser);
                console.log("Redirecting to dashboard");
                
                // Redirects to dashboard page
                this.$router.push('/dashboard');
              }
            else{
              alert("Username and password don't match!");
            }
          })
      },
      // Redirects to register page
      goToRegisterPage: function(){

        this.$router.push('/register');
      }
    }
  }



</script>

<style>

.loginUser{
  font-family: 'Raleway', sans-serif;
  margin-top: 200px;
}
</style>
