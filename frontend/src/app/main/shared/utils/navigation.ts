import { inject } from "@angular/core"
import { Router } from "@angular/router"

export function onNavigate(path : string) {
    const router = inject(Router);
    router.navigate(['/', path])
}