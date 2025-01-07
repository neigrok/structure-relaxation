<script setup lang="ts">
  import { GoLoadError } from '@constructor/ui';
</script>

<template>
  <GoLoadError>
    <template #default>
      Internet connection is lost, or the server is experiencing problems.
    </template>
    <template v-if="$slots.header" #header>
      <slot name="header"></slot>
    </template>
  </GoLoadError>
</template>

<style scoped></style>
