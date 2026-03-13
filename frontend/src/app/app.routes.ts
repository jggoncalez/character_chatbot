import { Routes } from '@angular/router';

export const routes: Routes = [
    {
        path: "",
        loadComponent: () => import("./features/pages/home-page/home-page").then(m => m.HomePage)
    },
    {
        path : "chat",
        loadComponent: () => import("./features/pages/chatbot/chatbot").then(m => m.Chatbot)
    }
];
