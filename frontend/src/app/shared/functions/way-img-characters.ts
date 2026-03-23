export const getWayImgCharacters = (agent : string) => {
    switch (agent) {
        case "Inuyasha":
            return "/assets/characters/inuyasha.jpg";
        case "Megumin":
            return "/assets/characters/megumin.png";
        case "Shadow":
            return "/assets/characters/shadow.webp";
        case "Goku":
            return "/assets/characters/goku.webp";
        default:
            return "https://placehold.co/400"
    }
} 