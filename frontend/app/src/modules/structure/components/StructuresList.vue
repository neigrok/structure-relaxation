<script lang="ts" setup>
  import { useBrowserStorageItem, GoButton } from '@constructor/ui';
  import { computed } from 'vue';
  import type { Structure } from '@/api/types/structure';
  import StructuresListItem from '@/modules/structure/components/StructuresListItem.vue';
  import { router } from '@/router/router';

  const { get } = useBrowserStorageItem<Structure[]>('structures', {
    storageArea: 'localStorage',
  });
  const structures = computed(() => get() || []);

  function navigateToHome() {
    router.push({ name: 'structures' });
  }
</script>

<template>
  <div class="structures-list">
    <GoButton class="create-button" @click="navigateToHome">Add new structure</GoButton>
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

  .create-button {
    margin-block: 8px;
    width: 100%;
  }

  .empty {
    text-align: center;
  }
</style>
