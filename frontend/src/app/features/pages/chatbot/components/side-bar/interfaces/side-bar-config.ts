import { IHistoryConfig } from "./history-config";


export interface ISideBarConfig {
    agent : string,
    favorites : IHistoryConfig[],
    historyChats : IHistoryConfig[]
}
