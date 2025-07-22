<template>
  <div
    class="px-3 py-1 rounded-full text-white text-sm"
    :class="isHealthy ? 'bg-green-600' : 'bg-red-600'"
  >
    {{ isHealthy ? "Backend Healthy" : "Backend Down" }}
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { checkHealth as checkHealthApi } from "../services/api";

const isHealthy = ref(false);

const checkHealth = async () => {
  try {
    const data = await checkHealthApi();
    isHealthy.value = data?.status === "ok";
  } catch (error) {
    isHealthy.value = false;
  }
};

onMounted(() => {
  checkHealth();
  setInterval(checkHealth, 30000); // Check every 30 seconds
});
</script>
