import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ChatService } from './chat.service';

interface ChatMessage {
  role: 'user' | 'bot';
  text: string;
  usedTool?: boolean;
}

@Component({
  selector: 'app-root',
  imports: [FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  private chatService = inject(ChatService);

  messages = signal<ChatMessage[]>([
    { role: 'bot', text: 'سلام! من چت‌بات آموزشی هستم. بپرس، یا بگو مقاله جدید پیدا کنم.' },
  ]);
  input = signal('');
  loading = signal(false);
  tokens = signal(0);
  maxTokens = signal(4000);
  sessionId: string | null = null;

  // درصد پر شدن توکن‌ها، برای نوار بالای صفحه
  tokenPercent(): number {
    if (this.maxTokens() === 0) return 0;
    return Math.min(100, Math.round((this.tokens() / this.maxTokens()) * 100));
  }

  send() {
    const text = this.input().trim();
    if (!text || this.loading()) return;

    this.messages.update((list) => [...list, { role: 'user', text }]);
    this.input.set('');
    this.loading.set(true);

    this.chatService.send(text, this.sessionId).subscribe({
      next: (res) => {
        this.sessionId = res.session_id;
        this.tokens.set(res.tokens);
        this.maxTokens.set(res.max_tokens);
        this.messages.update((list) => [
          ...list,
          { role: 'bot', text: res.reply, usedTool: res.used_tool },
        ]);
        this.loading.set(false);
      },
      error: () => {
        this.messages.update((list) => [
          ...list,
          { role: 'bot', text: 'خطا: اول API پایتون را اجرا کن: uvicorn api:app --reload --port 8000' },
        ]);
        this.loading.set(false);
      },
    });
  }

  askExample() {
    this.input.set('مقاله جدید درباره هوش مصنوعی در پزشکی پیدا کن');
    this.send();
  }
}
