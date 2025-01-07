<script lang="ts" setup>
  import { useCallbackLoadState, GoLoad } from '@constructor/ui';
  import { onBeforeMount } from 'vue';
  import BaseNglViewer from '@/components/BaseNglViewer/BaseNglViewer.vue';
  import { provideNglViewer } from '@/components/BaseNglViewer/nglViewer';

  const props = defineProps<{
    fileContent: string;
  }>();

  const ext = 'cif';
  const { callback: init, loadState } = useCallbackLoadState(initCallback);
  const { initLibrary, setStructure } = provideNglViewer();

  onBeforeMount(() => init());

  async function initCallback() {
    await Promise.all([initStructure(), initLibrary()]);
  }

  async function initStructure() {
    setStructure(props.fileContent, ext);
  }
</script>

<template>
  <div class="ngl-viewer">
    <div class="content">
      <GoLoad center :load-state="loadState" reload @reload="init">
        <BaseNglViewer />
      </GoLoad>
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
