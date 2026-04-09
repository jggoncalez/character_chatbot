import { Injectable, signal } from '@angular/core';
import { IToastConfig } from '../interfaces/toast-config';

@Injectable({
  providedIn: 'root',
})
export class ToastService {
  private idCounter = 0;
  toasts = signal<IToastConfig[]>([]);

  show(message: string, style: 'success' | 'danger' | 'info', duration: number = 3000) {
    const id = this.idCounter++;
    const newToast: IToastConfig = {
      id,
      message,
      styleToast: style,
      duration
    };

    this.toasts.update(list => [...list, newToast]);

    setTimeout(() => {
      this.remove(id);
    }, duration);
  }

  remove(id: number) {
    this.toasts.update(list => list.filter(t => t.id !== id));
  }
}
