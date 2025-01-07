<script lang="ts" setup>
  import type { Structure } from '@/api/types/structure';

  defineProps<{
    structure: Structure;
  }>();
</script>

<template>
  <RouterLink
    class="structures-item"
    :to="{ name: 'structure', params: { structureId: structure.id } }"
  >
    <div></div>
    <div class="font-weight-semi-bold">{{ structure.structures.chemical_formula }}</div>
    <div class="status">{{ structure.status }}</div>
  </RouterLink>
</template>

<style scoped>
  .structures-item {
    display: grid;
    gap: 0 16px;
    grid-template-columns: min-content auto min-content;
    grid-template-rows: min-content min-content;
    padding-block: 4px;
    padding-inline: 8px;
    margin-block: 4px;
    border: var(--go-border-primary);
  }

  .structures-item:hover {
    background-color: var(--go-color-overlay-hover);
  }

  .status {
    @mixin text-ui-11;
    color: var(--go-color-glyph-secondary);
    grid-column: 2;
    grid-row: 2;
  }
</style>
