import type { Component, Stage, StageParameters } from 'ngl';
import type { InjectionKey } from 'vue';
import { inject, provide, ref, shallowRef } from 'vue';

const key: InjectionKey<ReturnType<typeof getNglViewer>> = Symbol('nglViewer');
// Track active viewers to manage WebGL contexts
const activeViewers = new Set<ReturnType<typeof getNglViewer>>();

export function provideNglViewer() {
  const api = getNglViewer();
  activeViewers.add(api);
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
  const maxRetries = 3;
  const retryDelay = 500; // ms
  const isErrorState = ref(false);
  
  // Create a unique ID for this viewer instance
  const viewerId = `viewer-${Math.random().toString(36).substring(2, 9)}`;

  const api = {
    ngl,
    content,
    extension,
    setStage,
    stageInstance,
    componentInstance,
    initLibrary,
    setStructure,
    getStructureName,
    dispose,
    viewerId,
    isErrorState
  };

  return api;

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

    try {
      // Reset error state when setting up a new stage
      isErrorState.value = false;
      
      // to turn on debug use ngl.setDebug(true)
      const options: Partial<StageParameters> = {
        clipDist: 0,
        // Add WebGL context attributes to improve stability
        // We need to cast here because the type definition is incomplete
        // backgroundColor: 'white',
        // Set quality to medium for better performance
        quality: 'medium'
      };

      stageInstance.value = new ngl.value!.Stage(element, options);
      
      // Add event listener for WebGL context lost events
      element.addEventListener('webglcontextlost', handleContextLost, false);
      element.addEventListener('webglcontextrestored', handleContextRestored, false);
      
      initComponent();
    } catch (error) {
      console.error('Failed to set stage:', error);
      isErrorState.value = true;
    }
  }

  function handleContextLost(event: Event) {
    console.warn(`WebGL context lost for viewer ${viewerId}`);
    event.preventDefault(); // Allow context to be restored
    isErrorState.value = true;
  }

  function handleContextRestored() {
    console.log(`WebGL context restored for viewer ${viewerId}`);
    isErrorState.value = false;
    // Reinitialize the component after context is restored
    initComponent();
  }

  function setStructure(newContent: string, newExtension: string) {
    content.value = newContent;
    extension.value = newExtension;
    
    // Reset error state when setting a new structure
    isErrorState.value = false;
    
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

    // If in error state, attempt to recover by recreating the stage
    if (isErrorState.value && stageInstance.value) {
      const element = stageInstance.value.viewer.container as HTMLDivElement;
      stageInstance.value.dispose();
      stageInstance.value = undefined;
      
      // Small delay before recreating the stage
      await new Promise(resolve => setTimeout(resolve, 100));
      setStage(element);
      return;
    }

    try {
      // do not call set loading to prevent flushing of loading screen
      await setComponentWithRetry();
    } catch (error) {
      console.error('Failed to initialize component:', error);
      isErrorState.value = true;
      cleanComponent();
    }
  }

  async function setComponentWithRetry(retryCount = 0): Promise<void> {
    try {
      await setComponent();
    } catch (error) {
      // Check if it's the specific WebGL framebuffer error
      const errorMessage = error instanceof Error ? error.message : String(error);
      const isFramebufferError = errorMessage.includes('Framebuffer not complete') || 
                                errorMessage.includes('readRenderTargetPixels') ||
                                errorMessage.includes('WebGL') ||
                                errorMessage.includes('context');
      
      if (isFramebufferError && retryCount < maxRetries) {
        console.warn(`WebGL error detected in viewer ${viewerId}, retrying (${retryCount + 1}/${maxRetries})...`);
        
        // Mark this viewer as in error state
        isErrorState.value = true;
        
        // Clean up resources
        cleanComponent();
        
        // Pause other viewers temporarily to reduce WebGL context competition
        pauseOtherViewers();
        
        // Wait before retrying to allow WebGL context to reset
        await new Promise(resolve => setTimeout(resolve, retryDelay * (retryCount + 1)));
        
        // Resume other viewers
        resumeOtherViewers();
        
        // Retry with incremented counter
        return setComponentWithRetry(retryCount + 1);
      }
      
      // If we've exhausted retries or it's a different error, rethrow
      throw error;
    }
  }

  function pauseOtherViewers() {
    for (const viewer of activeViewers) {
      if (viewer.viewerId !== viewerId && viewer.stageInstance.value) {
        // Temporarily pause animations in other viewers
        try {
          // Use animation controls instead of requestPause
          viewer.stageInstance.value.animationControls.pause();
        } catch (e) {
          console.warn('Failed to pause viewer:', e);
        }
      }
    }
  }

  function resumeOtherViewers() {
    for (const viewer of activeViewers) {
      if (viewer.viewerId !== viewerId && viewer.stageInstance.value) {
        // Resume animations in other viewers
        try {
          // Use animation controls instead of requestAnimate
          viewer.stageInstance.value.animationControls.resume();
        } catch (e) {
          console.warn('Failed to resume viewer:', e);
        }
      }
    }
  }

  async function setComponent() {
    cleanComponent();
    try {
      const blob = new Blob([content.value!], { type: 'text/plain' });
      
      // Add error handling for loadFile
      let result;
      try {
        result = await stageInstance.value!.loadFile(blob, {
          ext: extension.value!,
          defaultRepresentation: true,
        });
      } catch (loadError: any) {
        console.error('Error loading file:', loadError);
        throw new Error(`Failed to load file: ${loadError.message || 'unknown error'}`);
      }

      if (!result) {
        throw new Error(`Failed to show file ${extension.value}`);
      }

      componentInstance.value = result;

      try {
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
        
        // Reset error state on successful component setup
        isErrorState.value = false;
      } catch (repError: any) {
        console.error('Error adding representations:', repError);
        throw new Error(`Failed to add representations: ${repError.message || 'unknown error'}`);
      }
    } catch (error) {
      // Catch and rethrow to be handled by the retry mechanism
      throw error;
    }
  }

  function cleanComponent() {
    if (componentInstance.value) {
      try {
        stageInstance.value?.removeComponent(componentInstance.value);
      } catch (error) {
        console.warn('Error removing component:', error);
      }
      componentInstance.value = undefined;
    }
  }

  function isComponentDataReady() {
    return !!content.value && !!extension.value && !!stageInstance.value;
  }
  
  function dispose() {
    // Clean up event listeners and WebGL context
    if (stageInstance.value) {
      const element = stageInstance.value.viewer.container as HTMLDivElement;
      element.removeEventListener('webglcontextlost', handleContextLost);
      element.removeEventListener('webglcontextrestored', handleContextRestored);
      
      stageInstance.value.dispose();
      stageInstance.value = undefined;
    }
    
    cleanComponent();
    activeViewers.delete(api);
  }
}
