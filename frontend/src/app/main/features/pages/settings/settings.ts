import { NgClass } from '@angular/common';
import { Component, inject } from '@angular/core';
import { ThemeService } from '../../../shared/services/theme-service';

@Component({
  selector: 'app-settings',
  imports: [NgClass],
  templateUrl: './settings.html',
  styleUrl: './settings.scss',
})
export class Settings {
  themeService = inject(ThemeService);

  get isDark(): boolean {
    return this.themeService.getCurrentTheme() === 'dark';
  }
}
