import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {NavigationComponent} from "./components/shared/navigation/navigation.component";
import {HttpClientModule} from "@angular/common/http";
import {NgxSliderModule} from "@angular-slider/ngx-slider";
import {SocketIoModule} from "ngx-socket-io";
import {SocketService} from "./services/socket.service";
import {NotificationService} from "./services/notification.service";
import {NgxAudioPlayerModule} from "ngx-audio-player";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    NavigationComponent,
    HttpClientModule,
    NgxSliderModule,
    SocketIoModule,
    NgxAudioPlayerModule,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'client';

  constructor(
    private socketService: SocketService,
    private notificationService: NotificationService,
  ) {}
}
