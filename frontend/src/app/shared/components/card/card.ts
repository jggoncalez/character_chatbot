import { Component, input } from '@angular/core';
import { ICardConfig } from './interfaces/card-config';

@Component({
  selector: 'app-card',
  imports: [],
  templateUrl: './card.html',
  styleUrl: './card.scss',
})
export class Card {
  cardConfig = input<ICardConfig>();
}
