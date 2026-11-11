import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ChatReply {
  reply: string;
  session_id: string;
  tokens: number;
  max_tokens: number;
  used_tool: boolean;
}

@Injectable({ providedIn: 'root' })
export class ChatService {
  private http = inject(HttpClient);
  // آدرس API پایتون (FastAPI روی پورت 8000)
  private apiUrl = 'http://localhost:8000/api/chat';

  send(message: string, sessionId: string | null): Observable<ChatReply> {
    return this.http.post<ChatReply>(this.apiUrl, {
      message,
      session_id: sessionId,
    });
  }
}
