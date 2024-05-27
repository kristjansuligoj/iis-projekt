import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, ParamMap, Router} from "@angular/router";
import {AuthService} from "../../services/auth.service";

@Component({
  selector: 'app-authorization',
  standalone: true,
  imports: [],
  templateUrl: './authorization.component.html',
  styleUrl: './authorization.component.css'
})
export class AuthorizationComponent implements OnInit {
  constructor (
    public router: Router,
    public activatedRoute: ActivatedRoute,
    public authService: AuthService,
  ) {}

  public ngOnInit(): void {
    this.activatedRoute.queryParamMap.subscribe((params: ParamMap): void => {
      const code: string | null = params.get('code');

      if (code !== null) {
        this.authService.saveTokens(code).subscribe({
          next: (response: any) => {
            this.authService.authorized = true;
            this.router.navigate(['/'])
          },
          error: (response: any) => {
            console.log(response);
          }
        })
      }
    });
  }
}
