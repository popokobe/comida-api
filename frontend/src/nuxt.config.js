import colors from "vuetify/es5/util/colors";

module.exports = {
  /*
   ** Headers of the page
   */
  head: {
    title: "app",
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { hid: "description", name: "description", content: "Nuxt.js project" }
    ],
    link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }]
  },
  /*
   ** Customize the progress bar color
   */
  loading: { color: "#3B8070" },
  modules: ["@nuxtjs/vuetify", "@nuxtjs/axios", "@nuxtjs/auth"],
  axios: {
    baseURL: "http://127.0.0.1:8000"
  },
  // auth: {
  //   redirect: {
  //     login: "/login/", // 未ログイン時に認証ルートへアクセスした際のリダイレクトURL
  //     logout: "/login/", // ログアウト時のリダイレクトURL
  //     home: "/" // ログイン後のリダイレクトURL
  //   },
  //   strategies: {
  //     local: {
  //       endpoints: {
  //         login: { url: "/auth/login/", method: "post", propertyName: "token" },
  //         user: { url: "/auth/myinfo/", method: "get", propertyName: false }
  //       },
  //       tokenType: "jwt"
  //     }
  //   }
  // },
  // router: {
  //   middleware: ["auth"]
  // },
  /*
   ** vuetify module configuration
   ** https://github.com/nuxt-community/vuetify-module
   */
  vuetify: {
    customVariables: ["~/assets/variables.scss"],
    theme: {
      dark: false,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        }
      }
    }
  },
  /*
   ** Build configuration
   */
  build: {
    /*
     ** Run ESLint on save
     */
    extend(config, { isDev, isClient }) {
      if (isDev && isClient) {
        config.module.rules.push({
          enforce: "pre",
          test: /\.(js|vue)$/,
          loader: "eslint-loader",
          exclude: /(node_modules)/
        });
      }
    }
  },
  server: {
    host: "0.0.0.0"
  }
};
