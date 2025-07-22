<template>
  <div v-if="resultData" class="mt-6 pt-6 border-t border-gray-600 space-y-4">
    <div>
      <h3 class="text-xl font-semibold mb-2 text-gray-300">Live Endpoints</h3>
      <ul>
        <li v-for="endpoint in resultData.endpoints" :key="endpoint" class="font-mono bg-gray-700 p-2 rounded text-sm break-all">
          <a :href="endpoint" target="_blank" class="text-cyan-400 hover:underline">{{ endpoint }}</a>
        </li>
      </ul>
    </div>
    <div>
      <h3 class="text-xl font-semibold mb-2 text-gray-300">API Documentation</h3>
      <div class="flex space-x-2">
        <a :href="`${backendBaseUrl}/docs`" target="_blank" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded text-sm">Swagger Docs</a>
        <a :href="`${backendBaseUrl}/redoc`" target="_blank" class="bg-pink-500 hover:bg-pink-600 text-white font-bold py-2 px-4 rounded text-sm">ReDoc</a>
      </div>
    </div>
    <div>
      <h3 class="text-xl font-semibold mb-2 text-gray-300">Generated Schema</h3>
      <pre class="bg-gray-900 text-gray-300 text-xs p-3 rounded overflow-x-auto max-h-80"><code>{{ JSON.stringify(resultData.api_schema, null, 2) }}</code></pre>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  resultData: Object
});

const backendBaseUrl = computed(() => {
  if (props.resultData?.mock_url) {
    try {
      const url = new URL(props.resultData.mock_url);
      return `${url.protocol}//${url.host}`;
    } catch (e) {
      console.error("Invalid mock_url received:", props.resultData.mock_url);
      return '';
    }
  }
  return '';
});
</script>