import { Component, effect, ElementRef, inject, input, untracked, viewChild } from '@angular/core';
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
  chatService  = inject(ChatService);
 
  agent   = input<string>();
  history = this.chatService.history;
  loading = this.chatService.loading;
 
  private scrollRef = viewChild<ElementRef>('scrollRef');
 
  get isDark(): boolean {
    return this.themeService.getCurrentTheme() === 'dark';
  }
 
  constructor() {
    effect(() => {
      const name = this.agent();
      if (name) this.chatService.loadHistory(name);
    });
 
    effect(() => {
      this.history();
      this.loading();
      untracked(() => this.scrollToBottom());
    });
  }
 
  private scrollToBottom(): void {
    const element = this.scrollRef()?.nativeElement;
    if (element) setTimeout(() => element.scrollTop = element.scrollHeight, 50);
  }

}
