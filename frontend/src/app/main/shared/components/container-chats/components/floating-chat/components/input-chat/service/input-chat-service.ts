import { computed, Injectable, signal } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class InputChatService {
  private readonly _isAudio = signal<boolean>(false);
 
  readonly isAudioMode = computed(() => this._isAudio());
  readonly isTextMode  = computed(() => !this._isAudio());
 
  toggleInputMode(): void {
    this._isAudio.update(v => !v);
  }
 
  setAudioMode(): void { this._isAudio.set(true);  }
  setTextMode():  void { this._isAudio.set(false); }
}
