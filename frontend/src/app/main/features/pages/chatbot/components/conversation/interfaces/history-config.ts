import { IChatConfig } from "../../../interfaces/chat-config";
import { IMessage } from "./message-config";

export interface IHistoryConfig {
    id: string;
    config: IChatConfig;
    messages: IMessage[];
    createdAt: Date;
}
