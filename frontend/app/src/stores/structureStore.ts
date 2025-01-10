import { defineStore } from 'pinia';
import { ref, watch } from 'vue';
import type { Structure } from '@/api/types/structure';

export const useStructureStore = defineStore('structureStore', () => {
  const structures = ref<Structure[]>(getInitialStructures());

  // Watch for changes in the structures ref and update localStorage
  watch(structures, updateLocalStorage, { deep: true });
  // Listen for storage events to update the structures ref
  window.addEventListener('storage', handleStorageEvent);

  return { structures };

  function getInitialStructures(): Structure[] {
    return JSON.parse(localStorage.getItem('structures') || '[]');
  }

  function updateLocalStorage(newStructures: Structure[]) {
    localStorage.setItem('structures', JSON.stringify(newStructures));
  }

  function handleStorageEvent(event: StorageEvent) {
    if (event.key === 'structures') {
      structures.value = JSON.parse(event.newValue || '[]');
    }
  }
});
