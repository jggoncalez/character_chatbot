type Links = {
    linkedin? : string,
    github? : string
}

export interface ITeamConfig {
    fullName : string,
    wayImg : string,
    role : string,
    describe : string,
    links : Links
}
