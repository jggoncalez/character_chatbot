import { computed, inject, Injectable, signal, WritableSignal } from '@angular/core';
import { IHistoryConfig } from '../interfaces/history-config';
import { IChatConfig } from '../../../interfaces/chat-config';
import { ApiService } from '../../../../../../shared/services/api-service';

@Injectable({
  providedIn: 'root',
})
export class ConversationService {
  apiService = inject(ApiService);

  public isThinking = signal<boolean>(false);
  public currentChat = signal<IHistoryConfig | null>(null);

  startChat(config: IChatConfig) {
    this.apiService.getHistory(config.agent).subscribe({
      next: (res) => {
        const messages = res.history.map(h => ({
          sender: (h.role === 'user' ? 'user' : 'agent') as 'user' | 'agent',
          content: h.content,
          state: h.state
        }));

        this.currentChat.set({
          id: crypto.randomUUID(),
          config,
          messages,
          createdAt: new Date()
        });
      },
      error: () => {
        this.currentChat.set({
          id: crypto.randomUUID(),
          config,
          messages: [],
          createdAt: new Date()
        });
      }
    });
  }

  set(text: string) {
    const chat = this.currentChat();
    if (!chat) return;
    this.isThinking.set(true);
    this.currentChat.update(chat => ({
      ...chat!,
      messages: [...chat!.messages, { sender: 'user', content: text }]
    }));
    this.apiService.sendMessage(text, chat.config.agent).subscribe({
      next: (responses) => {
        
        responses.forEach(response => {
          this.currentChat.update(chat => ({
            ...chat!,
            messages: [...chat!.messages, { sender: 'agent', content: response.text, state: response.state }]
          }));
        });
        this.isThinking.set(false);
      },
      error: (error) => {
        console.error('Erro ao enviar mensagem:', error);
        this.isThinking.set(false);
      }
    });
  }
  clearChat() {
    this.currentChat.set(null);
  }

  get() {
    return this.currentChat;
  }
}