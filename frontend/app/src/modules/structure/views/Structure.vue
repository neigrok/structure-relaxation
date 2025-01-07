<script lang="ts" setup>
  import { type PollingCallbackOptions, usePolling } from '@constructor/services';
  import { GoFillerBlock, GoLoad, useLoadState } from '@constructor/ui';
  import { onMounted, ref } from 'vue';
  import { useStructureRequest } from '@/api/structures';
  import type { Structure } from '@/api/types/structure';
  import NglViewer from '@/modules/ngl/views/NglViewer.vue';
  import { mockStructure } from '@/modules/structure/helper/helper';
  import { useRouteStructureId } from '@/modules/structure/services/helpers';

  const structure = ref<Structure>();
  const structureId = useRouteStructureId();
  const { requestCustom: request } = useStructureRequest();
  const { loadState, setLoading, setLoaded } = useLoadState();
  const { start, abort } = usePolling(loadStructureLoop, { timeout: 5000 });

  onMounted(() => {
    setLoading();
    start();
  });

  async function loadStructureLoop({ signal }: PollingCallbackOptions) {
    try {
      structure.value = await request({ signal }, structureId.value);
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
  <GoLoad :load-state="loadState" center>
    <template v-if="structure">
      <GoFillerBlock center size="lg">
        <h1>Chemical formula: {{ structure.structures.chemical_formula }}</h1>
        <div>max force = 0{{ structure.optimization.fmax }}</div>
        <div>Status: {{ structure.status }}</div>

        <div class="structures-views">
          <h2>Bulk structure</h2>
          <NglViewer :file-content="structure.structures.bulk.structure" />

          <h2>Slab structure</h2>
          <NglViewer :file-content="structure.structures.slab.structure" />
        </div>
      </GoFillerBlock>
    </template>
    <GoFillerBlock v-else center size="lg">
      <template #header>Structure not found</template>
    </GoFillerBlock>
  </GoLoad>
</template>

<style scoped>
  .structures-views {
    margin-block-start: 32px;
    inline-size: 100%;
  }
</style>
