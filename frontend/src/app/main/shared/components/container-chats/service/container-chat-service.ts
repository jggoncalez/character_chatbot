import { computed, Injectable, signal } from '@angular/core';
import { ICharacterConfig } from '../../../interfaces/character-config';

@Injectable({
  providedIn: 'root',
})
export class ContainerChatService {

  private _chats = signal<ICharacterConfig[]>([]);

  getChats = computed(() => this._chats())


  set(config : ICharacterConfig) {
    this._chats.update((value) => {
      if(value.some(value => value === config)) {
        return value;
      } else {
        return [...value, config];
      }
    });
  }
}
