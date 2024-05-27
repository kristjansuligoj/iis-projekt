import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  standalone: true,
  name: 'dateFormat'
})
export class DateFormatPipe implements PipeTransform {
  transform(value: string): string {
    const date = new Date(value);
    return `${this.padZero(date.getMonth() + 1)}/${this.padZero(date.getDate())}/${date.getFullYear()} at ${this.padZero(date.getHours())}:${this.padZero(date.getMinutes())}`;
  }

  private padZero(num: number): string {
    return num < 10 ? '0' + num : num.toString();
  }
}
