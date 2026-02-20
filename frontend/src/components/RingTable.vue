<template>
  <div class="table-wrapper">
    <h2>Fraud Ring Summary</h2>

    <table v-if="rings && rings.length">
      <thead>
        <tr>
          <th>Ring ID</th>
          <th>Pattern Type</th>
          <th>Member Count</th>
          <th>Risk Score</th>
          <th>Members</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="ring in rings" :key="ring.ring_id">
          <td>{{ ring.ring_id }}</td>
          <td>{{ ring.pattern_type }}</td>
          <td>{{ ring.member_accounts.length }}</td>
          <td>{{ ring.risk_score }}</td>
          <td>{{ ring.member_accounts.join(', ') }}</td>
        </tr>
      </tbody>
    </table>

    <p v-else>No fraud rings detected.</p>
  </div>
</template>

<script>
export default {
  props: ["rings"]
};
</script>
