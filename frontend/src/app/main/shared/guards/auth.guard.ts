import { CanActivateFn } from "@angular/router";

export const authGuard : CanActivateFn = (_route, _state ) => {
    // Futuramente injetar a api de login aqui

    return true;

}