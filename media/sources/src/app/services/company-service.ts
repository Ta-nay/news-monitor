import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Company } from '../models/source.model';

@Injectable({
  providedIn: 'root',
})
export class CompanyService {
  private apiUrl = 'http://127.0.0.1:8000/company/company/'
  constructor(private http: HttpClient) {}
  searchCompanies(query: string): Observable<Company[]> {
    const params = new HttpParams().set('search', query);
    return this.http.get<Company[]>(this.apiUrl, { params });
  }
}
