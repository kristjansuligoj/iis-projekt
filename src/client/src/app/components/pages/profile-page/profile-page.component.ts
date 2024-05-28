import {Component, OnInit} from '@angular/core';
import {NgForOf, NgIf} from "@angular/common";
import {AuthService} from "../../../services/auth.service";
import {Router} from "@angular/router";
import {DateFormatPipe} from "../../../pipes/date-format.pipe";
import {TrackService} from "../../../services/track.service";
import {environment} from '../../../../environments/environment';

@Component({
  selector: 'app-profile-page',
  standalone: true,
  imports: [
    NgIf,
    NgForOf,
    DateFormatPipe
  ],
  templateUrl: './profile-page.component.html',
  styleUrl: './profile-page.component.css'
})
export class ProfilePageComponent implements OnInit {
  public isAuthorized: boolean = false;
  public tracks: any;

  public constructor(
    public authService: AuthService,
    public trackService: TrackService,
    public router: Router,
  ) {}

  public ngOnInit() {
    this.isAuthorized = this.authService.authorized;

    this.trackService.getRecentlyPlayedTracks().subscribe({
      next: (response: any) => {
        console.log(response);
        this.tracks = response.items;
      },
      error: (response: any) => {
        console.log(response);
      },
    })
  }

  public login(): void {
    const baseUrl: string = environment.baseUrl;

    window.location.href =
      `https://accounts.spotify.com/authorize?` +
      `response_type=code&` +
      `client_id=2b71db2edbd7471cbaf3501242ddd3c7&` +
      `redirect_uri=${baseUrl}/authorization/callback&` +
      `scope=user-read-recently-played`;
  }

  public getArtistNames(artists: any[]): string {
    return artists.map(artist => artist.name).join(', ');
  }
}
