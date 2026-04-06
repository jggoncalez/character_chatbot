import { computed, inject, Injectable, signal, WritableSignal } from '@angular/core';
import { ApiService } from './api-service';
import { IHistoryResponse } from '../interfaces/history-response';
import { IChatResponse } from '../interfaces/chat-response';

@Injectable({
  providedIn: 'root',
})
export class ChatService {
  apiService = inject(ApiService);

  private _history: WritableSignal<IHistoryResponse | null> = signal(null);
  private _messages: WritableSignal<IChatResponse[]> = signal([]);
  private _loading: WritableSignal<boolean> = signal(false);

  history = computed(() => this._history());
  messages = computed(() => this._messages());
  loading = computed(() => this._loading());

  loadHistory(agentName: string): void {
    this.apiService.getHistory(agentName).subscribe({
      next: (value) => this._history.set(value),
    });
  }

  sendMessage(message: string, agentName: string): void {
    this._loading.set(true);

    this.apiService.sendMessage(message, agentName).subscribe({
      next: (responses) => {
        this._messages.set(responses);

        // Atualiza o histórico após enviar a mensagem
        this.loadHistory(agentName);
      },
      complete: () => this._loading.set(false),
    });
  }

  clearHistory(agentName: string): void {
    this.apiService.clearHistory(agentName).subscribe({
      next: () => {
        this._history.set(null);
        this._messages.set([]);
      },
    });
  }
}
