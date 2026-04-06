import { Component, inject, input } from '@angular/core';
import { FloatingChat } from './components/floating-chat/floating-chat';
import { ContainerChatService } from './service/container-chat-service';

@Component({
  selector: 'app-container-chats',
  imports: [FloatingChat],
  templateUrl: './container-chats.html',
  styleUrl: './container-chats.scss',
})
export class ContainerChats {
  containerChatService = inject(ContainerChatService);

  agentsConfig = this.containerChatService.getChats;
}
