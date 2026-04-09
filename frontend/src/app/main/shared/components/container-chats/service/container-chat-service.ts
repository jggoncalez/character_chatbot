import { computed, inject, Injectable, signal } from '@angular/core';
import { ICharacterConfig } from '../../../interfaces/character-config';
import { ToastService } from '../../toast-messages/services/toast-service';

@Injectable({
  providedIn: 'root',
})
export class ContainerChatService {
  private MAX_CHATS = 3;
  private toastService = inject(ToastService);

  private _chats = signal<ICharacterConfig[]>([]);
  getChats = computed(() => this._chats());
  set(config: ICharacterConfig): void {
    console.log(config)
    this._chats.update((current) => {
      const alreadyOpen = current.some(c => c.agent === config.agent);
      if (alreadyOpen) return current;

      if (current.length >= this.MAX_CHATS) {
        this.toastService.show(
          `Limite de ${this.MAX_CHATS} chats simultâneos atingido.`,
          'danger'
        );
        return current;
      }

      return [...current, config];
    });
  }

  remove(config: ICharacterConfig): void {
    this._chats.update(current =>
      current.filter(c => c.agent !== config.agent) 
    );
  }
}
