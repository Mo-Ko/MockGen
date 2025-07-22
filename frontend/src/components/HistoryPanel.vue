<template>
  <div class="bg-gray-800 rounded-lg p-4 mt-4">
    <h2 class="text-lg font-semibold text-gray-200 mb-3">Recent Generations</h2>
    <ol
      v-if="historyData && historyData.length"
      class="list-decimal list-inside space-y-2"
    >
      <li
        v-for="(item, idx) in historyData"
        :key="idx"
        class="text-gray-100 flex flex-col md:flex-row md:items-center md:gap-2"
      >
        <span class="font-mono bg-gray-700 px-2 py-1 rounded text-sm">{{
          item.api_type?.toUpperCase() || "API"
        }}</span>
        <span class="text-gray-400 text-xs">{{
          formatTimestamp(item.timestamp)
        }}</span>
      </li>
    </ol>
    <div v-else class="text-gray-400 text-sm">No recent generations.</div>
  </div>
</template>

<script setup>
const props = defineProps({
  historyData: Array,
});

function formatTimestamp(ts) {
  if (!ts) return "";
  const d = new Date(ts);
  return d.toLocaleString();
}
</script>
