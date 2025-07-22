<template>
  <div
    v-if="error"
    class="flex items-center justify-between bg-red-900 border border-red-700 text-red-200 px-4 py-3 rounded-md mb-4"
  >
    <div class="flex-1"><strong>Error:</strong> {{ error }}</div>
    <button
      @click="$emit('dismiss')"
      class="ml-4 text-red-300 hover:text-white text-lg font-bold focus:outline-none"
      title="Dismiss"
    >
      &times;
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  error: {
    type: String,
    default: "",
  },
});
</script>
