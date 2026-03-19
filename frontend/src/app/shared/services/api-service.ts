import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ICharactersResponse } from '../interfaces/characters-response';
import { IChatResponse } from '../interfaces/chat-response';
import { IChatRequest } from '../interfaces/chat-request';
import { IHistoryResponse } from '../interfaces/history-response';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private http = inject(HttpClient);
  private baseUrl = 'http://127.0.0.1:8000';

  getCharacters(): Observable<ICharactersResponse> {
    return this.http.get<ICharactersResponse>(`${this.baseUrl}/characters`);
  }

  sendMessage(message: string, character_name: string): Observable<IChatResponse[]> {
    const body: IChatRequest = { message, character_name };
    return this.http.post<IChatResponse[]>(`${this.baseUrl}/chat`, body);
  }

  getHistory(character_name: string): Observable<IHistoryResponse> {
    return this.http.get<IHistoryResponse>(`${this.baseUrl}/history/${character_name}`);
  }
}
