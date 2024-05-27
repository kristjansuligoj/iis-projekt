import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'unixTimestampToDatetime',
  standalone: true
})
export class UnixTimestampToDatetimePipe implements PipeTransform {
  transform(title: string): string {
    const numericParts = title.match(/\d+/);
    let timestamp: number = 0;

    if (numericParts) {
      timestamp = parseInt(numericParts[0]);
    } else {
      return '';
    }

    // Create a new Date object with the Unix timestamp
    const date = new Date(timestamp * 1000);

    // Get the components of the date (year, month, day, hours, minutes, seconds)
    const year = date.getFullYear();
    const month = ('0' + (date.getMonth() + 1)).slice(-2);
    const day = ('0' + date.getDate()).slice(-2);
    const hours = ('0' + date.getHours()).slice(-2);
    const minutes = ('0' + date.getMinutes()).slice(-2);
    const seconds = ('0' + date.getSeconds()).slice(-2);

    // Return the formatted date and time string
    return `${day}-${month}-${year} ${hours}:${minutes}:${seconds}`;
  }
}
