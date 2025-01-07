import { Endpoint } from '@constructor/services';

export const BASE_URL =
  'https://test-constructor.dev/platform/applications/2fd5d65cb7824fc3bb145ab7fb82d339/api';

export function apiRelaxation<Pathname extends string>(pathname: Pathname) {
  return createEndpoint('relaxation', pathname);
}

function createEndpoint<Pathname extends string>(
  prefix: string,
  pathname: Pathname,
  version: number | null = null,
) {
  return new Endpoint({
    prefix: `${BASE_URL}/${prefix}`,
    pathname,
    version,
  });
}
