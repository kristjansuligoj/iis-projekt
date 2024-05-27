import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl: string = 'http://0.0.0.0:8080/api/generate-track';

  constructor(
    private http: HttpClient,
  ) {}

  public generateTrack(trackData: any): Observable<any[]> {
    return this.http.post<any[]>(`${this.apiUrl}`, trackData);
  }
}
