type StyleTheme = {
    primaryColor : string,
    secundaryColor : string,
    configColor : string
}

export interface IChatConfig {
    name : string,
    describe : string,
    styleTheme : StyleTheme,
    wayImg : string
}
// Apenas para exemplo, pode ser alterado após a integração do backEnd