import { Component } from '@angular/core';
import { FloatingChat } from './components/floating-chat/floating-chat';

@Component({
  selector: 'app-container-chats',
  imports: [FloatingChat],
  templateUrl: './container-chats.html',
  styleUrl: './container-chats.scss',
})
export class ContainerChats {}
