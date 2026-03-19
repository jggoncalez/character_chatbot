import { inject, Injectable, signal, WritableSignal } from '@angular/core';
import { IHistoryConfig } from '../../side-bar/interfaces/history-config';
import { IChatConfig } from '../../../interfaces/chat-config';
import { ApiService } from '../../../../../../shared/services/api-service';

@Injectable({
  providedIn: 'root',
})
export class ConversationService {
  apiService = inject(ApiService);
  private history = signal<IHistoryConfig[]>([]);

  // conversa ativa no momento
  public currentChat = signal<IHistoryConfig | null>(null);

 getHistory() {
    return this.history.asReadonly();
  }

  startChat(config: IChatConfig) {
    this.apiService.getHistory(config.agent).subscribe({
      next: (res) => {

        const mensagens = res.history.map(h => ({
          sender: (h.role === 'user' ? 'user' : 'agent') as 'user' | 'agent',
          content: h.content
        }));

        const chat: IHistoryConfig = {
          id: crypto.randomUUID(),
          config,
          messages: mensagens,
          createdAt: new Date()
        };
        this.history.set([chat]);
        this.currentChat.set(chat);
      },
      error: () => {
        const chat: IHistoryConfig = {
          id: crypto.randomUUID(),
          config,
          messages: [],
          createdAt: new Date()
        };
        this.history.set([chat]);
        this.currentChat.set(chat);
      }
    });
  }

  set(text: string) {
    if (!this.currentChat()) return;

    this.currentChat.update(chat => ({
      ...chat!,
      messages: [...chat!.messages, { sender: 'user', content: text }]
    }));

    this._syncHistory();

    const characterName = this.currentChat()!.config.agent;
    this.apiService.sendMessage(text, characterName).subscribe({
      next: (responses) => {
        responses.forEach(response => {
          this.currentChat.update(chat => ({
            ...chat!,
            messages: [...chat!.messages, { sender: 'agent', content: response.text }]
          }));
        });
        this._syncHistory();
      },
      error: (err) => console.error('Erro:', err)
    });
  }

  private _syncHistory() {
    const current = this.currentChat();
    if (!current) return;
    this.history.update(h =>
      h.map(entry => entry.id === current.id ? current : entry)
    );
  }

  get() {
    return this.currentChat;
  }
}
