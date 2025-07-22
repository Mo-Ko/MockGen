<template>
  <form @submit.prevent="submitForm" class="space-y-6">
    <div>
      <label for="description" class="block text-sm font-medium text-gray-300 mb-1">API Description</label>
      <textarea id="description" v-model="prompt" rows="4"
        class="w-full bg-gray-700 border border-gray-600 rounded-md p-2 text-gray-200 focus:ring-blue-500 focus:border-blue-500"></textarea>
    </div>
    <div class="grid grid-cols-2 gap-4">
      <div>
        <label for="api-type" class="block text-sm font-medium text-gray-300 mb-1">API Type</label>
        <select id="api-type" v-model="api_type" class="w-full bg-gray-700 border border-gray-600 rounded-md p-2 text-gray-200 focus:ring-blue-500">
          <option value="rest">REST</option>
          <option value="graphql">GraphQL</option>
        </select>
      </div>
      <div>
        <label for="llm-provider" class="block text-sm font-medium text-gray-300 mb-1">LLM Provider</label>
        <select id="llm-provider" v-model="llm" class="w-full bg-gray-700 border border-gray-600 rounded-md p-2 text-gray-200 focus:ring-blue-500">
          <option value="gemini">Gemini</option>
          <option value="openai">OpenAI</option>
        </select>
      </div>
    </div>
    <button type="submit" :disabled="isLoading"
      class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md transition disabled:bg-gray-500 disabled:cursor-not-allowed flex items-center justify-center">
      <svg v-if="isLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      {{ isLoading ? 'Generating...' : 'Generate API' }}
    </button>
  </form>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
  isLoading: Boolean
});

const emit = defineEmits(['generate']);

const prompt = ref('');
const api_type = ref('rest');
const llm = ref('gemini');

const submitForm = () => {
  if (!prompt.value.trim()) {
    return;
  }
  emit('generate', {
    prompt: prompt.value,
    api_type: api_type.value,
    llm: llm.value
  });
};
</script>