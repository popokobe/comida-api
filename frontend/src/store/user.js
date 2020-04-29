export const state = () => ({
  users: []
  // followers: [],
  // following: []
});

export const getters = {
  getUsersInfo(state) {
    return state.users;
  },
  getUserFollowers(state) {
    return state.followers;
  },
  getUserFollowing(state) {
    return state.following;
  }
};

export const mutations = {
  setUserInfo(state, user) {
    state.users.push(user);
  },
  setUserFollowers(state, followers) {
    state.followers = followers;
  },
  setUserFollowing(state, following) {
    state.following = following;
  }
};

export const actions = {
  async getUserInfo(context, username) {
    const endpoint = `/user/${username}/`;
    const user = await this.$axios.$get(endpoint);
    context.commit("setUserInfo", user);
  },
  async getUserFollowers(context, username) {
    const endpoint = `/user/${username}/get-followers/`;
    const followers = await this.$axios.$get(endpoint);
    context.commit("setUserFollowers", followers);
  },
  async getUserFollowing(context, username) {
    const endpoint = `/user/${username}/get-following/`;
    const following = await this.$axios.$get(endpoint);
    context.commit("setUserFollowing", following);
  }
};
