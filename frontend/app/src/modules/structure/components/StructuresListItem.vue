<script lang="ts" setup>
  import type { Structure } from '@/api/types/structure';
  import { useRouteStructureId } from '@/modules/structure/services/helpers.ts';
  import { computed } from 'vue';

  const props = defineProps<{
    structure: Structure;
  }>();

  const structureId = useRouteStructureId();
  const isCurrentActive = computed(() => structureId.value === props.structure.id);
</script>

<template>
  <div :class="[
    'grid gap-y-2 gap-x-4 grid-cols-[min-content_auto_min-content] grid-rows-[min-content_min-content_auto] p-3 m-1 border border-gray-300',
    { 'bg-blue-100': isCurrentActive, 'hover:bg-gray-100': !isCurrentActive },
  ]">
    <RouterLink
      class="col-span-2"
      :to="{ name: 'structure', params: { structureId: structure.id } }"
    >
      <div class="font-semibold">{{ structure.structures.chemical_formula }}</div>
      <div class="text-sm text-gray-500">{{ structure.status }}</div>
    </RouterLink>
  </div>
</template>

<style scoped>
.grid {
  transition: all 0.2s ease;
}
</style>
