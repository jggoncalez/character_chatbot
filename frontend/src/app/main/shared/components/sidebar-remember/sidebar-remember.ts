import { Component, computed, inject } from '@angular/core';
import { ThemeService } from '../../services/theme-service';
import { SavePostsService } from '../../services/save-posts-service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sidebar-remember',
  imports: [],
  templateUrl: './sidebar-remember.html',
  styleUrl: './sidebar-remember.scss',
})
export class SidebarRemember {
  router = inject(Router);
  themeService = inject(ThemeService);
  savePostsService = inject(SavePostsService);
  saveIA = computed(() => this.savePostsService.getAll())

  seeProfile(agent : string) {
    this.router.navigate(["profileIA",agent]);
  }

}
