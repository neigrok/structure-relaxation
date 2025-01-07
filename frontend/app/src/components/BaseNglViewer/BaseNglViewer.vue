<script lang="ts" setup>
  import { GoLoader, vResize } from '@constructor/ui';
  import { onBeforeMount, onMounted, onUnmounted, ref, watch } from 'vue';
  import BaseLoadError from '@/components/BaseLoadError.vue';
  import { injectNglViewer } from '@/components/BaseNglViewer/nglViewer';

  const { stageInstance, loadState, ngl, initLibrary, setStage } = injectNglViewer();
  const element = ref<HTMLDivElement>();

  watch([ngl, element], onStageDataChange);
  onBeforeMount(initLibrary);
  onMounted(() => document.addEventListener('keydown', onKeyDown));
  onUnmounted(() => document.removeEventListener('keydown', onKeyDown));

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
    <div ref="element" v-resize="onResize" class="view"></div>
    <div v-if="loadState === 'loaded'" class="info">
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
    <div v-else class="state">
      <GoLoader v-if="loadState === 'loading'" />
      <BaseLoadError v-else />
    </div>
  </div>
</template>

<style scoped>
  .base-ngl-viewer {
    position: relative;
    flex-grow: 1;
  }

  .state {
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--go-color-spot-primary);
    inset: 0;
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
    @mixin text-ui-11;
    display: flex;
    gap: 4px;
  }

  .info-key {
    color: var(--go-color-glyph-inverted-info);
    font-weight: 500;
  }

  .info-action {
    color: var(--go-color-glyph-inverted-secondary);
  }

  .view {
    position: absolute;
    inset: 0;
  }
</style>
