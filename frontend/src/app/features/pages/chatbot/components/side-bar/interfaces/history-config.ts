import { IChatConfig } from "../../../interfaces/chat-config";
import { IMessage } from "./message-config";

export interface IHistoryConfig {
    messages: IMessage[],
    config: IChatConfig
}
