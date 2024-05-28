import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class MetricsService {
  private apiUrl: string = 'http://0.0.0.0:8080/api/metrics';

  constructor(
    private http: HttpClient
  ) {}

  public getProductionMetrics(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/production_accuracy`);
  }

  public getMetricsOfToday(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/metrics_of_today`);
  }
}
