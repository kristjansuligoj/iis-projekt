import {Component, OnInit} from '@angular/core';
import {MetricsService} from "../../services/metrics.service";
import {LineChartComponent} from "../shared/line-chart/line-chart.component";
import {NgIf} from "@angular/common";
import {NumberCardChartComponent} from "../shared/number-card-chart/number-card-chart.component";

@Component({
  selector: 'app-metrics-of-today',
  standalone: true,
  imports: [
    LineChartComponent,
    NgIf,
    NumberCardChartComponent
  ],
  templateUrl: './metrics-of-today.component.html',
  styleUrl: './metrics-of-today.component.css'
})
export class MetricsOfTodayComponent implements OnInit {

  public generateGraph: boolean = false;

  public metricsGraphData: any = [];
  public predictionsGraphData: any = []

  public constructor(
    public metricsService: MetricsService
  ) {}

  public ngOnInit() {
    this.metricsService.getMetricsOfToday().subscribe({
      next: (response: any) => {
        if (response.hasOwnProperty('total_predictions')) {
          const totalPredictions = response['total_predictions'];

          if (totalPredictions && totalPredictions > 0) {
            const accuracy = response['accuracy'];
            const f1 = response['f1'];
            const falsePredictions = response['false_predictions']
            const precision = response['precision']
            const recall = response['recall']

            this.metricsGraphData.push({
              'name': "Accuracy",
              'value': response['accuracy'],
            })

            this.metricsGraphData.push({
              'name': "F1",
              'value': response['f1'],
            })

            this.metricsGraphData.push({
              'name': "Precision",
              'value': response['precision'],
            })

            this.metricsGraphData.push({
              'name': "Recall",
              'value': response['recall'],
            })

            this.predictionsGraphData.push({
              'name': "Total predictions",
              'value': totalPredictions,
            })

            this.predictionsGraphData.push({
              'name': "False predictions",
              'value': response['false_predictions'],
            })

            this.generateGraph = true;
          }
        } else {
          // Handle the case where 'total_predictions' doesn't exist
          console.log('total_predictions does not exist in the response.');
        }
      },
      error: (response: any) => {
        console.log(response);
      },
    })
  }
}
