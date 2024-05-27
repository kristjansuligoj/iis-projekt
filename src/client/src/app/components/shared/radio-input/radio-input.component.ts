import {Component, Input} from '@angular/core';
import {FormGroup, ReactiveFormsModule} from "@angular/forms";

@Component({
  selector: 'app-radio-input',
  standalone: true,
  imports: [
    ReactiveFormsModule
  ],
  templateUrl: './radio-input.component.html',
  styleUrl: './radio-input.component.css'
})
export class RadioInputComponent {
  @Input() label: string = '';
  @Input() controlName: string = '';
  @Input() formGroup: FormGroup = new FormGroup({});
  @Input() name: string = '';
  @Input() value: string = '';
  @Input() id: string = '';
}
