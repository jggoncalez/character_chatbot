import { isPlatformBrowser } from '@angular/common';
import { inject, Injectable, PLATFORM_ID } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ThemeService {
  private plataformId = inject(PLATFORM_ID);
  private theme: string = 'dark';
 
  toggleTheme() {
    if (isPlatformBrowser(this.plataformId)) {
      this.theme = this.theme === 'light' ? 'dark' : 'light';
      localStorage.setItem('app-theme', this.theme);
    }
  }
 
  setTheme(theme: string) {
    if (isPlatformBrowser(this.plataformId)) {
      this.theme = theme;
      localStorage.setItem('app-theme', this.theme);
    }
  }
 
  getCurrentTheme() {
    if (isPlatformBrowser(this.plataformId)) {
      return localStorage.getItem('app-theme') ?? 'dark';
    } else {
      return 'dark';
    }
  }
}
