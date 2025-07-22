<template>
  <div
    class="min-h-screen bg-gray-900 flex flex-col items-center justify-start py-10 px-4"
  >
    <h1 class="text-3xl md:text-4xl font-bold text-white mb-8 text-center">
      AI Mock API Generator
    </h1>
    <HealthStatus class="fixed bottom-5 right-5 z-50" />
    <div class="w-full max-w-2xl bg-gray-800 rounded-lg shadow-lg p-6 mb-8">
      <ApiForm :isLoading="api.isLoading" @generate="api.handleGenerate" />
      <ErrorAlert
        v-if="api.error"
        :error="api.error"
        @dismiss="api.error = null"
        class="mt-6"
      />
      <ResultsDisplay v-if="api.resultData" :resultData="api.resultData" />
    </div>
    <div class="w-full max-w-2xl">
      <HistoryPanel
        :historyData="api.historyData"
        @refetch="api.fetchHistory"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useApiStore } from "./stores/apiStore";
import ApiForm from "./components/ApiForm.vue";
import ResultsDisplay from "./components/ResultsDisplay.vue";
import HealthStatus from "./components/HealthStatus.vue";
import HistoryPanel from "./components/HistoryPanel.vue";
import ErrorAlert from "./components/ErrorAlert.vue";

const api = useApiStore();

onMounted(() => {
  api.fetchHistory();
});
</script>
