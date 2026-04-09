import { Component, computed, inject, input, signal } from '@angular/core';
import { ThemeService } from '../../../../../../services/theme-service';
import { ChatService } from '../../../../../../services/chat-service';
import { form, required, FormField, minLength, maxLength } from '@angular/forms/signals';
import { ApiService } from '../../../../../../services/api-service';
import { dtoAgentName } from '../../../../../../utils/dto-agent-name';

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
  agent = input.required<string>();
  characters = signal<string[]>([]);
  message = signal('');
  characterName = computed(() => 
  {
    if(this.agent() !== "Dra. Galastriceia Pantufa") {
      return dtoAgentName(this.agent(), (this.characters() as  any).characters)
    } else {
      return  "dra galastriceia pantufa"
    }
    
  }
    
  );
  loading = this.chatService.loading;
  constructor() {
    this.apiService.getCharactersNodetails().subscribe({
      next: (response) => this.characters.set(response.data)
    });
  }

  get isDark(): boolean {
    return this.themeService.getCurrentTheme() === 'dark';
  }

  input = form(this.message,(message) => {
    required(message,{message : "Não pode ser enviado sem adicionar um valor!"})
    maxLength(message,250,{message : "Máximo de caracteres atingido!"})
  })
  

  send(): void {
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

}
