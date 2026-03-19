import { Component, computed, inject, signal } from '@angular/core';
import { Carousel } from '../../../shared/components/carousel/carousel';
import { ActivatedRoute } from '@angular/router';
import { ICharactersResponse } from '../../../shared/interfaces/characters-response';
import { IChatConfig } from '../chatbot/interfaces/chat-config';


@Component({
  selector: 'app-home-page',
  imports: [Carousel],
  templateUrl: './home-page.html',
  styleUrl: './home-page.scss',
})
export class HomePage {
  private route = inject(ActivatedRoute);

  cards = computed(() => {
    const res = this.route.snapshot.data['characters'] as ICharactersResponse;
    return res.characters.map(name => ({
      agent: name,
      wayImg: '',
      describe: ''
    } as IChatConfig));
  });
}
