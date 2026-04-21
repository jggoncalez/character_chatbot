import { computed, inject, Injectable, signal, WritableSignal } from '@angular/core';
import { ApiService } from './api-service';
import { IHistoryResponse } from '../interfaces/history-response';
import { IChatResponse } from '../interfaces/chat-response';
import { ToastService } from '../components/toast-messages/services/toast-service';
import { resolveAudioErrorMessage, resolveErrorMessage } from '../utils/error-messages';

@Injectable({
  providedIn: 'root',
})
export class ChatService {
  apiService = inject(ApiService);
  private toastService = inject(ToastService);
 
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
 
    this._history.update(value => {
      if (!value) return value;
      return {
        ...value,
        history: [...value.history, { role: 'user' as const, content: message }]
      };
    });
 
    this.apiService.sendMessage(message, agentName).subscribe({
      next: () => {
        this.loadHistory(agentName);
      },
      error: (error) => {
        const msg = resolveErrorMessage(error);
        this._history.update(value => {
          if (!value) return value;
          return {
            ...value,
            history: [...value.history, { role: 'model' as const, content: msg }]
          };
        });
        this._loading.set(false);
      },
      complete: () => this._loading.set(false),
    });
  }
 
  sendMessageAudio(formData: FormData, agentName: string): void {
    this._loading.set(true);
 
    this.apiService.sendMessageAudio(agentName, formData).subscribe({
      next: (response: any) => {
        this.loadHistory(agentName);
      },
      error: (error) => {
        const msg = resolveAudioErrorMessage(error);
        this._history.update(value => {
          if (!value) return value;
          return {
            ...value,
            history: [...value.history, { role: 'model' as const, content: msg }]
          };
        });
        this._loading.set(false);
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
      error: () => {
        this.toastService.show('Erro ao limpar o histórico. Tente novamente.', 'danger', 3000);
      }
    });
  }

}
