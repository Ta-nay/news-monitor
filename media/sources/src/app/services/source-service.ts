import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Source } from '../models/source.model';
import { catchError, throwError } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
@Injectable({
  providedIn: 'root',
})

export class SourceService {  
  private apiUrl = 'http://127.0.0.1:8000/source/source/';
  constructor(private http : HttpClient) {}
  getSources(search: string = '', page: number = 1): Observable<PaginatedResponse<Source>> {
    let params = new HttpParams().set('page', page);
    if (search) {
      params = params.set('search', search);
    }
    return this.http.get<PaginatedResponse<Source>>(this.apiUrl, {
      params,
    }).pipe(catchError((error) => this.handleError(error)));
  }

  getSource(id: number): Observable<Source> {
    return this.http.get<Source>(`${this.apiUrl}${id}/`)
    .pipe(catchError((error) => this.handleError(error)));
  }

  createSource(data: Partial<Source>): Observable<Source> {
    return this.http.post<Source>(this.apiUrl, data,)
    .pipe(catchError((error) => this.handleError(error)));
  }

  updateSource(id: number, data: Partial<Source>): Observable<Source> {
    return this.http.patch<Source>(`${this.apiUrl}${id}/`, data)
    .pipe(catchError((error) => this.handleError(error)));
  }

  deleteSource(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${id}/`)
    .pipe(catchError((error) => this.handleError(error)));
  }


  private handleError(error: HttpErrorResponse) {
  let errorMessage = 'An unknown error occurred';
  if (error.error instanceof ErrorEvent) {
    // Client-side error
    errorMessage = `Client error: ${error.error.message}`;
  } else {
    // Server-side error
    errorMessage = `Server error (${error.status}): ${error.message}`;
  }
  console.error(errorMessage);
  return throwError(() => new Error(errorMessage));
  }
}