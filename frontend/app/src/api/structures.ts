import type {
  ApiStructureGetResponse,
  ApiStructuresPostBody,
  ApiStructuresPostResponse,
} from '@/api/endpoints/structures';
import { apiStructureGet, apiStructuresPost } from '@/api/endpoints/structures';
import { requester } from '@/services/requester';

export function useStructureRequest() {
  return requester
    .entity(apiStructureGet)
    .response<ApiStructureGetResponse>()
    .setup((id: string) => ({
      params: { id },
    }));
}

export function useCreateStructureRequest() {
  return requester
    .entity(apiStructuresPost)
    .response<ApiStructuresPostResponse>()
    .setup((body: ApiStructuresPostBody) => ({
      body,
    }));
}
