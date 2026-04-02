import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ThemeService {

  private theme: string = 'dark';

  toggleTheme() {
    this.theme = this.theme === 'light' ? 'dark' : 'light';

    localStorage.setItem('app-theme', this.theme);
  }

  getCurrentTheme() {
    return localStorage.getItem('app-theme') ? localStorage.getItem('app-theme') : 'dark';
  }
}
