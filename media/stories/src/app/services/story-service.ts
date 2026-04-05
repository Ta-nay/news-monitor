import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class StoryService {
  private apiUrl = 'http://127.0.0.1:8000/story/story/';

  constructor(private http: HttpClient) {}

  getStories(search?: string): Observable<any>  {
  const url = search
    ? `${this.apiUrl}?search=${search}`
    : this.apiUrl;
  return this.http.get<any>(url, { withCredentials: true });
}

  getStory(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}${id}/`, {
    withCredentials: true
  });
  }

  createStory(data: any): Observable<any> {
    return this.http.post(this.apiUrl, data, {
    withCredentials: true
  });
  }

  updateStory(id: number, data: any): Observable<any> {
    return this.http.patch(`${this.apiUrl}${id}/`, data, {
    withCredentials: true
  });
  }

  deleteStory(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}${id}/`, {
    withCredentials: true
  });
  }
}
