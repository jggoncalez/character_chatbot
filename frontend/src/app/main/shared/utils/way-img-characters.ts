
export const getWayImgCharacters = (agent: string) => {

    switch (agent.toLowerCase()) {
        case "abri":
            return "/assets/characters/abri.webp";
        case "corretor rodrigo":
        case "corretor_rodrigo":
            return "/assets/characters/corretor_rodrigo.webp";
        case "dra. galastriceia pantufa":
        case "dra_galastriceia_pantufa":
            return "/assets/characters/dra_galastriceia_pantufa.webp";
        case "goku":
            return "/assets/characters/goku.webp";
        case "hiromi higuruma":
        case "hiromi_higuruma":
            return "/assets/characters/higuruma_hiromi.webp";
        case "inuyasha":
            return "/assets/characters/inuyasha.webp";
        case "megumin":
            return "/assets/characters/megumin.webp";
        case "pixxie":
            return "/assets/characters/pixxie.webp";
        case "professor elcio veras":
        case "professor_elcio_veras":
            return "/assets/characters/professor_elcio_veras.webp";
        case "shadow":
            return "/assets/characters/shadow.webp";
        case "tux":
            return "/assets/characters/tux.webp";
        default:
            return "https://placehold.co/400";
    }
};