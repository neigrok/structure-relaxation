<script lang="ts" setup>
  import { ref } from 'vue';
  import { useCreateStructureRequest } from '@/api/structures';
  import type { StructureCreateForm, Structure } from '@/api/types/structure';

  const initialValues = ref<StructureCreateForm>({
    mp_api_key: localStorage.getItem('mp_api_key') || '',
    material_id: 'mp-',
    fmax: 0.05,
    max_steps: 20,
  });

  const values = ref<StructureCreateForm>({ ...initialValues.value });
  const { request: requestCreateStructure } = useCreateStructureRequest();

  function getStructures(): Structure[] {
    return JSON.parse(localStorage.getItem('structures') || '[]');
  }

  function setStructures(structures: Structure[]) {
    localStorage.setItem('structures', JSON.stringify(structures));
  }

  async function onSubmit() {
    const structures = getStructures();

    const response = await requestCreateStructure(values.value);
    structures.push(response);
    setStructures(structures);

    localStorage.setItem('mp_api_key', values.value.mp_api_key);
    window.location.reload();
  }
</script>

<template>
  <form @submit.prevent="onSubmit" class="space-y-4">
    <div>
      <label for="mp_api_key" class="block text-sm font-medium text-gray-700">API Key</label>
      <input
        id="mp_api_key"
        v-model="values.mp_api_key"
        required
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
      />
    </div>
    <div>
      <label for="material_id" class="block text-sm font-medium text-gray-700">Material ID</label>
      <input
        id="material_id"
        v-model="values.material_id"
        required
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
      />
    </div>
    <div>
      <label for="fmax" class="block text-sm font-medium text-gray-700">Fmax</label>
      <input
        id="fmax"
        v-model="values.fmax"
        required
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
      />
    </div>
    <div>
      <label for="max_steps" class="block text-sm font-medium text-gray-700">Max Steps</label>
      <input
        id="max_steps"
        v-model="values.max_steps"
        required
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
      />
    </div>
    <button
      type="submit"
      :disabled="!values.mp_api_key || !values.material_id || !values.fmax || !values.max_steps"
      class="w-full inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 disabled:opacity-50"
    >
      Create Structure
    </button>
  </form>
</template>

<style scoped>
input:invalid {
  border: 1px solid  red;
}
</style>
