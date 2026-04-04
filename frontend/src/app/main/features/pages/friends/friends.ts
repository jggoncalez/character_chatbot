import { Component, computed, inject, signal } from '@angular/core';
import { ThemeService } from '../../../shared/services/theme-service';
import { ApiService } from '../../../shared/services/api-service';
import { ICharacterConfig } from '../../../shared/interfaces/character-config';
import { Router } from '@angular/router';

@Component({
  selector: 'app-friends',
  imports: [],
  templateUrl: './friends.html',
  styleUrl: './friends.scss',
})
export class Friends {
  themeService = inject(ThemeService);
  router = inject(Router);
  apiService = inject(ApiService);

  configs = signal<ICharacterConfig[]>([]);

  agentsConfig = computed(() => this.configs())

  constructor() {
    this.loadingIAs();
  }

  loadingIAs() {
    this.apiService.getCharacters().subscribe({
      next : (value) => {
        this.configs.set(value.characters)
      }
    })
  }

  seeProfile(agent : string) {
    this.router.navigate(["profileIA",agent]);
  }
}
