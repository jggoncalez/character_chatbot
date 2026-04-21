import { Component, computed, inject, input, signal } from '@angular/core';
import { ThemeService } from '../../../../../../services/theme-service';
import { ChatService } from '../../../../../../services/chat-service';
import { form, required, FormField, minLength, maxLength } from '@angular/forms/signals';
import { ApiService } from '../../../../../../services/api-service';
import { dtoAgentName } from '../../../../../../utils/dto-agent-name';
import { InputChatService } from './service/input-chat-service';
import { ToastService } from '../../../../../../components/toast-messages/services/toast-service';

@Component({
  selector: 'app-input-chat',
  imports: [FormField],
  templateUrl: './input-chat.html',
  styleUrl: './input-chat.scss',
})
export class InputChat {
  apiService = inject(ApiService);
  themeService = inject(ThemeService);
  chatService = inject(ChatService);
  inputChatService = inject(InputChatService);
  private toastService = inject(ToastService);

  agent = input.required<string>();
  characters = signal<string[]>([]);
  message = signal('');
  dropdownOpen = signal<boolean>(false);
  characterName = computed(() => {
    if(this.agent() !== "Dra. Galastriceia Pantufa") {
      return dtoAgentName(this.agent(), (this.characters() as any).characters)
    } else {
      return "dra galastriceia pantufa"
    }
  });

  loading = this.chatService.loading;

  isAudioMode = this.inputChatService.isAudioMode;
  isTextMode  = this.inputChatService.isTextMode;

  private mediaRecorder: MediaRecorder | null = null;
  private audioChunks: Blob[] = [];
  isRecording = signal<boolean>(false);

  constructor() {
    this.apiService.getCharactersNodetails().subscribe({
      next: (response) => this.characters.set(response.data)
    });
  }

  get isDark(): boolean {
    return this.themeService.getCurrentTheme() === 'dark';
  }

  input = form(this.message, (message) => {
    required(message, { message: "Não pode ser enviado sem adicionar um valor!" })
    maxLength(message, 250, { message: "Máximo de caracteres atingido!" })
  })

  send(): void {
    if (!this.characterName()) return;
    const text = this.message().trim();
    if (!text) return;
    this.chatService.sendMessage(text, this.characterName());
    this.message.set('');
  }

  onKeyDown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.send();
    }
  }


  async startRecording(): Promise<void> {
    if (!this.characterName()) return;
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      this.audioChunks = [];
      this.mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm;codecs=opus' });

      this.mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) this.audioChunks.push(e.data);
      };

      this.mediaRecorder.onstop = () => {
        const blob = new Blob(this.audioChunks, { type: 'audio/webm;codecs=opus' });
        this.sendAudio(blob);
        stream.getTracks().forEach(t => t.stop());
      };

      this.mediaRecorder.start();
      this.isRecording.set(true);
    } catch {
      this.isRecording.set(false);
      this.toastService.show('Não foi possível acessar o microfone. Verifique as permissões.', 'danger', 4000);
    }
  }

  stopRecording(): void {
    this.mediaRecorder?.stop();
    this.isRecording.set(false);
  }

  private sendAudio(blob: Blob): void {
    const formData = new FormData();
    formData.append('audio', blob, 'recording.webm');

    this.chatService.sendMessageAudio(formData, this.characterName());
  }
}
