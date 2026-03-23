import { computed, inject, Injectable, signal, WritableSignal } from '@angular/core';
import { IHistoryConfig } from '../../side-bar/interfaces/history-config';
import { IChatConfig } from '../../../interfaces/chat-config';
import { ApiService } from '../../../../../../shared/services/api-service';
import { ISideBarConfig } from '../../side-bar/interfaces/side-bar-config';

@Injectable({
  providedIn: 'root',
})
export class ConversationService {
  apiService = inject(ApiService);

  private history = signal<IHistoryConfig[]>([]);
  public currentChat = signal<IHistoryConfig | null>(null);

  public sideBarHistory = computed<ISideBarConfig[]>(() => {
    const flatHistory = this.history();
    const map = new Map<string, IHistoryConfig[]>();

    flatHistory.forEach(chat => {
      const agent = chat.config.agent;
      if (!map.has(agent)) {
        map.set(agent, []);
      }
      map.get(agent)!.push(chat);
    });

    return Array.from(map.entries()).map(([agent, historyChats]) => ({
      agent,
      historyChats
    }));
  });

  getHistory() {
    return this.history.asReadonly();
  }

  startChat(config: IChatConfig) {
    this.apiService.getHistory(config.agent).subscribe({
      next: (res) => {
        const mensagens = res.history.map(h => ({
          sender: (h.role === 'user' ? 'user' : 'agent') as 'user' | 'agent',
          content: h.content,
          state: h.state
        }));

        const chat: IHistoryConfig = {
          id: crypto.randomUUID(),
          config,
          messages: mensagens,
          createdAt: new Date()
        };
        
        // 3. CORREÇÃO: Usamos o 'update' para adicionar o novo chat à lista,
        // em vez de 'set([chat])', que apagava o histórico anterior.
        this.history.update(h => [...h, chat]);
        this.currentChat.set(chat);
      },
      error: () => {
        const chat: IHistoryConfig = {
          id: crypto.randomUUID(),
          config,
          messages: [],
          createdAt: new Date()
        };
        // A mesma correção para o caso de erro
        this.history.update(h => [...h, chat]);
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
            messages: [...chat!.messages, { sender: 'agent', content: response.text, state: response.state }]
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

  createNewEmptyChat(config: IChatConfig) {
    const newChat: IHistoryConfig = {
      id: crypto.randomUUID(), 
      config: config,          
      messages: [],            
      createdAt: new Date()
    };
    
    this.history.update(h => [...h, newChat]);
    this.currentChat.set(newChat);
  }

  get() {
    return this.currentChat;
  }
}