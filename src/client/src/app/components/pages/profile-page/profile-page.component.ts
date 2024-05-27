import {Component, OnInit} from '@angular/core';
import {NgForOf, NgIf} from "@angular/common";
import {AuthService} from "../../../services/auth.service";
import {Router} from "@angular/router";
import {SpotifyService} from "../../../services/spotify.service";
import {DateFormatPipe} from "../../../pipes/date-format.pipe";

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
  public username: string = "Kristjan";
  public tracks: any;

  public constructor(
    public authService: AuthService,
    public spotifyService: SpotifyService,
    public router: Router,
  ) {}

  public ngOnInit() {
    this.isAuthorized = this.authService.authorized;

    this.spotifyService.getRecentlyPlayedTracks().subscribe({
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
    window.location.href =
      `https://accounts.spotify.com/authorize?` +
      `response_type=code&` +
      `client_id=2b71db2edbd7471cbaf3501242ddd3c7&` +
      `redirect_uri=http://localhost:4200/authorization/callback&` +
      `scope=user-read-recently-played`;
  }

  public getArtistNames(artists: any[]): string {
    return artists.map(artist => artist.name).join(', ');
  }
}
