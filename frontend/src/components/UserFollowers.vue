<template>
  <v-row>
    <v-dialog v-model="dialog" scrollable max-width="400px">
      <template v-slot:activator="{ on }">
        <v-btn text v-on="on">
          <span class="title font-weight-black mr-1">{{
            user.number_of_followers
          }}</span
          >Followers
        </v-btn>
      </template>
      <v-card>
        <v-card-title>Followers</v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-0" style="height: 400px;">
          <v-list-item-group v-model="duplicatedFollowers" color="primary">
            <v-list-item v-for="(follower, i) in duplicatedFollowers" :key="i">
              <v-list-item-icon>
                <v-avatar>
                  <img :src="follower.profile_pic" :alt="follower.username" />
                </v-avatar>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title
                  v-text="follower.username"
                ></v-list-item-title>
              </v-list-item-content>
              <v-btn
                @click.stop="unfollowUser(follower)"
                v-if="follower.followed_by_req_user"
                depressed
                small
                >Following</v-btn
              >
              <v-btn
                @click.stop="followUser(follower)"
                v-else
                depressed
                small
                color="primary"
                >Follow</v-btn
              >
            </v-list-item>
          </v-list-item-group>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn color="blue darken-1" text @click="dialog = false"
            >Close</v-btn
          >
          <v-btn
            :loading="loading"
            :disabled="loading"
            @click="loader = 'loading'"
            >テスト</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  props: {
    followers: {
      type: Array
    }
  },
  data() {
    return {
      dialog: false,
      loader: null,
      loading: false,
      duplicatedFollowers: this.followers
    };
  },
  methods: {
    followUser(follower) {
      const to_user = follower.username;
      this.$store.dispatch("user/followUser", to_user);
    },
    unfollowUser(follower) {
      const to_user = follower.username;
      this.$store.dispatch("user/followUser", to_user);
    }
  },
  computed: {
    ...mapGetters("user", {
      users: "getUsersInfo"
    }),
    user() {
      const username = this.$route.params.username;
      const user = this.users.find(user => {
        return user.username === username;
      });
      return user;
    }
  },
  watch: {
    loader() {
      const l = this.loader;
      this[l] = !this[l];

      setTimeout(() => (this[l] = false), 1000);

      this.loader = null;
    }
  }
};
</script>
