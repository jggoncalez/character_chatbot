import { Component, computed, input, signal } from '@angular/core';
import { getWayImgCharacters } from '../../utils/way-img-characters';

@Component({
  selector: 'app-agent-image',
  imports: [],
  templateUrl: './agent-image.html',
  styleUrl: './agent-image.scss',
})
export class AgentImage {
  agentName = input.required<string>();
  size = input<number>(36);
  imageError = signal<boolean>(false);
  imageSrc = computed(() => getWayImgCharacters(this.agentName()));
 
  fontSize = computed(() => +((this.size() / 36) * 0.85).toFixed(2));
 
  onImageError(): void {
    this.imageError.set(true);
  }
}
