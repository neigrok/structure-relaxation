import type { Component, Stage, StageParameters } from 'ngl';
import type { InjectionKey } from 'vue';
import { inject, provide, ref, shallowRef } from 'vue';

const key: InjectionKey<ReturnType<typeof getNglViewer>> = Symbol('nglViewer');

export function provideNglViewer() {
  const api = getNglViewer();

  provide(key, api);

  return api;
}

export function injectNglViewer() {
  return inject(key)!;
}

function getNglViewer() {
  const ngl = shallowRef<{ Stage: typeof Stage; Component: typeof Component }>();
  const stageInstance = shallowRef<Stage>();
  const componentInstance = shallowRef<Component>();
  const content = ref<string>();
  const extension = ref<string>();
  let libPromise: Promise<void>;

  return {
    ngl,
    content,
    extension,
    setStage,
    stageInstance,
    componentInstance,
    initLibrary,
    setStructure,
    getStructureName,
  };

  async function initLibrary() {
    libPromise = loadLibrary();
    return libPromise;
  }

  async function loadLibrary() {
    ngl.value = await import('ngl');
  }

  function setStage(element: HTMLDivElement) {
    if (stageInstance.value) {
      stageInstance.value.dispose();
      stageInstance.value = undefined;
    }

    // to turn on debug use ngl.setDebug(true)
    const options: Partial<StageParameters> = {
      clipDist: 0,
    };

    stageInstance.value = new ngl.value!.Stage(element, options);
    initComponent();
  }

  function setStructure(newContent: string, newExtension: string) {
    content.value = newContent;
    extension.value = newExtension;
    initComponent();
  }

  function getStructureName() {
    return componentInstance.value?.parameters.name;
  }

  async function initComponent() {
    if (!isComponentDataReady()) {
      cleanComponent();
      return;
    }

    try {
      // do not call set loading to prevent flushing of loading screen
      await setComponent();
    } catch (error) {
      throw error;
    }
  }

  async function setComponent() {
    cleanComponent();
    const blob = new Blob([content.value!], { type: 'text/plain' });
    const result = await stageInstance.value!.loadFile(blob, {
      ext: extension.value!,
      defaultRepresentation: true,
    });

    if (!result) {
      throw new Error(`Failed to show file ${extension.value}`);
    }

    componentInstance.value = result;

    // Add default ball+stick representation
    componentInstance.value.addRepresentation('ball+stick', {
      sphereScale: 0.7,
      bondScale: 0.3,
      bondColor: 'yellow',
      aspectRatio: 1.5,
    });

    // Add unit cell
    componentInstance.value.addRepresentation('unitcell', {
      lineWidth: 1,
      color: 'yellow',
      opacity: 1,
    });

    // Center and zoom to structure
    componentInstance.value.autoView();
  }

  function cleanComponent() {
    if (componentInstance.value) {
      stageInstance.value?.removeComponent(componentInstance.value);
      componentInstance.value = undefined;
    }
  }

  function isComponentDataReady() {
    return !!content.value && !!extension.value && !!stageInstance.value;
  }
}
