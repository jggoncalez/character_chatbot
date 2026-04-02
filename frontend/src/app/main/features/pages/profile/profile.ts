import { NgClass } from '@angular/common';
import { Component, inject } from '@angular/core';
import { ThemeService } from '../../../shared/services/theme-service';

@Component({
  selector: 'app-profile',
  imports: [NgClass],
  templateUrl: './profile.html',
  styleUrl: './profile.scss',
})
export class Profile {
  themeService = inject(ThemeService);
  get isDark(): boolean {
    return this.themeService.getCurrentTheme() === 'dark';
  }
}
