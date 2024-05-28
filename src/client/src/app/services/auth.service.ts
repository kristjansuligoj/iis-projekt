import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {environment} from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl: string = `${environment.apiUrl}/authorize`;

  public authorized: boolean = false;

  constructor(
    private http: HttpClient,
  ) {
    // Check if the authorization status is saved in local storage
    const authorizedStatus = localStorage.getItem('authorized');

    // If the authorization status is found in local storage, update the 'authorized' property
    if (authorizedStatus) {
      this.authorized = JSON.parse(authorizedStatus);
    } else {
      // If the authorization status is not found in local storage, check it from the server
      this.checkIfAuthorized().subscribe({
        next: (response: any) => {
          this.authorized = true;
          // Save the authorized status to local storage
          localStorage.setItem('authorized', JSON.stringify(true));
        },
        error: (response: any) => {
          this.authorized = false;
          // Save the unauthorized status to local storage
          localStorage.setItem('authorized', JSON.stringify(false));
        },
      });
    }
  }


  public checkIfAuthorized(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/check`);
  }

  public saveTokens(code: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}?code=${code}`);
  }
}
