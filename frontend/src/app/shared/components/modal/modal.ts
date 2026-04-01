import { Component, computed, inject, signal, ViewEncapsulation } from '@angular/core';
import { ApiService } from '../../services/api-service';
import { IChatConfig } from '../../../features/pages/chatbot/interfaces/chat-config';
import { getWayImgCharacters } from '../../functions/way-img-characters';
import { getDescribeCharacters } from '../../functions/describe-characters';
import { getStyleCharacters } from '../../functions/style-characters';
import { Card } from '../card/card';
import { map } from 'rxjs';
import { toSignal } from '@angular/core/rxjs-interop';

@Component({
  selector: 'app-modal',
  imports: [Card],
  templateUrl: './modal.html',
  styleUrl: './modal.scss',
  encapsulation: ViewEncapsulation.None
})
export class Modal {
  apiService = inject(ApiService);

  cards = toSignal(
    this.apiService.getCharacters().pipe(
      map(data =>
        data.characters.map(name => ({
          agent: name,
          wayImg: getWayImgCharacters(name),
          describe: getDescribeCharacters(name),
          styleTheme: getStyleCharacters(name)
        } as IChatConfig))
      )
    ),
    { initialValue: [] as IChatConfig[] }  
  );
}

