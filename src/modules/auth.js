
const auth_store = {
  state: {
    profile: null,
  },
  mutations: {
    set_profile(state,profile){
      state.profile=profile;
    }
  }
}

export default auth_store
