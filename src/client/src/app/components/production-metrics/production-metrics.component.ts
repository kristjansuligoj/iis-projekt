import {Component, OnInit} from '@angular/core';
import {MetricsService} from "../../services/metrics.service";
import {NgxChartsModule} from "@swimlane/ngx-charts";
import {LineChartComponent} from "../shared/line-chart/line-chart.component";

@Component({
  selector: 'app-production-metrics',
  standalone: true,
  imports: [
    NgxChartsModule,
    LineChartComponent
  ],
  templateUrl: './production-metrics.component.html',
  styleUrl: './production-metrics.component.css'
})
export class ProductionMetricsComponent implements OnInit {
  public generateGraph: boolean = false;

  public graphData: any = [{
    "name": "Production accuracy",
    "series": []
  }];

  public constructor(
    public metricsService: MetricsService,
  ) {}

  public ngOnInit() {
    this.metricsService.getProductionMetrics().subscribe({
      next: (response: any) => {
        for(const accuracy of response) {
          this.graphData[0].series.push({
            "name": accuracy['datetime'],
            "value": accuracy['accuracy'],
          })
        }

        this.generateGraph = true;
      },
      error: (response: any) => {
        console.log(response);
      },
    })
  }
}
