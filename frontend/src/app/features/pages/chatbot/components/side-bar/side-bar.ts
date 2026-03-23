import { Component, inject, input } from '@angular/core';
import { ConversationService } from '../conversation/services/conversation-service';
import { DatePipe } from '@angular/common';
import { Router } from '@angular/router';
import { StyleTheme } from '../../interfaces/chat-config';



@Component({
  selector: 'app-side-bar',
  imports: [DatePipe],
  templateUrl: './side-bar.html',
  styleUrl: './side-bar.scss',
})
export class SideBar {
  conversationService = inject(ConversationService);
  router = inject(Router);
  history = this.conversationService.getHistory();
  theme = input<StyleTheme>();

  novoChat() {
    const current = this.conversationService.currentChat();

    if (current) {
      this.conversationService.createNewEmptyChat(current.config);
    } else {
      this.conversationService.currentChat.set(null);
      this.router.navigate(['']);
    }
  }

  voltar() {
    this.conversationService.currentChat.set(null);
    this.router.navigate(['']);
  }
}
