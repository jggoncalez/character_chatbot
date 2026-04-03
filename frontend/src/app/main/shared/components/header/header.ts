import { Component, inject } from '@angular/core';
import { ThemeService } from '../../services/theme-service';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { onNavigate } from '../../utils/navigation';
import { IHeaderConfig } from './interfaces/header-config';

@Component({
  selector: 'app-header',
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './header.html',
  styleUrl: './header.scss',
})
export class Header {
  themeService = inject(ThemeService);

  links : IHeaderConfig[] = [
    {
      path : "feed",
      icon : "bi-house"
    },
    {
      path : "friends",
      icon : "bi-people"
    },
    {
      path : "profile",
      icon : "bi-person"
    }
  ]

  navigate = onNavigate;
}
