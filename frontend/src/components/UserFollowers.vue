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
        <v-card-text style="height: 400px;">
          <v-list-item-group v-model="followers" color="primary">
            <v-list-item v-for="(follower, i) in followers" :key="i">
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
            </v-list-item>
          </v-list-item-group>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn color="blue darken-1" text @click="dialog = false"
            >Close</v-btn
          >
          <v-btn color="blue darken-1" text @click="dialog = false">Save</v-btn>
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
      dialog: false
    };
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
