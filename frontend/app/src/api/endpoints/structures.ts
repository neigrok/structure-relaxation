import { apiRelaxation } from '@/api/endpoints/api';
import type { Structure, StructureCreateForm } from '@/api/types/structure';

export const apiStructureGet = apiRelaxation(':id');
export type ApiStructureGetResponse = Structure;

export const apiStructuresPost = apiRelaxation('').post();
export type ApiStructuresPostResponse = Structure;
export type ApiStructuresPostBody = StructureCreateForm;
