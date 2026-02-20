<template>
  <div id="root">
    <LandingPage v-if="view === 'landing'" @try="view = 'analyzer'" />
    <AnalyzerView v-else @back="view = 'landing'" />
  </div>
</template>

<script>
import LandingPage from "./components/LandingPage.vue";
import AnalyzerView from "./components/AnalyzerView.vue";

export default {
  components: { LandingPage, AnalyzerView },
  data() {
    return { view: 'landing' };
  }
};
</script>

<style>
#root {
  min-height: 100vh;
  background: var(--bg-primary);
}
</style>
