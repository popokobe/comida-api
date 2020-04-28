<template>
  <v-app id="comida">
    <NavigationDrawer />
    <NavigationBar />

    <v-content>
      <v-container class="fill-height" fluid>
        <nuxt />
      </v-container>
      <Footer />
    </v-content>
    <SnackBar />
  </v-app>
</template>

<script>
import NavigationDrawer from "@/components/NavigationDrawer";
import NavigationBar from "@/components/NavigationBar";
import Footer from "@/components/Footer";
import SnackBar from "@/components/SnackBar";

export default {
  components: {
    NavigationDrawer,
    NavigationBar,
    Footer,
    SnackBar
  }
};
</script>
