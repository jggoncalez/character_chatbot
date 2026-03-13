import { Component, signal, WritableSignal } from '@angular/core';
import { IChatConfig } from './interfaces/chat-config';

@Component({
  selector: 'app-chatbot',
  imports: [],
  templateUrl: './chatbot.html',
  styleUrl: './chatbot.scss',
})
export class Chatbot {
  chatConfig : WritableSignal<IChatConfig> = signal<IChatConfig>({
    name : "Steve",
    describe : "Em busca de Diamantes",
    styleTheme : "#adadfd",
    wayImg : "https://placehold.co/40"
  })
}
