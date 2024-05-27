import {CanActivateFn, Router} from '@angular/router';
import {AuthService} from "../services/auth.service";
import {inject} from "@angular/core";

export const AuthGuard: CanActivateFn = (): boolean => {
  const authService: AuthService = inject(AuthService);
  const router: Router = inject(Router);

  if (authService.authorized) {
    return true;
  }

  router.navigate(['/profile']);
  return false;
};
