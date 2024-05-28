import { Component } from '@angular/core';
import {AuthService} from "../../../services/auth.service";
import {Router} from "@angular/router";
import {NgForOf} from "@angular/common";
import {UnixTimestampToDatetimePipe} from "../../../pipes/unix-timestamp-to-datetime.pipe";
import {ProductionMetricsComponent} from "../../production-metrics/production-metrics.component";
import {MetricsOfTodayComponent} from "../../metrics-of-today/metrics-of-today.component";

@Component({
  selector: 'app-admin-panel-page',
  standalone: true,
  imports: [
    NgForOf,
    UnixTimestampToDatetimePipe,
    ProductionMetricsComponent,
    MetricsOfTodayComponent
  ],
  templateUrl: './admin-panel-page.component.html',
  styleUrl: './admin-panel-page.component.css'
})
export class AdminPanelPageComponent {
  public constructor(
    public authService: AuthService,
    public router: Router,
  ) {}
}
