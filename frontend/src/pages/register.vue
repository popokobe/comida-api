<template>
  <v-container>
    <h1>Register</h1>
    <UserAuthForm button-text="登録" :submit-form="register" has-email="true" />
  </v-container>
</template>

<script>
import UserAuthForm from "@/components/UserAuthForm";

export default {
  auth: false,
  components: {
    UserAuthForm
  },
  methods: {
    async register(registrationInfo) {
      try {
        await this.$axios.post("user/register/", registrationInfo);

        await this.$auth.loginWith("local", {
          data: registrationInfo
        });
        this.$store.dispatch("snackbar/create", {
          text: "登録ありがとうございます"
        });
        this.$router.push("/");
      } catch (error) {
        this.$store.dispatch("snackbar/create", {
          text: "登録内容に不備があります。もう一度お試しください。",
          color: "red"
        });
      }
    }
  }
};
</script>
