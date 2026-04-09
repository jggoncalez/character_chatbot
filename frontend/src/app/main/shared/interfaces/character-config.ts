import { IPersonalityConfig } from "./personality-config"

export interface ICharacterConfig {
    agent : string
    personality : IPersonalityConfig
    age : string
}
