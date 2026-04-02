import { Component, inject, input } from '@angular/core';
import { ConversationService } from './services/conversation-service';
import { StyleTheme } from '../../interfaces/chat-config';

@Component({
  selector: 'app-conversation',
  imports: [],
  templateUrl: './conversation.html',
  styleUrl: './conversation.scss',
})
export class Conversation {
  conversationService = inject(ConversationService);
  inputs = this.conversationService.get();
  theme = input<StyleTheme>();
}