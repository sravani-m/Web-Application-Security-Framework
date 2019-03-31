import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export const store = new Vuex.Store({

  state : {
      loggedUser : null,
      nonNeuralModelSelected: "LinearSVC",
      currentNotebook: null,
      report: "No report available.",
      },
 
  mutations : {

    updateNonNeuralModelSelected (state,value){
      state.nonNeuralModelSelected = value;
      console.log("selected value",state.nonNeuralModelSelected);
      
    },

    updateReport (state,value){
    	state.report = value;
    }
  },
  getters : {
    getNonNeuralModelSelected(state)
    {
      return state.nonNeuralModelSelected;
    },
    getReport(state)
    {
    	return state.report;
    }
  }
});
