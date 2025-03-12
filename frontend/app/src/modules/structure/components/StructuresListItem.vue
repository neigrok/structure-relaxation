<script lang="ts" setup>
  import type { Structure } from '@/api/types/structure';
  import { useRouteStructureId } from '@/modules/structure/services/helpers.ts';
  import { computed } from 'vue';

  const props = defineProps<{
    structure: Structure;
  }>();

  const structureId = useRouteStructureId();
  const isCurrentActive = computed(() => structureId.value === props.structure.id);

  const downloadTrajectory = () => {
    const link = document.createElement('a');
    link.href = `/api/relaxations/${props.structure.id}/trajectory`;
    link.download = `trajectory_${props.structure.id}.xyz`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };
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

    <div v-if="structure.status === 'FINISHED'" class="flex flex-col gap-2">
      <button
        @click="downloadTrajectory"
        class="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Download XYZ
      </button>
    </div>

  </div>
</template>

<style scoped>
.grid {
  transition: all 0.2s ease;
}
</style>
