<script lang="ts" setup>
  import {
    GoForm,
    GoInputControl,
    useBrowserStorageItem,
    provideGoForm,
    GoFormActions,
  } from '@constructor/ui';
  import { ref } from 'vue';
  import { useCreateStructureRequest } from '@/api/structures';
  import type { StructureCreateForm, Structure } from '@/api/types/structure';
  import { mockStructure } from '@/modules/structure/helper/helper';

  const initialValues = ref<StructureCreateForm>({
    api_key: 'TANIzwMjjHwX7G8NjP0LOLPMd44KSVpG',
    material_id: 'mt-',
    fmax: 0.05,
    max_steps: 200,
  });

  const { meta, values } = provideGoForm<StructureCreateForm>({
    initialValues: initialValues.value,
  });
  const { request: requestCreateStructure } = useCreateStructureRequest();
  const errorMessage = ref<string | null>(null);
  const { get, set } = useBrowserStorageItem<Structure[]>('structures', {
    storageArea: 'localStorage',
  });

  async function onSubmit() {
    errorMessage.value = null;
    const structures = get() || [];

    try {
      await requestCreateStructure(values);
      window.location.reload();
    } catch {
      structures.push(mockStructure as Structure);
      set(structures);
      window.location.reload();
    }
  }
</script>

<template>
  <GoForm :submit="onSubmit">
    <GoInputControl label="API Key" name="api_key" rules="required" />
    <GoInputControl label="Material ID" name="material_id" rules="required" />
    <GoInputControl label="Fmax" name="fmax" rules="required" />
    <GoInputControl label="Max Steps" name="max_steps" rules="required" />

    <GoFormActions right :disabled="!meta.valid" :submit-text="'Create Structure'" />
  </GoForm>
</template>

<style scoped></style>
