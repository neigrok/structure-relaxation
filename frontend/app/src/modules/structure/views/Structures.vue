<script lang="ts" setup>
  import { GoFillerBlock } from '@constructor/ui';
  import StructureFormCreate from '@/modules/structure/components/StructureFormCreate.vue';
  import StructuresList from '@/modules/structure/components/StructuresList.vue';
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
        <Component :is="Structure" v-if="Structure" />
        <GoFillerBlock v-else center size="lg">
          <StructureFormCreate />
        </GoFillerBlock>
      </RouterView>
    </div>
  </div>
</template>

<style scoped>
  .structures-page {
    display: flex;
    flex-grow: 1;
    flex-direction: column;
  }

  .menu-container {
    display: flex;
    position: relative;
    flex-shrink: 0;
    align-self: stretch;
    border-inline-end: var(--go-border-secondary);
    inline-size: 100%;
    block-size: 350px;
  }

  .menu {
    position: absolute;
    display: flex;
    flex-direction: column;
    inset: 0;
    background-color: var(--go-color-spot-secondary);
  }

  .content {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
  }

  @media (min-width: 768px) {
    .structures-page {
      display: flex;
      flex-grow: 1;
      flex-direction: row;
    }

    .menu-container {
      inline-size: 300px;
      block-size: auto;
    }
  }
</style>
