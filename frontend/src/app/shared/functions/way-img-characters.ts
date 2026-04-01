export const getWayImgCharacters = (agent : string) => {
    switch (agent) {
        case "Inuyasha":
            return "/assets/characters/inuyasha.webp";
        case "Megumin":
            return "/assets/characters/megumin.webp";
        case "Shadow":
            return "/assets/characters/shadow.webp";
        case "Goku":
            return "/assets/characters/goku.webp";
        default:
            return "https://placehold.co/400"
    }
} 