import {Injectable, OnInit} from '@angular/core';
import {SocketService} from "./socket.service";
import {ToastrService} from "ngx-toastr";

@Injectable({
  providedIn: 'root'
})
export class NotificationService {

  public constructor(
    public socketService: SocketService,
    public toastrService: ToastrService,
  ) {
    this.trackGenerated();
  }

  public trackGenerated() {
    this.socketService.on('track-generated', (data: any) => {
      this.toastrService.success("Listen to it in 'Library'.", "Track generated!")
    })
  }
}
