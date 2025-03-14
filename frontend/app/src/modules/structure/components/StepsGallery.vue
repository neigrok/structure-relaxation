<script lang="ts" setup>
import { ref, computed, watch, onBeforeUnmount } from 'vue';
import type { StructureDetails } from '@/api/types/structure';
import NglViewer from '@/modules/ngl/views/NglViewer.vue';

const props = defineProps<{
  steps: StructureDetails[];
}>();

const currentStep = ref(0);
const isPlaying = ref(false);
const playbackSpeed = ref(500); // milliseconds between steps
let playbackInterval: number | null = null;

const totalSteps = computed(() => props.steps.length);

// Watch for changes in steps array and reset current step
watch(() => props.steps, (newSteps, oldSteps) => {
  // Reset to first step when steps array changes
  if (newSteps.length !== oldSteps?.length) {
    currentStep.value = 0;
    stopPlayback();
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

function startPlayback() {
  if (isPlaying.value || totalSteps.value <= 1) return;
  
  isPlaying.value = true;
  
  // Use a more robust playback mechanism with requestAnimationFrame
  // to better synchronize with the browser's rendering cycle
  let lastStepTime = performance.now();
  let animationFrameId: number;
  
  const animate = (timestamp: number) => {
    if (!isPlaying.value) return;
    
    const elapsed = timestamp - lastStepTime;
    
    if (elapsed >= playbackSpeed.value) {
      if (currentStep.value < totalSteps.value - 1) {
        currentStep.value++;
      } else {
        // Loop back to the beginning when reaching the end
        currentStep.value = 0;
      }
      
      lastStepTime = timestamp;
    }
    
    animationFrameId = requestAnimationFrame(animate);
  };
  
  animationFrameId = requestAnimationFrame(animate);
  
  // Store the animation frame ID for cleanup
  playbackInterval = animationFrameId as unknown as number;
}

function stopPlayback() {
  if (playbackInterval) {
    cancelAnimationFrame(playbackInterval as unknown as number);
    playbackInterval = null;
  }
  isPlaying.value = false;
}

function togglePlayback() {
  if (isPlaying.value) {
    stopPlayback();
  } else {
    startPlayback();
  }
}

function updateSpeed(newSpeed: number) {
  playbackSpeed.value = newSpeed;
  if (isPlaying.value) {
    stopPlayback();
    startPlayback();
  }
}

// Clean up interval when component is unmounted
onBeforeUnmount(() => {
  stopPlayback();
});
</script>

<template>
  <div class="steps-gallery" v-if="steps && steps.length > 0">
    <div class="gallery-header">
      <h2 class="text-xl font-semibold text-center mb-4">Optimization Steps</h2>
      
      <!-- Slider control -->
      <div class="slider-container">
        <input 
          type="range" 
          min="0" 
          :max="totalSteps - 1" 
          v-model.number="currentStep"
          class="step-slider"
        >
        <div class="slider-labels">
          <span>Step 1</span>
          <span>Step {{ totalSteps }}</span>
        </div>
      </div>
      
      <div class="playback-controls">
        <button 
          class="play-button" 
          @click="togglePlayback"
          :title="isPlaying ? 'Pause' : 'Play'"
        >
          <span v-if="isPlaying">⏸️</span>
          <span v-else>▶️</span>
        </button>
        
        <div class="speed-controls">
          <span>Speed:</span>
          <select v-model="playbackSpeed" @change="updateSpeed(playbackSpeed)">
            <option :value="1000">Slow</option>
            <option :value="500">Normal</option>
            <option :value="200">Fast</option>
          </select>
        </div>
      </div>
      
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
      <!-- Use a more stable key strategy that doesn't cause complete remounting -->
      <NglViewer 
        :file-content="steps[currentStep].structure" 
        :key="`step-viewer-${currentStep % 2}`"
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

.slider-container {
  width: 100%;
  max-width: 720px;
  margin: 0 auto 1rem;
  padding: 0 1rem;
}

.step-slider {
  width: 100%;
  height: 8px;
  -webkit-appearance: none;
  appearance: none;
  background: #ddd;
  outline: none;
  border-radius: 4px;
  margin: 1rem 0 0.5rem;
}

.step-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #4caf50;
  cursor: pointer;
}

.step-slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #4caf50;
  cursor: pointer;
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #666;
}

.playback-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 1rem 0;
  gap: 1rem;
}

.play-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.speed-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.speed-controls select {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.step-navigation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 720px;
  margin: 0 auto;
  padding: 0 1rem;
}

.nav-button {
  background-color: #f0f0f0;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  transition: background-color 0.2s;
}

.nav-button:hover:not(.disabled) {
  background-color: #e0e0e0;
}

.nav-button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.step-indicator {
  font-weight: 500;
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
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: background-color 0.2s;
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
