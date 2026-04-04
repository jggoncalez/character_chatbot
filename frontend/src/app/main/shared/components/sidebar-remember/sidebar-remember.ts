import { Component, inject } from '@angular/core';
import { ThemeService } from '../../services/theme-service';
import { SavePostsService } from '../../services/save-posts-service';

@Component({
  selector: 'app-sidebar-remember',
  imports: [],
  templateUrl: './sidebar-remember.html',
  styleUrl: './sidebar-remember.scss',
})
export class SidebarRemember {
  themeService = inject(ThemeService);
  savePostsService = inject(SavePostsService);
  saveIA = this.savePostsService.getAll()
}
