import { Component, inject } from '@angular/core';
import { ThemeService } from '../../../shared/services/theme-service';
import { NgClass } from '@angular/common';

@Component({
  selector: 'app-feed',
  imports: [NgClass],
  templateUrl: './feed.html',
  styleUrl: './feed.scss',
})
export class Feed {
  themeService = inject(ThemeService);

  get isDark(): boolean {
    return this.themeService.getCurrentTheme() === 'dark';
  }
}
