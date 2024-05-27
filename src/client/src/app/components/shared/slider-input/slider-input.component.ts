import {Component, Input} from '@angular/core';
import {FormGroup, ReactiveFormsModule} from "@angular/forms";

@Component({
  selector: 'app-slider-input',
  standalone: true,
    imports: [
        ReactiveFormsModule
    ],
  templateUrl: './slider-input.component.html',
  styleUrl: './slider-input.component.css'
})
export class SliderInputComponent {
  @Input() label: string = '';
  @Input() controlName: string = '';
  @Input() formGroup: FormGroup = new FormGroup({});
  @Input() minValue: number = 0;
  @Input() maxValue: number = 1;
  @Input() step: number = 0.001;
  @Input() description: string = "";
}
