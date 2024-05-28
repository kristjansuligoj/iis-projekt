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
  @Input() public data: [] = [];
  @Input() public size: [number, number] = [150, 150];
  @Input() public colorScheme: any = {
    domain: ['#5AA454', '#A10A28', '#C7B42C', '#AAAAAA']
  };
}
