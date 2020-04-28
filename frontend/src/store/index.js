export const state = () => ({
  drawer: false
});

export const getters = {};

export const mutations = {
  showDrawer(state) {
    state.drawer = !state.drawer;
  }
};

export const actions = {
  showDrawer(context) {
    context.commit("showDrawer");
  }
};
