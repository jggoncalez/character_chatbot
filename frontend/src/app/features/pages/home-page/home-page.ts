import { Component } from '@angular/core';
import { Carousel } from '../../../shared/components/carousel/carousel';
import { ICardConfig } from '../../../shared/components/card/interfaces/card-config';

@Component({
  selector: 'app-home-page',
  imports: [Carousel],
  templateUrl: './home-page.html',
  styleUrl: './home-page.scss',
})
export class HomePage {
  cards : ICardConfig[] = [
    {
      wayAssetImg : "https://placehold.co/300",
      name : "card 1",
      describe : "lorem",
      wayCharcAi : ""
    },
    {
      wayAssetImg : "https://placehold.co/400",
      name : "card 2",
      describe : "lorem",
      wayCharcAi : ""
    },
    {
      wayAssetImg : "https://placehold.co/500",
      name : "card 3",
      describe : "lorem",
      wayCharcAi : ""
    },
    {
      wayAssetImg : "https://placehold.co/600",
      name : "card 4",
      describe : "lorem",
      wayCharcAi : ""
    }
  ]
}
