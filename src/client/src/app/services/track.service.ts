import { HttpClient } from '@angular/common/http';
import {Injectable} from "@angular/core";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root',
})
export class TrackService {
  private apiUrl: string = 'http://0.0.0.0:8080/api/track';

  constructor(
    private http: HttpClient
  ) {}

  downloadTrack(track: string): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/download-specific?track_file_name=${track}`, { responseType: 'blob' });
  }

  public getGeneratedTracks(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/list`);
  }
}