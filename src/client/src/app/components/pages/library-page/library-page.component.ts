import {Component, OnInit} from '@angular/core';
import {TrackService} from "../../../services/track.service";
import {NgForOf, NgIf} from "@angular/common";
import {NgxAudioPlayerModule} from "ngx-audio-player";
import {firstValueFrom, Observable} from "rxjs";
import {ToastrService} from "ngx-toastr";
import {UnixTimestampToDatetimePipe} from "../../../pipes/unix-timestamp-to-datetime.pipe";

@Component({
  selector: 'app-library-page',
  standalone: true,
  imports: [
    NgForOf,
    NgIf,
    NgxAudioPlayerModule,
    UnixTimestampToDatetimePipe,
  ],
  templateUrl: './library-page.component.html',
  styleUrl: './library-page.component.css'
})
export class LibraryPageComponent implements OnInit {
  public tracks: any[] = [];

  constructor(
    private trackService: TrackService,
    private toastrService: ToastrService,
  ) {}

  ngOnInit(): void {
    this.getTracks();
  }

  public getTracks(): void {
    this.trackService.getGeneratedTracks().subscribe(async (tracks: any) => {
      let trackCount = 0;
      const totalTracks = tracks[0].length;

      for(const track of tracks[0]) {
        const blobData: Blob = await firstValueFrom(this.trackService.downloadTrack(track));
        const blobUrl: string = window.URL.createObjectURL(blobData);

        const trackData: any = {
          'title': track,
          'url': blobUrl,
        }

        this.tracks.push(trackData);
        trackCount++;

        // Check if all tracks are fetched
        if (trackCount === totalTracks) {
          // Sort tracks based on Unix timestamp in descending order
          this.tracks.sort((first: any, second: any) => {
            const firstTimestamp = first.title.match(/\d+/)[0];
            const secondTimestamp = second.title.match(/\d+/)[0];

            return secondTimestamp - firstTimestamp;
          });
        }
      }
    });
  }
}
