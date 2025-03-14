<script lang="ts" setup>
  import { onBeforeMount, onUnmounted, watch } from 'vue';
  import BaseNglViewer from '@/components/BaseNglViewer/BaseNglViewer.vue';
  import { provideNglViewer } from '@/components/BaseNglViewer/nglViewer';

  const props = defineProps<{
    fileContent: string;
  }>();

  const ext = 'cif';
  const { initLibrary, setStructure, dispose } = provideNglViewer();

  onBeforeMount(() => init());
  onUnmounted(() => {
    // Ensure proper cleanup when component is unmounted
    dispose();
  });

  // Watch for changes in fileContent to update the structure
  watch(() => props.fileContent, (newContent) => {
    if (newContent) {
      setStructure(newContent, ext);
    }
  });

  async function init() {
    try {
      await Promise.all([initStructure(), initLibrary()]);
    } catch (error) {
      console.error('Failed to initialize NGL viewer:', error);
    }
  }

  async function initStructure() {
    if (props.fileContent) {
      setStructure(props.fileContent, ext);
    }
  }
</script>

<template>
  <div class="ngl-viewer">
    <div class="content">
      <BaseNglViewer />
    </div>
  </div>
</template>

<style scoped>
  .ngl-viewer {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    flex-grow: 1;
    margin-block-end: 16px;
  }

  .content {
    display: flex;
    flex-direction: column;
    block-size: 472px;
    inline-size: 100%;
  }

  @media (min-width: 768px) {
    .content {
      inline-size: 720px;
    }
  }
</style>
