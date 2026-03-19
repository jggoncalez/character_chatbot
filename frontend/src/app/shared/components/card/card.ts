import { Component, inject, input } from '@angular/core';
import { IChatConfig } from '../../../features/pages/chatbot/interfaces/chat-config';
import { Router } from '@angular/router';
import { ChatbotService } from '../../../features/pages/chatbot/services/chatbot-service';
import { ConversationService } from '../../../features/pages/chatbot/components/conversation/services/conversation-service';


@Component({
  selector: 'app-card',
  imports: [],
  templateUrl: './card.html',
  styleUrl: './card.scss',
})
export class Card {
  conversationService = inject(ConversationService);
  router = inject(Router);
  cardConfig = input<IChatConfig>();

  onClick(config: IChatConfig) {
    this.conversationService.startChat(config);
    this.router.navigate(['chat']);
  }
}
