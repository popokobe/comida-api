<template>
  <div>
    <v-snackbar
      v-for="(snackbar, index) in snackbars.filter((s) => s.showing)"
      :key="snackbar.text + Math.random()"
      :value="snackbar.showing"
      :timeout="snackbar.timeout"
      :color="snackbar.color"
      :style="`bottom: ${index * 60 + 8}px`"
      @input="removeSnackbar(snackbar)"
    >
      {{ snackbar.text }}

      <v-btn text @click="removeSnackbar(snackbar)">
        閉じる
      </v-btn>
    </v-snackbar>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState({
      snackbars: (state) => state.snackbar.snackbars
    })
  },
  methods: {
    removeSnackbar(snackbar) {
      this.$store.dispatch('snackbar/remove', snackbar)
    }
  }
}
</script>
