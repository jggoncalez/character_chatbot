import { inject } from '@angular/core';
import { Router, Routes } from '@angular/router';
import { EMPTY, of } from 'rxjs';
import { Main } from './main/main';
import { authGuard } from './main/shared/guards/auth.guard';
import { characterDataResolver } from './main/features/pages/profile-ia/route/character-data-resolver';
import { AboutUs } from './main/features/pages/about-us/about-us';


export const routes: Routes = [
    {
        path : "",
        component : Main,
        canActivate : [authGuard],
        children: [
            {
                path : "home",
                component : AboutUs
            },
            {
                path: "feed",
                loadComponent : () => import("./main/features/pages/feed/feed").then(m=> m.Feed)
            },
            {
                path: "friends",
                loadComponent : () => import("./main/features/pages/friends/friends").then(m=> m.Friends)
            },
            {
                path : "profile",
                loadComponent : () => import("./main/features/pages/profile/profile").then(m => m.Profile)
            },
            {
                path : "settings",
                loadComponent : () => import("./main/features/pages/settings/settings").then(m => m.Settings)
            },
            {
                path : "profileIA/:agent",
                loadComponent : () => import("./main/features/pages/profile-ia/profile-ia").then(m => m.ProfileIA),
                resolve : { characterData: characterDataResolver }
            },
            {
                path : "",
                redirectTo : "home",
                pathMatch : "full"
            }
        ]
    },
    {
        path : "**",
        redirectTo : ""
    }
];
