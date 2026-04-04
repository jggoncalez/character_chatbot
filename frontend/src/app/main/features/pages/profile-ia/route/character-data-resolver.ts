import { ResolveFn, Router } from "@angular/router";
import { ApiService } from "../../../../shared/services/api-service";
import { inject } from "@angular/core";
import { ICharacterConfig } from "../../../../shared/interfaces/character-config";
import { ICharactersResponse } from "../../../../shared/interfaces/characters-response";
import { filter, map, tap } from "rxjs";

export const characterDataResolver : ResolveFn<ICharacterConfig> = (route,_state) => {
    const apiService = inject(ApiService);
    const router = inject(Router);
    const agent = route.paramMap.get("agent");

    return apiService.getCharacters().pipe(
        map((data: ICharactersResponse) =>
        data.characters.find((c) => c.agent === agent)
        ),
        tap((character) => {
        if (!character) router.navigate(['/feed']);
        }),
        filter((character): character is ICharacterConfig => !!character)
    );
}