import { Component, inject, input } from '@angular/core';
import { ThemeService } from '../../../../services/theme-service';
import { Conversation } from './components/conversation/conversation';
import { InputChat } from './components/input-chat/input-chat';
import { ICharacterConfig } from '../../../../interfaces/character-config';
import { ContainerChatService } from '../../service/container-chat-service';
import { ChatService } from '../../../../services/chat-service';

@Component({
  selector: 'app-floating-chat',
  providers : [ChatService],
  imports: [Conversation,InputChat],
  templateUrl: './floating-chat.html',
  styleUrl: './floating-chat.scss',
})
export class FloatingChat {
  themeService = inject(ThemeService);
  agentInput = input.required<ICharacterConfig>();
  private containerChatService = inject(ContainerChatService);

  isMinimized = false;

  toggleMinimize(): void {
    this.isMinimized = !this.isMinimized;
  }

  close(): void {
    this.containerChatService.remove(this.agentInput());
  }
  get isDark(): boolean {
    return this.themeService.getCurrentTheme() === 'dark';
  }
}
