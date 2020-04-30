<template>
  <v-container class="user_profile">
    <v-container>
      <v-row>
        <v-col cols="4">
          <v-row justify="center">
            <v-avatar size="150px">
              <v-img :src="user.profile_pic" />
            </v-avatar>
          </v-row>
        </v-col>
        <v-col cols="8">
          <h1>{{ user.username }}</h1>
          <v-row>
            <v-col cols="4">
              <p>
                <span class="title font-weight-black mr-1">{{
                  user.number_of_posts
                }}</span
                >posts
              </p>
            </v-col>
            <v-col cols="4">
              <UserFollowers :followers="followers" />
            </v-col>
            <v-col cols="4">
              <UserFollowing :followings="followings" />
            </v-col>
          </v-row>
          <p class="body-1">{{ user.bio }}</p>
        </v-col>
      </v-row>
    </v-container>
    <v-divider></v-divider>
    <h2 class="text-center">Your Posts</h2>
    <v-row>
      <v-col cols="12">
        <v-card flat tile>
          <v-container fluid>
            <v-row>
              <v-col
                v-for="n in 9"
                :key="n"
                class="d-flex child-flex"
                cols="12"
                sm="6"
                md="4"
                lg="3"
              >
                <v-card flat tile class="d-flex">
                  <v-img
                    :src="`https://picsum.photos/500/300?image=${n * 5 + 10}`"
                    :lazy-src="`https://picsum.photos/10/6?image=${n * 5 + 10}`"
                    aspect-ratio="1"
                    class="grey lighten-2"
                  >
                    <template v-slot:placeholder>
                      <v-row
                        class="fill-height ma-0"
                        align="center"
                        justify="center"
                      >
                        <v-progress-circular
                          indeterminate
                          color="grey lighten-5"
                        ></v-progress-circular>
                      </v-row>
                    </template>
                  </v-img>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import UserFollowers from "@/components/UserFollowers";
import UserFollowing from "@/components/UserFollowing";

import { mapGetters } from "vuex";

export default {
  components: {
    UserFollowers,
    UserFollowing
  },
  async asyncData({ store, params }) {
    const username = params.username;
    await store.dispatch("user/getUserInfo", username);
    await store.dispatch("user/getUserFollowers", username);
    await store.dispatch("user/getUserFollowing", username);
  },
  computed: {
    ...mapGetters("user", {
      users: "getUsersInfo",
      followers: "getUserFollowers",
      followings: "getUserFollowing"
    }),
    user() {
      const username = this.$route.params.username;
      const user = this.users.find(user => {
        return user.username === username;
      });
      return user;
    }
  }
};
</script>
