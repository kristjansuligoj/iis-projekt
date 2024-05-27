import { Routes } from '@angular/router';
import { HomePageComponent } from "./components/pages/home-page/home-page.component";
import { ProfilePageComponent } from "./components/pages/profile-page/profile-page.component";
import { GenerateMusicPageComponent } from "./components/pages/generate-music-page/generate-music-page.component";
import { AdminPanelPageComponent } from "./components/pages/admin-panel-page/admin-panel-page.component";
import {AuthorizationComponent} from "./components/authorization/authorization.component";
import {AuthGuard} from "./guards/auth.guard";
import {LibraryPageComponent} from "./components/pages/library-page/library-page.component";

export const routes: Routes = [
  {
    path: '',
    component: HomePageComponent,
    title: 'Homepage',
  },
  {
    path: 'profile',
    component: ProfilePageComponent,
    title: 'My profile',
  },
  {
    path: 'authorization/callback',
    component: AuthorizationComponent,
    title: 'Authorization',
  },
  {
    path: 'generate-music',
    component: GenerateMusicPageComponent,
    title: 'Generate music',
    canActivate: [AuthGuard],
  },
  {
    path: 'library',
    component: LibraryPageComponent,
    title: 'Library',
    canActivate: [AuthGuard],
  },
  {
    path: 'admin-panel',
    component: AdminPanelPageComponent,
    title: 'Admin panel',
    canActivate: [AuthGuard],
  },
];
