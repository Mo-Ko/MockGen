import { defineStore } from 'pinia';
import { ref } from 'vue';
import { generateApi, getHistory } from '../services/api';

export const useApiStore = defineStore('api', () => {
  // State
  const isLoading = ref(false);
  const error = ref('');
  const resultData = ref(null);
  const historyData = ref([]);
  const submittedApiType = ref('');

  // Actions
  async function handleGenerate(formData) {
    isLoading.value = true;
    error.value = '';
    resultData.value = null;
    submittedApiType.value = formData.api_type;
    try {
      resultData.value = await generateApi(formData);
      await fetchHistory();
    } catch (err) {
      error.value = err?.response?.data?.detail || err.message || 'Unknown error';
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchHistory() {
    try {
      historyData.value = await getHistory();
    } catch (err) {
      // Optionally handle error
    }
  }

  return {
    isLoading,
    error,
    resultData,
    historyData,
    submittedApiType,
    handleGenerate,
    fetchHistory,
  };
}); 