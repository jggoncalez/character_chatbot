import { Component, inject } from '@angular/core';
import { ThemeService } from '../../services/theme-service/theme-service';

@Component({
  selector: 'app-sidebar-nav',
  imports: [],
  templateUrl: './sidebar-nav.html',
  styleUrl: './sidebar-nav.scss',
})
export class SidebarNav {
  themeService = inject(ThemeService);
}
