export interface IPostResponse {
    id : string
    character : string
    text : string
    state : string
    created_at : string
    comments : IPostResponse[]
}
