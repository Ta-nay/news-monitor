export interface Company {
  id: number;
  name: string;
}

export interface Source {
  id: number;
  name: string;
  url: string;
  company: Company;
  tagged_companies: Company[];
  created_by: number;
  updated_by: number;
  created_on: string;
  updated_on: string;
}