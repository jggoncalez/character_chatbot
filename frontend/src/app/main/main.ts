import { Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Header } from './shared/components/header/header';
import { SidebarNav } from './shared/components/sidebar-nav/sidebar-nav';
import { SidebarRemember } from './shared/components/sidebar-remember/sidebar-remember';
import { ThemeService } from './shared/services/theme-service';

@Component({
  selector: 'app-main',
  imports: [RouterOutlet,Header,SidebarNav,SidebarRemember],
  templateUrl: './main.html',
  styleUrl: './main.scss',
})
export class Main {
  themeService = inject(ThemeService);
}
