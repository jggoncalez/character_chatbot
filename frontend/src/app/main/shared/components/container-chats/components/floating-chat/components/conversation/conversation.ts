import { Component, inject, input } from '@angular/core';
import { ThemeService } from '../../../../../../services/theme-service';
import { ChatService } from '../../../../../../services/chat-service';

@Component({
  selector: 'app-conversation',
  imports: [],
  templateUrl: './conversation.html',
  styleUrl: './conversation.scss',
})
export class Conversation {
  themeService = inject(ThemeService);
  chatService = inject(ChatService);
  agent = input<string>()

  get isDark(): boolean {
    return this.themeService.getCurrentTheme() === 'dark';
  }

  history = this.chatService.history;

  constructor() {
    const name = this.agent();
    if (name) this.chatService.loadHistory(name);
  }
}
