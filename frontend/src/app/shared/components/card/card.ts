import { Component, inject, input } from '@angular/core';
import { IChatConfig } from '../../../features/pages/chatbot/interfaces/chat-config';
import { Router } from '@angular/router';
import { ChatbotService } from '../../../features/pages/chatbot/services/chatbot-service';


@Component({
  selector: 'app-card',
  imports: [],
  templateUrl: './card.html',
  styleUrl: './card.scss',
})
export class Card {
  chatbotService = inject(ChatbotService);
  route = inject(Router);
  cardConfig = input<IChatConfig>();

  onClick() {
    if(this.cardConfig()) {
      this.chatbotService.setConfig(this.cardConfig()!);
      setTimeout(() => {
        this.route.navigate(['chat'])
      },1000);
    } else {
      return;
    }
  }
}
