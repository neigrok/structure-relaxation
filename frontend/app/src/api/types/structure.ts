export type StructureCreateForm = {
  mp_api_key: string;
  material_id: string;
  fmax: number;
  max_steps: number;
};

export type Optimization = {
  progress: number;
  fmax: number;
  max_steps: number;
  forces: [];
  energies: [];
};

export type StructureDetails = {
  format: string;
  structure: string;
};

export type Structures = {
  chemical_formula: string;
  bulk: StructureDetails;
  slab: StructureDetails;
};

export type Structure = {
  id: string;
  status: 'PENDING' | 'RUNNING' | 'FINISHED' | 'FAILED';
  optimization: Optimization;
  structures: Structures;
};
