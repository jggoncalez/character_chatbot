import { IHistoryMessages } from "./history-messages";

export interface IHistoryResponse {
  character: string;
  history: IHistoryMessages[];
}
