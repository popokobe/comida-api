<template>
  <v-row>
    <v-dialog v-model="dialog" scrollable max-width="400px">
      <template v-slot:activator="{ on }">
        <v-btn text v-on="on">
          <span class="title font-weight-black mr-1">{{
            user.number_of_following
          }}</span
          >Following
        </v-btn>
      </template>
      <v-card>
        <v-card-title>Following</v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-0" style="height: 400px;">
          <v-list-item-group v-model="duplicatedFollowings" color="primary">
            <v-list-item
              v-for="(following, i) in duplicatedFollowings"
              :key="i"
            >
              <v-list-item-icon>
                <v-avatar>
                  <img :src="following.profile_pic" :alt="following.username" />
                </v-avatar>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title
                  v-text="following.username"
                ></v-list-item-title>
              </v-list-item-content>
              <v-btn
                @click.stop="unfollowUser(following)"
                v-if="following.followed_by_req_user"
                depressed
                small
                >Following</v-btn
              >
              <v-btn
                @click.stop="followUser(following)"
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
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  props: {
    followings: {
      type: Array
    }
  },
  data() {
    return {
      dialog: false,
      duplicatedFollowings: this.followings
    };
  },
  methods: {
    followUser(following) {
      const to_user = following.username;
      this.$store.dispatch("user/followUser", to_user);
    },
    unfollowUser(following) {
      const to_user = following.username;
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
  }
};
</script>
