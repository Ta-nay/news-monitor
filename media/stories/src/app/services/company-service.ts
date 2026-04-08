import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { Company } from '../models/story.models';

interface CompanyResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Company[];
}

@Injectable({
  providedIn: 'root',
})
export class CompanyService {
  private apiUrl = 'http://127.0.0.1:8000/company/company/';
  constructor(private http: HttpClient) {}
  searchCompanies(query: string) {
    return this.http
      .get<CompanyResponse>(this.apiUrl, {
        params: { search: query },
      })
      .pipe(map((res) => res.results));
  }
}
