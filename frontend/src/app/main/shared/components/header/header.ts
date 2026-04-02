import { Component, inject } from '@angular/core';
import { ThemeService } from '../../services/theme-service';

@Component({
  selector: 'app-header',
  imports: [],
  templateUrl: './header.html',
  styleUrl: './header.scss',
})
export class Header {
  themeService = inject(ThemeService);
}
