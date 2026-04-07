import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SourceService {
  
  private apiUrl = 'http://127.0.0.1:8000/source/source/';
  constructor(private http: HttpClient) {}
  getSources(search: string = '', page: number = 1): Observable<any> {
    let params = new HttpParams().set('page', page);
    if (search) {
      params = params.set('search', search);
    }
    return this.http.get<any>(this.apiUrl, {
      params,
      withCredentials: true
    });
  }

  getSource(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}${id}/`, {
    withCredentials: true
  });
  }

  createSource(data: any): Observable<any> {
    return this.http.post(this.apiUrl, data, {
    withCredentials: true
  });
  }

  updateSource(id: number, data: any): Observable<any> {
    return this.http.patch(`${this.apiUrl}${id}/`, data, {
    withCredentials: true
  });
  }

  deleteSource(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}${id}/`, {
    withCredentials: true
  });
  }
}