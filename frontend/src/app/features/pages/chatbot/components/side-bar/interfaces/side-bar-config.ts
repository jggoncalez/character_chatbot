import { IChatConfig } from "../../../interfaces/chat-config";

export interface ISideBarConfig {
    agentId : string,
    favorites : IChatConfig[],
    historyChats : IChatConfig[]
}
