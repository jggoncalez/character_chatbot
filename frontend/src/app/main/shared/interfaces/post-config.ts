export interface IPostConfig {
    id : string
    agent : string
    message : string
    state : string
    time : string
    comments : IPostConfig[]
}
