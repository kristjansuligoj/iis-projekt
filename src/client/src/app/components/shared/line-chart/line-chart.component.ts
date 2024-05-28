import {Component, Input} from '@angular/core';
import {LegendPosition, NgxChartsModule} from "@swimlane/ngx-charts";

@Component({
  selector: 'app-line-chart',
  standalone: true,
  imports: [
    NgxChartsModule
  ],
  templateUrl: './line-chart.component.html',
  styleUrl: './line-chart.component.css'
})
export class LineChartComponent {
  @Input() public data: any[] = [];
  @Input() public size: [number, number] = [500, 500];
  @Input() public showLegend: boolean = true;
  @Input() public timeline: boolean = true;
  @Input() public showGrid: boolean = true;
  @Input() public xAxis: boolean = true;
  @Input() public yAxis: boolean = true;
  @Input() public xAxisLabel: string = "x label";
  @Input() public yAxisLabel: string = "y label";
  @Input() public yScaleMax: number = 1;
  @Input() public yScaleMin: number = 0;
  @Input() public colorScheme: any = {
    domain: ['#5AA454', '#A10A28', '#C7B42C', '#AAAAAA']
  };
}
