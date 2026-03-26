import { Component, inject, input } from '@angular/core';
import { IChatConfig } from '../../../features/pages/chatbot/interfaces/chat-config';
import { Router } from '@angular/router';
import { ConversationService } from '../../../features/pages/chatbot/components/conversation/services/conversation-service';
import { ToastService } from '../toast-messages/services/toast-service';


@Component({
  selector: 'app-card',
  imports: [],
  templateUrl: './card.html',
  styleUrl: './card.scss',
})
export class Card {
  toastService = inject(ToastService);
  conversationService = inject(ConversationService);
  router = inject(Router);
  cardConfig = input<IChatConfig>();

  onClick(config: IChatConfig) {
    this.toastService.show(`Indo para o chat de ${config.agent}`,'info',2000)
    this.conversationService.startChat(config);
    setTimeout(() => {
      this.router.navigate(['chat']);
    },1000)
  }
}
