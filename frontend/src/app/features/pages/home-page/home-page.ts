import { Component, computed, inject, signal } from '@angular/core';
import { Carousel } from '../../../shared/components/carousel/carousel';
import { ActivatedRoute } from '@angular/router';
import { ICharactersResponse } from '../../../shared/interfaces/characters-response';
import { IChatConfig } from '../chatbot/interfaces/chat-config';
import { getWayImgCharacters } from '../../../shared/functions/way-img-characters';
import { getDescribeCharacters } from '../../../shared/functions/describe-characters';
import { getStyleCharacters } from '../../../shared/functions/style-characters';


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
      wayImg: getWayImgCharacters(name),
      describe: getDescribeCharacters(name),
      styleTheme : getStyleCharacters(name)
    } as IChatConfig));
  });
}
