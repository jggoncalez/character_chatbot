export const resolveErrorMessage = (error: any): string => {
    const status = error?.status;
    switch (status) {
        case 404:
        return '⚠️ Personagem não encontrado. Verifique se o personagem está disponível.';
        case 500:
        return '⚠️ Infelizmente não foi possível concluir a mensagem. O serviço está temporariamente indisponível. Tente novamente.';
        case 0:
        return '⚠️ Sem conexão com o servidor. Verifique sua rede e tente novamente.';
        default:
        return '⚠️ Infelizmente não foi possível concluir a mensagem. Tente novamente.';
    }
}
 
export const resolveAudioErrorMessage = (error: any): string => {
    const status = error?.status;
    switch (status) {
        case 404:
        return '⚠️ Personagem não encontrado para processar o áudio.';
        case 413:
        return '⚠️ Áudio muito longo. O arquivo excede o limite de 1 MB. Grave uma mensagem mais curta.';
        case 415:
        return '⚠️ Formato de áudio não suportado. Tente gravar novamente.';
        case 422:
        return '⚠️ Não foi possível transcrever o áudio. Fale mais claramente e tente novamente.';
        case 500:
        return '⚠️ Infelizmente não foi possível concluir a transcrição do áudio. Tente novamente.';
        case 0:
        return '⚠️ Sem conexão com o servidor. Verifique sua rede e tente novamente.';
        default:
        return '⚠️ Infelizmente não foi possível processar o áudio. Tente novamente.';
    }
}