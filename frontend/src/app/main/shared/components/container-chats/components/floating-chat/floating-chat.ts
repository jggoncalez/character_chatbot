import { Component, inject } from '@angular/core';
import { ThemeService } from '../../../../services/theme-service';
import { Conversation } from './components/conversation/conversation';
import { InputChat } from './components/input-chat/input-chat';

@Component({
  selector: 'app-floating-chat',
  imports: [Conversation,InputChat],
  templateUrl: './floating-chat.html',
  styleUrl: './floating-chat.scss',
})
export class FloatingChat {
  themeService = inject(ThemeService);

  isMinimized = false;
  isVisible   = true;
  
  toggleMinimize(): void {
    this.isMinimized = !this.isMinimized;
  }
 
  close(): void {
    this.isVisible = false;
  }
  get isDark(): boolean {
    return this.themeService.getCurrentTheme() === 'dark';
  }
}
