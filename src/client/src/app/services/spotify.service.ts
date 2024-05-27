import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class SpotifyService {
  private apiUrl: string = 'http://0.0.0.0:8080/api/spotify';

  constructor(
    private http: HttpClient,
  ) {}

  public getRecentlyPlayedTracks(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/recently_played_tracks`);
  }
}
