import {Component, Input, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from "@angular/forms";
import {NgxSliderModule, Options} from '@angular-slider/ngx-slider';
import {SliderInputComponent} from "../shared/slider-input/slider-input.component";
import {NgIf} from "@angular/common";
import {ToastrService} from "ngx-toastr";
import {TrackService} from "../../services/track.service";

@Component({
  selector: 'app-generate-music-form',
  standalone: true,
  imports: [
    FormsModule,
    ReactiveFormsModule,
    NgxSliderModule,
    SliderInputComponent,
    NgIf
  ],
  templateUrl: './generate-music-form.component.html',
  styleUrl: './generate-music-form.component.css'
})
export class GenerateMusicFormComponent implements OnInit {
  @Input() public mode: string = "default"

  public form!: FormGroup;
  public advancedForm!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private trackService: TrackService,
    private toastrService: ToastrService,
  ) {}

  ngOnInit() {
    this.advancedForm = this.fb.group({
      acousticness: [0.5, [Validators.required, Validators.min(0), Validators.max(1)]],
      danceability: [0.5, [Validators.required, Validators.min(0), Validators.max(1)]],
      energy: [0.5, [Validators.required, Validators.min(0), Validators.max(1)]],
      instrumentalness: [0.5, [Validators.required, Validators.min(0), Validators.max(1)]],
      key: [5, [Validators.required, Validators.min(-1), Validators.max(11)]],
      liveness: [0.5, [Validators.required, Validators.min(0), Validators.max(1)]],
      loudness: [-30, [Validators.required, Validators.min(-60), Validators.max(0)]],
      mode: [0.5, [Validators.required, Validators.min(0), Validators.max(1)]],
      speechiness: [0, [Validators.required, Validators.min(0), Validators.max(1)]],
      tempo: [0.5, [Validators.required]],
      valence: [0.5, [Validators.required, Validators.min(0), Validators.max(1)]],
      explicit: [1, [Validators.required]]
    });

    this.form = this.fb.group({
      acousticness: [0.5, [Validators.required, Validators.min(0), Validators.max(1)]],
      danceability: [0.5, [Validators.required, Validators.min(0), Validators.max(1)]],
      energy: [0.5, [Validators.required, Validators.min(0), Validators.max(1)]],
      instrumentalness: [0.5, [Validators.required, Validators.min(0), Validators.max(1)]],
      key: [5, [Validators.required, Validators.min(-1), Validators.max(11)]],
      liveness: [0, [Validators.required, Validators.min(0), Validators.max(1)]],
      loudness: [-30, [Validators.required, Validators.min(-60), Validators.max(0)]],
      mode: [0.5, [Validators.required, Validators.min(0), Validators.max(1)]],
      speechiness: [0.5, [Validators.required, Validators.min(0), Validators.max(1)]],
      tempo: [150, [Validators.required]],
      valence: [0.5, [Validators.required, Validators.min(0), Validators.max(1)]],
      explicit: [0, [Validators.required]]
    });
  }

  submitForm() {
    if (this.mode == "advanced" && this.advancedForm.valid) {
      const trackData = this.advancedForm.value;

      this.trackService.generateTrack(trackData).subscribe({
        next: (response: any) => {
          this.toastrService.info("Note that this might take a while.", "Track is being generated.")
        },
        error: (response: any) => {
          this.toastrService.error("There was an error", "Track could not be generated.")
        },
      })
    }

    if (this.mode == "default" && this.form.valid) {
      const trackData = this.form.value;

      this.trackService.generateTrack(trackData).subscribe({
        next: (response: any) => {
          this.toastrService.info("Note that this might take a while.", "Track is being generated.")
        },
        error: (response: any) => {
          this.toastrService.error("There was an error", "Track could not be generated.")
        },
      })
    }
  }
}
