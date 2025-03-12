<script lang="ts" setup>
import { ref, computed, watch } from 'vue';
import type { StructureDetails } from '@/api/types/structure';
import NglViewer from '@/modules/ngl/views/NglViewer.vue';

const props = defineProps<{
  steps: StructureDetails[];
}>();

const currentStep = ref(0);

const totalSteps = computed(() => props.steps.length);

// Watch for changes in steps array and reset current step
watch(() => props.steps, (newSteps, oldSteps) => {
  // Reset to first step when steps array changes
  if (newSteps.length !== oldSteps?.length) {
    currentStep.value = 0;
  }
}, { deep: true });

function goToStep(index: number) {
  if (index >= 0 && index < totalSteps.value) {
    currentStep.value = index;
  }
}

function goToPreviousStep() {
  goToStep(currentStep.value - 1);
}

function goToNextStep() {
  goToStep(currentStep.value + 1);
}
</script>

<template>
  <div class="steps-gallery" v-if="steps && steps.length > 0">
    <div class="gallery-header">
      <h2 class="text-xl font-semibold text-center mb-4">Optimization Steps</h2>
      <div class="step-navigation">
        <button 
          class="nav-button" 
          @click="goToPreviousStep" 
          :disabled="currentStep === 0"
          :class="{ 'disabled': currentStep === 0 }"
        >
          <span class="icon">←</span> Previous
        </button>
        <div class="step-indicator">
          Step {{ currentStep + 1 }} of {{ totalSteps }}
        </div>
        <button 
          class="nav-button" 
          @click="goToNextStep" 
          :disabled="currentStep === totalSteps - 1"
          :class="{ 'disabled': currentStep === totalSteps - 1 }"
        >
          Next <span class="icon">→</span>
        </button>
      </div>
    </div>
    
    <div class="step-viewer">
      <NglViewer 
        :file-content="steps[currentStep].structure" 
        :key="`step-viewer-${currentStep}`"
      />
    </div>
    
    <div class="step-thumbnails">
      <div 
        v-for="(step, index) in steps" 
        :key="index"
        class="step-thumbnail" 
        :class="{ 'active': index === currentStep }"
        @click="goToStep(index)"
      >
        {{ index + 1 }}
      </div>
    </div>
  </div>
  <div v-else class="no-steps">
    <p>No optimization steps available yet.</p>
  </div>
</template>

<style scoped>
.steps-gallery {
  width: 100%;
  margin: 2rem 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.gallery-header {
  width: 100%;
  margin-bottom: 1rem;
}

.step-navigation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 720px;
  margin: 0 auto 1rem;
}

.nav-button {
  padding: 0.5rem 1rem;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-button:hover {
  background-color: #45a049;
}

.nav-button.disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.step-indicator {
  font-weight: bold;
}

.step-viewer {
  width: 100%;
  max-width: 720px;
  margin: 0 auto;
}

.step-thumbnails {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1rem;
  max-width: 720px;
}

.step-thumbnail {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.step-thumbnail:hover {
  background-color: #e0e0e0;
}

.step-thumbnail.active {
  background-color: #4caf50;
  color: white;
}

.no-steps {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>
