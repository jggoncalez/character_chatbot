import { Component, computed, inject, input, signal } from '@angular/core';
import { getWayImgCharacters } from '../../utils/way-img-characters';
import { ApiService } from '../../services/api-service';
import { dtoAgentName } from '../../utils/dto-agent-name';

@Component({
  selector: 'app-agent-image',
  imports: [],
  templateUrl: './agent-image.html',
  styleUrl: './agent-image.scss',
})
export class AgentImage {
  apiService = inject(ApiService);
  characters = signal<string[]>([]);
  agentName = input.required<string>();
  size = input<number>(36);
  imageError = signal<boolean>(false);

  characterName = computed(() => 
    dtoAgentName(this.agentName(), (this.characters() as  any).characters)
  );
  imageSrc = computed(() => getWayImgCharacters(this.characterName()));
 
  fontSize = computed(() => +((this.size() / 36) * 0.85).toFixed(2));

  constructor() {
    this.apiService.getCharactersNodetails().subscribe({
      next: (response) => this.characters.set(response.data)
    });
  }
 
  onImageError(): void {
    this.imageError.set(true);
  }
}

