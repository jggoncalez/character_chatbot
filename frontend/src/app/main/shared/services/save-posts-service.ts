import { computed, Injectable, signal } from '@angular/core';
import { ICharacterConfig } from '../interfaces/character-config';

@Injectable({
  providedIn: 'root',
})
export class SavePostsService {
  private readonly STORAGE_KEY = 'saved_agents';

  private savedAgents = signal<ICharacterConfig[]>(this.loadFromStorage());

  getAll = computed(() => this.savedAgents());

  isSaved = (agent: string) => computed(() =>
    this.savedAgents().some((c) => c.agent === agent)
  );

  save(character: ICharacterConfig) {
    if (this.isSaved(character.agent)()) return;
    const updated = [...this.savedAgents(), character];
    this.savedAgents.set(updated);
    this.persistToStorage(updated);
  }

  remove(agent: string) {
    const updated = this.savedAgents().filter((c) => c.agent !== agent);
    this.savedAgents.set(updated);
    this.persistToStorage(updated);
  }

  private loadFromStorage(): ICharacterConfig[] {
    try {
      const raw = localStorage.getItem(this.STORAGE_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  }

  private persistToStorage(data: ICharacterConfig[]) {
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(data));
  }
}
