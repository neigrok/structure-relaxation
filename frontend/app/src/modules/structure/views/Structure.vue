<script lang="ts" setup>
  import { onMounted, ref } from 'vue';
  import { useStructureRequest } from '@/api/structures';
  import type { Structure } from '@/api/types/structure';
  import NglViewer from '@/modules/ngl/views/NglViewer.vue';
  import { mockStructure } from '@/modules/structure/helper/helper';
  import { useRouteStructureId } from '@/modules/structure/services/helpers';
  import { useLoadState, usePolling } from '@/services/services';

  const structure = ref<Structure>();
  const structureId = useRouteStructureId();
  const { request } = useStructureRequest();
  const { loadState, setLoading, setLoaded } = useLoadState();
  const { start, abort } = usePolling(loadStructureLoop, { timeout: 5000 });

  onMounted(() => {
    setLoading();
    start();
  });

  async function loadStructureLoop() {
    try {
      structure.value = await request(structureId.value);

      if (structure.value.status === 'FINISHED') {
        abort();
        setLoaded();
      }
    } catch {
      structure.value = mockStructure as Structure;
      abort();
      setLoaded();
    }
  }
</script>

<template>
  <template v-if="loadState === 'loading'">
    <div class="flex justify-center items-center h-full">
      <div class="loader"></div>
    </div>
  </template>

  <template v-else-if="structure">
    <div class="flex flex-col justify-center items-center mx-4 my-10">
      <h1 class="text-2xl font-bold mb-2">
        Chemical formula: {{ structure.structures.chemical_formula }}
      </h1>
      <div class="text-lg mb-2">max force = 0{{ structure.optimization.fmax }}</div>
      <div class="text-lg mb-4">Status: {{ structure.status }}</div>
    </div>

    <div class="mt-8 w-full">
      <h2 class="text-center text-xl font-semibold mb-4">Bulk structure</h2>
      <NglViewer :file-content="structure.structures.bulk.structure" />

      <h2 class="text-center text-xl font-semibold mb-4 mt-10">Slab structure</h2>
      <NglViewer :file-content="structure.structures.slab.structure" />
    </div>
  </template>
  <div class="flex justify-center items-center h-full" v-else>
    <h2>Structure not found</h2>
  </div>
</template>

<style scoped>
.loader {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
