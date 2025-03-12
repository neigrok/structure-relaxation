<script lang="ts" setup>
  import type Plotly from 'plotly.js-dist-min';
  import { onMounted, ref, shallowRef } from 'vue';
  import type { Optimization } from '@/api/types/structure';

  const props = defineProps<{
    optimizationData: Optimization;
  }>();

  const elementPlotly = ref<HTMLDivElement>();
  const plotly = shallowRef<typeof Plotly>();

  onMounted(() => setPlotly());

  async function setPlotly() {
    plotly.value = (await import('plotly.js-dist-min')).default;

    if (props.optimizationData) {
      const forces = props.optimizationData.forces;
      const energies = props.optimizationData.energies.map(
        (e) => e - props.optimizationData.energies[props.optimizationData.energies.length - 1],
      );
      const iterations = forces.length;

      const data: Plotly.Data[] = [
        {
          x: Array.from({ length: iterations }, (_, i) => i + 1),
          y: forces,
          type: 'scatter',
          mode: 'lines+markers',
          name: 'Max Force',
          yaxis: 'y1',
          line: { color: 'blue', shape: 'linear' },
          marker: { color: 'blue' },
        },
        {
          x: Array.from({ length: iterations }, (_, i) => i + 1),
          y: energies,
          type: 'scatter',
          mode: 'lines+markers',
          name: 'Energy',
          yaxis: 'y2',
          line: { color: 'red', dash: 'dash', shape: 'linear' },
          marker: { color: 'red' },
        },
      ];

      const layout: Partial<Plotly.Layout> = {
        title: 'Max Force and Energy during Optimization',
        xaxis: {
          title: 'Iteration',
          type: 'linear',
        },
        yaxis: {
          title: 'Maximum Force (eV/Å)',
          type: 'log',
          titlefont: { color: 'blue' },
          tickfont: { color: 'blue' },
          tickformat: '.1e',
          range: [
            Math.log10(Math.min(...forces)) - 0.1,
            Math.log10(Math.max(...forces)) + 0.1
          ],
          nticks: 2,  // Show only 2 ticks
          showgrid: false,  // Remove vertical grid lines
        },
        yaxis2: {
          title: 'Energy (eV/Å)',
          type: 'log',
          overlaying: 'y',
          side: 'right',
          titlefont: { color: 'red' },
          tickfont: { color: 'red' },
          tickformat: '.1e',
          nticks: 2,  // Show only 2 ticks
          showgrid: false,  // Remove vertical grid lines
          showline: true,  // Remove horizontal line
        },
        legend: { x: 0, y: 1.1, orientation: 'h' },
      };

      const root: Plotly.Root = elementPlotly.value!;
      await plotly.value!.newPlot(root, data, layout);
    }
  }
</script>

<template>
  <div ref="elementPlotly" class="display-plotly"></div>
</template>

<style scoped>
.display-plotly {
  width: 100%;
  height: 400px;
}
</style>
