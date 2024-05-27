import { Component } from '@angular/core';
import {Router, RouterLink, RouterLinkActive} from "@angular/router";
import {NgIconComponent, provideIcons} from "@ng-icons/core";
import { heroHomeSolid, heroUserSolid, heroMusicalNoteSolid, heroChartBarSolid, heroCloudSolid, heroArrowDownTraySolid } from "@ng-icons/heroicons/solid";
import {AuthService} from "../../../services/auth.service";
import {NgClass, NgIf} from "@angular/common";

@Component({
  selector: 'app-navigation',
  standalone: true,
  imports: [
    RouterLink,
    RouterLinkActive,
    NgIconComponent,
    NgIf,
    NgClass,
  ],
  providers: [
    provideIcons({ heroHomeSolid, heroUserSolid, heroMusicalNoteSolid, heroChartBarSolid, heroCloudSolid, heroArrowDownTraySolid })
  ],
  templateUrl: './navigation.component.html',
  styleUrl: './navigation.component.css'
})
export class NavigationComponent {
  public constructor(
    public authService: AuthService,
  ) {}
}
