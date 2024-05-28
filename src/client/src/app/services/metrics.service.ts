import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {environment} from "../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class MetricsService {
  private apiUrl: string = `${environment.apiUrl}/metrics`;

  constructor(
    private http: HttpClient
  ) {}

  public getProductionMetrics(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/production-accuracy`);
  }

  public getMetricsOfToday(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/metrics-of-today`);
  }
}
