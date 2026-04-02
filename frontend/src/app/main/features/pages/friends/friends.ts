import { Component, inject } from '@angular/core';
import { ThemeService } from '../../../shared/services/theme-service';

@Component({
  selector: 'app-friends',
  imports: [],
  templateUrl: './friends.html',
  styleUrl: './friends.scss',
})
export class Friends {
  themeService = inject(ThemeService);
  ias = [
    { nome: 'Aurora', cargo: 'Assistente Criativa', desc: 'Especializada em arte, design e criatividade', icon: '🎨' },
    { nome: 'Nexus', cargo: 'Analista de Dados', desc: 'Mestre em análise de dados e insights', icon: '📊' },
    { nome: 'Codex', cargo: 'Desenvolvedor', desc: 'Expert em programação e tecnologia', icon: '💻' },
    { nome: 'Sage', cargo: 'Filósofo', desc: 'Explorador de grandes ideias', icon: '🧠' },
    { nome: 'Luna', cargo: 'Guia', desc: 'Sua luz no caminho do conhecimento', icon: '✨' },
    { nome: 'Atlas', cargo: 'Geógrafo', desc: 'Conhecimento global ao seu alcance', icon: '🌍' }
  ];

}
