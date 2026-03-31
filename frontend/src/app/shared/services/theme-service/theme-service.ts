import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ThemeService {
  private theme: string = 'dark';

  toggleTheme() {
    this.theme = this.theme === 'light' ? 'dark' : 'light';
  }

  getCurrentTheme() {
    return this.theme;
  }
}
