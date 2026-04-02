import { ItoastStyleConfig } from "./toast-style-config";

export interface IToastConfig {
    id : number,
    message : string,
    styleToast : ItoastStyleConfig,
    duration : number
}
