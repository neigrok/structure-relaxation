import axios from 'axios';
import type {
  ApiStructureGetResponse,
  ApiStructuresPostBody,
  ApiStructuresPostResponse,
} from '@/api/endpoints/structures';

const baseURL = import.meta.env.CONSTRUCTOR_APP_URL;

export function useStructureRequest() {
  return {
    async request(id: string): Promise<ApiStructureGetResponse> {
      const response = await axios.get<ApiStructureGetResponse>(`${baseURL}/relaxations/${id}`);
      return response.data;
    },
  };
}

export function useCreateStructureRequest() {
  return {
    async request(body: ApiStructuresPostBody): Promise<ApiStructuresPostResponse> {
      const response = await axios.post<ApiStructuresPostResponse>(
        `${baseURL}/relaxations`,
        body,
      );
      return response.data;
    },
  };
}
