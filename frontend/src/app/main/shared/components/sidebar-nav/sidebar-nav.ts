import { Component, inject } from '@angular/core';
import { ThemeService } from '../../services/theme-service';
import { onNavigate } from '../../utils/navigation';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { ISidebarNavConfig } from './interfaces/sidebar-nav-config';

@Component({
  selector: 'app-sidebar-nav',
  imports: [RouterLink,RouterLinkActive],
  templateUrl: './sidebar-nav.html',
  styleUrl: './sidebar-nav.scss',
})
export class SidebarNav {
  themeService = inject(ThemeService);

  links : ISidebarNavConfig[] = [
    {
      path : "feed",
      name : "Início",
      icon : "bi-house"
    },
    {
      path : "friends",
      name : "Amigos",
      icon : "bi-people"
    },
    {
      path : "profile",
      name : "Perfil",
      icon : "bi-person"
    },
    {
      path : "save-posts",
      name : "Salvos",
      icon : "bi-bookmark-fill"
    },
    {
      path : "settings",
      name : "Configurações",
      icon : "bi-gear"
    }
  ]

  navigate = onNavigate;
}
