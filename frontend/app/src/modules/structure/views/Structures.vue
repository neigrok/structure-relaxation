<script lang="ts" setup>
  import StructureFormCreate from '@/modules/structure/components/StructureFormCreate.vue';
  import StructuresList from '@/modules/structure/components/StructuresList.vue';
  import { useRouteStructureId } from '@/modules/structure/services/helpers.ts';

  const structureId = useRouteStructureId();
</script>

<template>
  <div class="structures-page">
    <div class="menu-container">
      <div class="menu">
        <StructuresList />
      </div>
    </div>
    <div class="content">
      <RouterView v-slot="{ Component: Structure }">
        <Component :is="Structure" v-if="Structure" :key="structureId" />
        <div v-else class="flex justify-center items-center h-full">
          <StructureFormCreate />
        </div>
      </RouterView>
    </div>
  </div>
</template>

<style scoped>
  .structures-page {
    display: flex;
    flex-grow: 1;
    flex-direction: column;
    block-size: 100vh;
  }

  .menu-container {
    display: flex;
    position: relative;
    flex-shrink: 0;
    align-self: stretch;
    border-inline-end: 1px solid #ccc;
    inline-size: 100%;
    block-size: 350px;
    margin-block-end: 20px;
  }

  .menu {
    position: absolute;
    display: flex;
    flex-direction: column;
    inset: 0;
    background-color: #f0f0f0;
  }

  .content {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    overflow-y: auto;
  }

  @media (min-width: 768px) {
    .structures-page {
      display: flex;
      flex-grow: 1;
      flex-direction: row;
    }

    .menu-container {
      inline-size: 300px;
      block-size: 100vh;
    }
  }
</style>
