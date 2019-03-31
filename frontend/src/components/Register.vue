<template>

 <div id="registerUser">
    <b-container class="registerUser">
    <b-row>
    	<b-col> </b-col>

    	<b-col cols="7" class="bg-light">
	    <br>
	    <h2>Register</h2>
	    <br>
	    <form @submit.prevent="handleSubmit" id="reg_usr_form" name="reg_usr_form">
	        <div class="form-group">
	            <label for="firstName">First Name</label>
	            <input type="text" v-model="registerUser.firstName" v-validate="'required'" name="firstName" class="form-control" :class="{ 'is-invalid': registerSumbitted && errors.has('firstName') }" />
	            
	            <div v-if="registerUser.registerSumbitted && errors.has('firstName')" class="invalid-feedback">{{ errors.first('firstName') }}
	            </div>
	        </div>
	        
	        <div class="form-group">
	            <label for="lastName">Last Name</label>
	            <input type="text" v-model="registerUser.lastName" v-validate="'required'" name="lastName" class="form-control" :class="{ 'is-invalid': registerSumbitted && errors.has('lastName') }" />
	            <div v-if="registerUser.registerSumbitted && errors.has('lastName')" class="invalid-feedback">{{ errors.first('lastName') }}
	            </div>
	            
	        </div>
	            
	        <div class="form-group">
	            <label for="username">Username</label>
	            <input type="text" v-model="registerUser.username" v-validate="'required'" name="username" class="form-control" :class="{ 'is-invalid': registerSumbitted && errors.has('username') }" />
	            <div v-if="registerUser.registerSumbitted && errors.has('username')" class="invalid-feedback">{{ errors.first('username') }}
	        	</div>
	        </div>
	        
	        <div class="form-group">
	            <label htmlFor="password">Password</label>
	            <input type="password" v-model="registerUser.password" v-validate="{ required: true, min: 6 }" name="password" class="form-control" :class="{ 'is-invalid': registerSumbitted && errors.has('password') }" />
	            <div v-if="registerUser.registerSumbitted && errors.has('password')" class="invalid-feedback">{{ errors.first('password') }}</div>
	        </div>
	        <br>    
	        <div class="form-group">
	            <button class="btn btn-primary" @click="registerUserHandler()">Register</button>
	            <button class="btn btn-white" @click="goToLoginPage()" >Cancel</button>
	        </div>
	        
	    </form>
	    </br>
	  	</br>
	  </b-col>

	  <b-col></b-col>
	 </b-row>
  </b-container>
</div>
</template>

<script type="text/javascript">
	
	export default{

		mounted() 
		{
      		feather.replace()
    	},

    	data: function(){
    	return {
    		registerSumbitted: false,
    		registerUser: {
                firstName: '',
                lastName: '',
                username: '',
                password: '',

            	}
    		}
    	
    	},

    	methods: {
    		// Handles register user
			registerUserHandler()
			{
				console.log("Register user");
	          	console.log(this.registerUser);

	          	// Checks if username exists
	      		this.$http.get('http://localhost:5000/check_username_exists/'+JSON.stringify(this.registerUser)).then((response) => 
	      		{
	        	console.log("Check username exists:",response.data);

	        	if(response.data.comment =='Username available')
	        	{
	        		// Adds username
	          		this.$http.post('http://localhost:5000/add_user',JSON.stringify(this.registerUser), { headers: { 'Content-Type': 'application/json' } }).then((response) => 
	          			{
	            			console.log("adduser",response.data);
	            		 	alert("Username added!");
	            		 	this.$router.push('/login');
	          			})
	        	}
	        	else 
	        	{
	          		alert("Username already exists!");
	          		console.log("User exists");
	        	}})
		},
		// Redirects to login page
		goToLoginPage()
		{
			this.$router.push('/login')
		}    		
	}

}

</script>


<style>

.registerUser{
  margin-top: 200px;
  font-family: 'Raleway', sans-serif;
}
</style>
