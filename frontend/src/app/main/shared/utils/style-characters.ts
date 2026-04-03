export const getStyleCharacters = (agent: string) => {
    switch (agent) {
        case "Inuyasha":
            return {
                primaryColor: '#C82B2B',   
                secundaryColor: '#2B2B36', 
                configColor: '#16161E'
            };
        case "Megumin":
            return {
                primaryColor: '#FF4500',   
                secundaryColor: '#3A1E1E',
                configColor: '#1A0F0D'
            };
        case "Shadow":
            return {
                primaryColor: '#E50000',
                secundaryColor: '#252525',
                configColor: '#121212'
            };
        case "Goku":
            return {
                primaryColor: '#FF6600',   
                secundaryColor: '#1C2938', 
                configColor: '#0B131E'     
            };
        default:
            return {
                primaryColor: '#0D6EFD',   
                secundaryColor: '#212529', 
                configColor: '#121212'     
            };
    }
}