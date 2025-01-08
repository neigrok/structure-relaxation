import { ref } from 'vue';

export function useLoadState() {
  const loadState = ref('loading');
  const setLoading = () => (loadState.value = 'loading');
  const setLoaded = () => (loadState.value = 'loaded');
  return { loadState, setLoading, setLoaded };
}

export function usePolling(
  callback: (options: { signal: AbortSignal }) => Promise<void>,
  options: { timeout: number },
) {
  const controller = new AbortController();
  const start = () => {
    const interval = setInterval(() => {
      callback({ signal: controller.signal });
    }, options.timeout);
    controller.signal.addEventListener('abort', () => clearInterval(interval));
  };
  const abort = () => controller.abort();
  return { start, abort };
}
