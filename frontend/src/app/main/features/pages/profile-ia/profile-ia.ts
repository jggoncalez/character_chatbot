import { Component, computed, inject, signal, WritableSignal } from '@angular/core';
import { ThemeService } from '../../../shared/services/theme-service';
import { ICharacterConfig } from '../../../shared/interfaces/character-config';
import { ActivatedRoute } from '@angular/router';
import { toSignal } from '@angular/core/rxjs-interop';
import { SavePostsService } from '../../../shared/services/save-posts-service';

@Component({
  selector: 'app-profile-ia',
  imports: [],
  templateUrl: './profile-ia.html',
  styleUrl: './profile-ia.scss',
})
export class ProfileIA {
  route = inject(ActivatedRoute);
  themeService = inject(ThemeService);
  savePostsService = inject(SavePostsService);

  private routeData = toSignal(this.route.data);

  agentConfig = computed(() => this.routeData()?.['characterData'] as ICharacterConfig ?? null);

  get isDark(): boolean {
    return this.themeService.getCurrentTheme() === 'dark';
  }

  isSaved = computed(() =>
    this.savePostsService.isSaved(this.agentConfig()?.agent ?? '')()
  );

  onSave() {
    const config = this.agentConfig();
    if (!config) return;
    this.isSaved() ? this.savePostsService.remove(config.agent) : this.savePostsService.save(config);
  }
}
