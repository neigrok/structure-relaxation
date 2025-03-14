<script lang="ts" setup>
  import { computed, onMounted, ref } from 'vue';
  import { useStructureRequest } from '@/api/structures';
  import type { Structure } from '@/api/types/structure';
  import NglViewer from '@/modules/ngl/views/NglViewer.vue';
  import { useRouteStructureId } from '@/modules/structure/services/helpers';
  import { usePolling } from '@/services/services';
  import StructureChart from '@/modules/structure/components/StructureChart.vue';
  import StepsGallery from '@/modules/structure/components/StepsGallery.vue';
  import { useRouter } from 'vue-router';
  import { useStructureStore } from '@/stores/structureStore.ts';
  import { storeToRefs } from 'pinia';
  import { useToast } from 'vue-toast-notification';

  const structure = ref<Structure>();
  const router = useRouter();
  const structureId = useRouteStructureId();
  const { request } = useStructureRequest();
  const toast = useToast();
  const structureStore = useStructureStore();
  const { structures } = storeToRefs(structureStore);
  const { start, abort } = usePolling(loadStructureLoop, { timeout: 5000 });
  const progressBarWidth = computed(() => {
    if (!structure.value) {
      return '0%';
    }

    const { progress, max_steps } = structure.value.optimization;
    const currentIteration = progress * max_steps;
    const progressPercentage = ((currentIteration / max_steps) * 100).toFixed(2);

    return `${progressPercentage}%`;
  });

  onMounted(async () => {
    await loadStructureLoop(); // Start the request immediately
    start();
  });

  async function loadStructureLoop() {
    try {
      structure.value = await request(structureId.value);
      const index = structures.value.findIndex((s) => s.id === structure.value!.id);
      if (index !== -1) {
        structures.value[index] = structure.value;
      }

      if (structure.value.status === 'FINISHED') {
        abort();
      }
    } catch (error) {
      toast.error('Failed to fetch the structure. Structure is removed from the list.');
      const index = structures.value.findIndex((s) => s.id === structureId.value);

      if (index !== -1) {
        structures.value.splice(index, 1);
      }

      abort();
      await router.push({ name: 'structures' });
    }
  }

  const downloadTrajectory = () => {
    if (!structure.value) return;
    
    const link = document.createElement('a');
    link.href = `/api/relaxations/${structure.value.id}/trajectory`;
    link.download = `trajectory_${structure.value.id}.xyz`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };
</script>

<template>
  <template v-if="structure">
    <div class="flex flex-col justify-center items-center mx-4 my-10">
      <h1 class="text-2xl font-bold mb-2">
        Chemical formula: {{ structure.structures.chemical_formula }}
      </h1>
      <div class="text-lg mb-2">max force = {{ structure.optimization.fmax }}</div>
      <div class="text-lg mb-4">
        Status: <strong> {{ structure.status }} </strong>
      </div>
      <button
        v-if="structure.status === 'FINISHED'"
        @click="downloadTrajectory"
        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
      >
        Download XYZ
      </button>
    </div>

    <div class="mt-8 w-full">
      <h2 class="text-center text-xl font-semibold mb-4">Bulk structure</h2>
      <NglViewer :file-content="structure.structures.bulk.structure" />

      <h2 class="text-center text-xl font-semibold mb-4 mt-10">Slab structure</h2>
      <NglViewer :file-content="structure.structures.slab.structure" />
    </div>

    <div class="my-8 px-8 w-full">
      <div class="flex flex-col justify-center items-center">
        <h2 class="flex flex-col justify-center items-center text-xl font-semibold">Progress</h2>
        <div class="progress-bar-container mt-4 max-w-2xl">
          <div class="progress-bar" :style="{ width: progressBarWidth }"></div>
        </div>

        <StructureChart
          class="w-full h-auto max-w-2xl"
          :key="structure.optimization.progress"
          :optimization-data="structure.optimization"
        />
      </div>
    </div>
    
    <!-- Steps Gallery Section -->
    <div class="my-8 px-8 w-full" v-if="structure.steps && structure.steps.length > 0">
      <StepsGallery 
        :steps="structure.steps" 
        :key="`steps-gallery-${structure.id}-${structure.optimization.progress}`" 
      />
    </div>
  </template>
  <div class="flex justify-center items-center h-full" v-else>
    <h2>Structure not found</h2>
  </div>
</template>

<style scoped>
  .progress-bar-container {
    width: 100%;
    background-color: #e0e0e0;
    border-radius: 8px;
    overflow: hidden;
    height: 20px;
  }

  .progress-bar {
    height: 100%;
    background-color: #4caf50;
    transition: width 0.3s;
  }
</style>
