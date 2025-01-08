<script lang="ts" setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import type { Structure } from '@/api/types/structure';
  import StructuresListItem from '@/modules/structure/components/StructuresListItem.vue';

  const router = useRouter();
  const structures = ref<Structure[]>(JSON.parse(localStorage.getItem('structures') || '[]'));

  function navigateToHome() {
    router.push({ name: 'structures' });
  }
</script>

<template>
  <div class="structures-list">
    <button
      class="w-full mb-4 bg-gray-800 hover:bg-gray-900 text-white font-bold py-2 px-4 rounded"
      @click="navigateToHome"
    >
      Add new structure
    </button>
    <template v-if="structures.length">
      <StructuresListItem
        v-for="structure of structures"
        :key="structure.id"
        :structure="structure"
      />
    </template>
    <div v-else class="empty">No structures found.</div>
  </div>
</template>

<style scoped>
  .structures-list {
    overflow: auto;
    padding-block: 8px;
    padding-inline: 12px;
  }

  .empty {
    text-align: center;
  }
</style>
