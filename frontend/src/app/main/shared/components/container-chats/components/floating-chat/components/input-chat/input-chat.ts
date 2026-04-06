import { Component, inject, input, signal } from '@angular/core';
import { ThemeService } from '../../../../../../services/theme-service';
import { ChatService } from '../../../../../../services/chat-service';
import { form, required, FormField, minLength, maxLength } from '@angular/forms/signals';

@Component({
  selector: 'app-input-chat',
  imports: [FormField],
  templateUrl: './input-chat.html',
  styleUrl: './input-chat.scss',
})
export class InputChat {
  themeService = inject(ThemeService);
  chatService = inject(ChatService);
  agent = input.required<string>();
  get isDark(): boolean {
    return this.themeService.getCurrentTheme() === 'dark';
  }


  message = signal('');
  input = form(this.message,(message) => {
    required(message,{message : "Não pode ser enviado sem adicionar um valor!"})
    maxLength(message,250,{message : "Máximo de caracteres atingido!"})
  })
  loading = this.chatService.loading;

  send(): void {
    const text = this.message().trim();
    if (!text) return;
    this.chatService.sendMessage(text, this.agent());
    this.message.set('');
  }

  onKeyDown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.send();
    }
  }

}
