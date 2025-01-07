import { computed } from 'vue';
import { useRoute } from 'vue-router';

export function useRouteStructureId() {
  const route = useRoute();

  return computed(() => route.params.structureId as string);
}
