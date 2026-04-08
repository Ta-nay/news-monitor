import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, Observable, throwError } from 'rxjs';
import { Story } from '../models/story.models';

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

@Injectable({
  providedIn: 'root',
})
export class StoryService {
  private apiUrl = 'http://127.0.0.1:8000/story/story/';

  constructor(private http: HttpClient) {}

  getStories(search: string = '', page: number = 1): Observable<PaginatedResponse<Story>> {
    let params = new HttpParams().set('page', page);
    if (search) {
      params = params.set('search', search);
    }
    return this.http.get<PaginatedResponse<Story>>(this.apiUrl, {
      params,
    }).pipe(catchError((error) => this.handleError(error)));
  }

  getStory(id: number): Observable<Story> {
    return this.http.get<Story>(`${this.apiUrl}${id}/`)
    .pipe(catchError((error) => this.handleError(error)));
  }

  createStory(data: Partial<Story>): Observable<Story> {
    return this.http.post<Story>(this.apiUrl, data)
    .pipe(catchError((error) => this.handleError(error)));
  }

  updateStory(id: number, data: Partial<Story>): Observable<Story> {
    return this.http.patch<Story>(`${this.apiUrl}${id}/`, data)
    .pipe(catchError((error) => this.handleError(error)));
  }

  deleteStory(id: number): Observable<void> {
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
