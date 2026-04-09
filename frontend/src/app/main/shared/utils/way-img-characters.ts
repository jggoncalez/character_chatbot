export const getWayImgCharacters = (agent : string) => {
    switch (agent) {
        case "inuyasha":
        case "Inuyasha":
            return "/assets/characters/inuyasha.webp";
        case "megumin":
        case "Megumin":
            return "/assets/characters/megumin.webp";
        case "Shadow the Hedgehog":
            return "/assets/characters/shadow.webp";
        case "goku":
        case "Goku":
            return "/assets/characters/goku.webp";
        default:
            return "https://placehold.co/400"
    }
} 