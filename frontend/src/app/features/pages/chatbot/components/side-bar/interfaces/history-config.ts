import { IChatConfig } from "../../../interfaces/chat-config";
import { IMessageConfig } from "./message-config";

export interface IHistoryConfig {
    messages: IMessageConfig,
    config: IChatConfig
}
