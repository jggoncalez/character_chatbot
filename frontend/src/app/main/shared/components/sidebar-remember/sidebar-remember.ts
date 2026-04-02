import { Component, inject } from '@angular/core';
import { ThemeService } from '../../services/theme-service';

@Component({
  selector: 'app-sidebar-remember',
  imports: [],
  templateUrl: './sidebar-remember.html',
  styleUrl: './sidebar-remember.scss',
})
export class SidebarRemember {
  themeService = inject(ThemeService);
  iasOnline = [
    { nome: 'Aurora', cargo: 'Assistente Criativa', icon: 'bi-lightbulb-fill', color: 'bg-warning' },
    { nome: 'Nexus', cargo: 'Analista de Dados', icon: 'bi-bar-chart-fill', color: 'bg-info' },
    { nome: 'Codex', cargo: 'Desenvolvedor', icon: 'bi-code-slash', color: 'bg-dark', text: 'text-success' },
    { nome: 'Luna', cargo: 'Poeta', icon: 'bi-stars', color: 'bg-primary' },
    { nome: 'Melody', cargo: 'Musicista', icon: 'bi-music-note-beamed', color: '', customColor: '#6f42c1' },
    { nome: 'Nova', cargo: 'Cientista', icon: 'bi-rocket-fill', color: 'bg-danger' }
  ];
}
