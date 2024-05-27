import { Component } from '@angular/core';
import {GenerateMusicFormComponent} from "../../generate-music-form/generate-music-form.component";
import {NgClass, NgIf} from "@angular/common";

@Component({
  selector: 'app-generate-music-page',
  standalone: true,
  imports: [
    GenerateMusicFormComponent,
    NgIf,
    NgClass
  ],
  templateUrl: './generate-music-page.component.html',
  styleUrl: './generate-music-page.component.css'
})
export class GenerateMusicPageComponent {

  public mode: 'default' | 'advanced' = 'default';

  setMode(mode: 'default' | 'advanced') {
    this.mode = mode;
  }
}
