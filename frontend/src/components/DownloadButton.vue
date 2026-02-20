<template>
  <div class="download-wrapper">
    <button @click="downloadJSON">
      Download JSON Report
    </button>
  </div>
</template>

<script>
export default {
  props: ["jsonData"],

  methods: {
    downloadJSON() {
      const blob = new Blob(
        [JSON.stringify(this.jsonData, null, 2)],
        { type: "application/json" }
      );

      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "forensics_results.json";
      a.click();

      URL.revokeObjectURL(url);
    }
  }
};
</script>
