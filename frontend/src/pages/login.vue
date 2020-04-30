<template>
  <v-container>
    <h1>Login</h1>
    <UserAuthForm button-text="ログイン" :submit-form="login" />
  </v-container>
</template>

<script>
import UserAuthForm from "@/components/UserAuthForm";

export default {
  components: {
    UserAuthForm
  },
  methods: {
    async login(loginInfo) {
      try {
        await this.$auth.loginWith("local", {
          data: loginInfo
        });
        this.$store.dispatch("snackbar/create", {
          text: "ログインしました"
        });
        this.$router.push("/");
      } catch (error) {
        this.$store.dispatch("snackbar/create", {
          text: "ログインできませんでした",
          color: "red"
        });
      }
    }
  }
};
</script>
