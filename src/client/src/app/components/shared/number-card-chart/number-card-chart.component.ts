import {Component, Input} from '@angular/core';
import {NgxChartsModule} from "@swimlane/ngx-charts";

@Component({
  selector: 'app-number-card-chart',
  standalone: true,
  imports: [
    NgxChartsModule
  ],
  templateUrl: './number-card-chart.component.html',
  styleUrl: './number-card-chart.component.css'
})
export class NumberCardChartComponent {
  @Input() public title: string = "Title";
  @Input() public data: [] = [];
  @Input() public size: [number, number] = [150, 150];
  @Input() public cardColor: string = "#0f2052";
  @Input() public colorScheme: any = {
    domain: ['#5AA454', '#A10A28', '#892cc7', '#c97834']
  };
}
