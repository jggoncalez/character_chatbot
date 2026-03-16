import { Component, inject } from '@angular/core';
import { ConversationService } from './services/conversation-service';

@Component({
  selector: 'app-conversation',
  imports: [],
  templateUrl: './conversation.html',
  styleUrl: './conversation.scss',
})
export class Conversation {
  conversationService = inject(ConversationService);
  inputs = this.conversationService.read();
}
