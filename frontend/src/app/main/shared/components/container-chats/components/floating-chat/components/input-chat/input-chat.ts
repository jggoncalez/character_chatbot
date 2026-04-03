import { Component, inject } from '@angular/core';
import { ThemeService } from '../../../../../../services/theme-service';

@Component({
  selector: 'app-input-chat',
  imports: [],
  templateUrl: './input-chat.html',
  styleUrl: './input-chat.scss',
})
export class InputChat {
  themeService = inject(ThemeService);

  get isDark(): boolean {
    return this.themeService.getCurrentTheme() === 'dark';
  }
}
