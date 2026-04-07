// src/app/models/story.model.ts

export interface Company {
  id: number;
  name: string;
}

export interface Source {
  id: number;
  name: string;
}

export interface Story {
  id: number;
  title: string;
  body_text: string;
  url: string;
  is_owner : boolean;
  is_staff : boolean;
  company: Company;
  source: Source;
  tagged_companies: Company[];

  created_on: string;
  updated_on: string;
}