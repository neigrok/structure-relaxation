<script lang="ts" setup>
  import type { Structure } from '@/api/types/structure';

  defineProps<{
    structure: Structure;
  }>();
</script>

<template>
  <RouterLink
    class="grid gap-y-0 gap-x-4 grid-cols-[min-content_auto_min-content] grid-rows-[min-content_min-content] p-1 m-1 border border-gray-300 hover:bg-gray-100"
    :to="{ name: 'structure', params: { structureId: structure.id } }"
  >
    <div></div>
    <div class="font-semibold">{{ structure.structures.chemical_formula }}</div>
    <div class="text-sm text-gray-500 col-start-2 row-start-2">{{ structure.status }}</div>
  </RouterLink>
</template>

<style scoped></style>
