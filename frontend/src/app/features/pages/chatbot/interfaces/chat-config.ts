export type StyleTheme = {
    primaryColor : string,
    secundaryColor : string,
    configColor : string
}

export interface IChatConfig {
    agent : string,
    describe : string,
    styleTheme? : StyleTheme,
    wayImg : string
}