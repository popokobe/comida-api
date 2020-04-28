export default function({ store, $axios }) {
  $axios.onRequest(config => {
    config.headers["Token"] = store.$auth.getToken("local");
  });
}
