import { NgClass } from '@angular/common';
import { Component, inject } from '@angular/core';
import { ThemeService } from '../../../shared/services/theme-service';
import { ApiService } from '../../../shared/services/api-service';
import { SavePostsService } from '../../../shared/services/save-posts-service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-profile',
  imports: [NgClass],
  templateUrl: './profile.html',
  styleUrl: './profile.scss',
})
export class Profile {
  apiService = inject(ApiService);
  themeService = inject(ThemeService);
  savePostsService = inject(SavePostsService);
  router = inject(Router);

  get isDark(): boolean {
    return this.themeService.getCurrentTheme() === 'dark';
  }
  

  seeProfile(agent : string) {
    this.router.navigate(["profileIA",agent]);
  }
  
}
