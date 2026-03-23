export const getDescribeCharacters = (agent : string) => {
    switch (agent) {
        case "Inuyasha":
            return "Hanyou (meio-youkai, meio-humano) rejeitado tanto por humanos quanto por youkais. Desenvolveu obsessão por ficar mais forte após infância solitária e dolorosa. Foi traído e lacrado por 50 anos, ficando amargurado.";
        case "Megumin":
            return "Prodígio Demônio Carmesim de uma família pobre. Se apaixonou por Magia de Explosão depois de ser salva por ela. Dedicou anos estudando para dominar o feitiço, ignorando seus deméritos. Aprendeu a se sustentar desde jovem.";
        case "Shadow":
            return "Forma de Vida Suprema criada pelo Professor Gerald Robotnik na Colônia Espacial ARK há 50 anos. Cresceu com Maria Robotnik, sua única amiga. Capturado por GUN após a morte de Maria. Traumatizado, buscava vingança mas eventualmente aceitou sua promessa a Maria de proteger o planeta.";
        case "Goku":
            return "Saiyajin enviado à Terra com missão de destruição, mas um acidente de infância apagou sua memória. Criado por seu avô adotivo Gohan com pureza de coração. Treinou desde criança com mestres marciais. Tornou-se o maior defensor da Terra e líder informal dos Guerreiros Z."
        default:
            return "https://placehold.co/400"
    }
}