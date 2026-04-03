import { Component, inject } from '@angular/core';
import { ThemeService } from '../../../../../../services/theme-service';

@Component({
  selector: 'app-conversation',
  imports: [],
  templateUrl: './conversation.html',
  styleUrl: './conversation.scss',
})
export class Conversation {
  themeService = inject(ThemeService);

  get isDark(): boolean {
    return this.themeService.getCurrentTheme() === 'dark';
  }
}
