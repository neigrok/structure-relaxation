<script lang="ts" setup>
  import { onBeforeMount, onMounted, onUnmounted, ref, watch } from 'vue';
  import { injectNglViewer } from '@/components/BaseNglViewer/nglViewer';

  const { stageInstance, ngl, initLibrary, setStage, dispose, isErrorState } = injectNglViewer();
  const element = ref<HTMLDivElement>();

  watch([ngl, element], onStageDataChange);
  // Watch for error state changes to attempt recovery
  watch(isErrorState, (hasError) => {
    if (hasError && element.value) {
      // If we're in an error state, try to recreate the stage
      console.log('Attempting to recover from WebGL error state');
      setTimeout(() => {
        if (element.value) setStage(element.value);
      }, 300);
    }
  });
  
  onBeforeMount(initLibrary);
  onMounted(() => document.addEventListener('keydown', onKeyDown));
  onUnmounted(() => {
    document.removeEventListener('keydown', onKeyDown);
    // Properly dispose of the viewer when component is unmounted
    dispose();
  });

  async function onStageDataChange() {
    if (ngl.value && element.value) {
      setStage(element.value);
    }
  }

  function onResize() {
    stageInstance.value?.handleResize();
  }

  function onKeyDown(event: KeyboardEvent) {
    if (stageInstance.value && event.code === 'Digit0' && event.ctrlKey) {
      stageInstance.value.autoView();
      stageInstance.value.viewerControls.rotate([0, 0, 0, 0]);
    }
  }
</script>

<template>
  <div class="base-ngl-viewer">
    <div ref="element" @resize="onResize" class="view"></div>
    <div v-if="isErrorState" class="error-overlay">
      <div class="error-message">WebGL rendering error. Attempting to recover...</div>
    </div>
    <div class="info">
      <div class="info-row">
        <span class="info-key">LMB+Shift</span>
        <span class="info-action">Zoom</span>
      </div>
      <div class="info-row">
        <span class="info-key">LMB</span>
        <span class="info-action">Rotate</span>
      </div>
      <div class="info-row">
        <span class="info-key">Ctrl+0</span>
        <span class="info-action">Reset view</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .base-ngl-viewer {
    position: relative;
    flex-grow: 1;
  }

  .info {
    position: absolute;
    display: flex;
    gap: 16px;
    inset-block-end: 4px;
    inset-inline-start: 50%;
    pointer-events: none;
    transform: translateX(-50%);
  }

  .info-row {
    display: flex;
    gap: 4px;
  }

  .info-key {
    color: #fff; /* Replace with appropriate color */
    font-weight: 500;
  }

  .info-action {
    color: #ccc; /* Replace with appropriate color */
  }

  .view {
    position: absolute;
    inset: 0;
  }
  
  .error-overlay {
    position: absolute;
    inset: 0;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10;
  }
  
  .error-message {
    color: #fff;
    background-color: rgba(255, 0, 0, 0.7);
    padding: 10px 20px;
    border-radius: 4px;
    font-weight: 500;
  }
</style>
