<template>
  <v-app-bar
    :clipped-left="$vuetify.breakpoint.lgAndUp"
    app
    color="blue darken-3"
    dark
  >
    <v-app-bar-nav-icon @click="$store.commit('showDrawer')" />
    <v-toolbar-title style="width: 300px" class="ml-0 pl-4">
      <v-btn to="/" text>comida</v-btn>
    </v-toolbar-title>
    <v-text-field
      flat
      solo-inverted
      hide-details
      prepend-inner-icon="mdi-magnify"
      label="検索"
      class="hidden-sm-and-down"
    />
    <v-spacer />
    <div v-if="$auth.loggedIn">
      <v-btn :to="$auth.user.username" text>
        <v-icon>mdi-account</v-icon>マイページ
      </v-btn>
      <v-btn text @click="$auth.logout()">
        <v-icon>mdi-logout</v-icon>
        ログアウト
        {{ $auth.user.username }}
      </v-btn>
    </div>
    <div v-else>
      <v-btn to="/login" text> <v-icon>mdi-account</v-icon>ログイン </v-btn>
      <v-btn to="/register" text>
        <v-icon>mdi-account-circle</v-icon>登録
      </v-btn>
    </div>
  </v-app-bar>
</template>

<script>
export default {};
</script>
