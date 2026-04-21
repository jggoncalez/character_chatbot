import { inject, Injectable } from '@angular/core';
import { forkJoin, map, Observable, switchMap } from 'rxjs';
import { ICharactersResponse } from '../interfaces/characters-response';
import { IChatResponse } from '../interfaces/chat-response';
import { IChatRequest } from '../interfaces/chat-request';
import { IHistoryResponse } from '../interfaces/history-response';
import { HttpClient } from '@angular/common/http';
import { ICharacterConfig } from '../interfaces/character-config';
import { ICharacterResponse } from '../interfaces/character-response';
import { IPostConfig } from '../interfaces/post-config';
import { IPostResponse } from '../interfaces/post-response';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private http = inject(HttpClient);
  private baseUrl = 'http://127.0.0.1:8000';

  getCharacters(): Observable<ICharactersResponse> {
    return this.http.get<any>(`${this.baseUrl}/characters`).pipe(
      switchMap((data: ICharacterResponse) => {
        const requests = data.characters.map((value: string) => this.getDetails(value));
        return forkJoin(requests);
      }),
      map((characters: ICharacterConfig[]) => ({ characters }))
    );
  }

  private getDetails(agent: string): Observable<ICharacterConfig> {
    return this.http.get<any>(`${this.baseUrl}/character/${agent}/details`).pipe(
      map((data: any) => ({
        agent: data.name,
        personality: {
          traits : data.personality.traits,
          background : data.personality.background,
          speechStyle : data.personality.speech_style,
          weaknesses : data.personality.weaknesses,
          development : data.personality.development
        },
        age: data.age,
      } as ICharacterConfig))
    );
  }

  getCharactersNodetails(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/characters`).pipe(
      map((characters: []) => ({ data : characters }))
    );
  }

  sendMessage(message: string, character_name: string): Observable<IChatResponse[]> {
    const body: IChatRequest = { message, character_name };
    return this.http.post<IChatResponse[]>(`${this.baseUrl}/chat`, body);
  }

  getHistory(character_name: string): Observable<IHistoryResponse> {
    return this.http.get<IHistoryResponse>(`${this.baseUrl}/history/${character_name}`);
  }

  clearHistory(character_name : string) {
    return this.http.delete(`${this.baseUrl}/history/${character_name}/clear`).pipe(
      map(
        (data : any) => {
          return {
            message : data.message
          }
        }
      )
    )
  }

  geratingFeed() {
    return this.http.get(`${this.baseUrl}/feed`).pipe(
      map(
        (data : any) => {
          return data.posts.map((value : IPostResponse) => {
            return this.mapDto(value)
          })
        }
      )
    );
  }

  private mapDto(value : IPostResponse) : IPostConfig {
    return {
              id : value.id,
              agent : value.character,
              message : value.text,
              state : value.state,
              time : value.created_at,
              comments : value.comments?.map((valueData : any)=> this.mapDto(valueData)) ?? []
            } as IPostConfig
  }

  getFeed() {
    return this.http.get(`${this.baseUrl}/feed/cached`).pipe(
      map(
        (data : any) => {
          return data.posts.map((value : IPostResponse) => {
            return this.mapDto(value)
          })
        }
      )
    );
  }

  postCommentFeed(post_id : string, text : string) {
    const body = {post_id,text}
    return this.http.post(`${this.baseUrl}/feed/comment`,body).pipe(
      map(
        (_) => ({message : "Post atualizado com a resposta do personagem adicionada aos comentários."})
      )
    )
  }

  sendMessageAudio(character_name : string, body : any) {
    return this.http.post(`${this.baseUrl}/voice/${character_name}/transcribe`,body);
  }
  
  postFeedUser(text : string) {
    const body = {
      text : text
    }

    return this.http.post(`${this.baseUrl}/feed/post`,body).pipe(
      map(
        (value : any) => {
          return this.mapDto(value)
        }
      )
    )
  }
}
