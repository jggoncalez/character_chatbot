import { Component } from '@angular/core';
import { Carousel } from '../../../shared/components/carousel/carousel';
import { IChatConfig } from '../chatbot/interfaces/chat-config';


@Component({
  selector: 'app-home-page',
  imports: [Carousel],
  templateUrl: './home-page.html',
  styleUrl: './home-page.scss',
})
export class HomePage {
  cards : IChatConfig[] = [
    {
      wayImg : "https://placehold.co/400",
      agent : "card 2",
      describe : "lorem"
    },
    {
      wayImg : "https://placehold.co/300",
      agent : "Steve",
      describe : "Em Busca de Diamantes"
    },
    {
      wayImg : "https://placehold.co/500",
      agent : "card 3",
      describe : "lorem"
    },
    {
      wayImg : "https://placehold.co/600",
      agent : "card 4",
      describe : "lorem"
    }
  ]
}
