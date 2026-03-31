import { inject } from '@angular/core';
import { Router, Routes } from '@angular/router';
import { EMPTY, of } from 'rxjs';
import { ConversationService } from './features/pages/chatbot/components/conversation/services/conversation-service';

export const routes: Routes = [
    {
        path: '',
        loadComponent: () => import('./features/pages/home-page/home-page').then(m => m.HomePage)
    },
    {
        path: 'chat',
        loadComponent: () => import('./features/pages/chatbot/chatbot').then(m => m.Chatbot),
        resolve: {
            config: () => {
            const conversationService = inject(ConversationService);
            const router = inject(Router);

            if (!conversationService.currentChat()) {
                router.navigate(['']);
                return EMPTY;
            }

            return of(conversationService.currentChat());
            }
        }
    },
    {
        path: 'about-us',
        loadComponent: () => import('./features/pages/about-us/about-us').then(m => m.AboutUs)
    }
];
