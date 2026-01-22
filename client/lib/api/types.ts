export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface ChatRequest {
  id: string;
  userId: string;
  messages: Message[];
  contextKey?: string; // School name for context retrieval
  createdDate?: string;
}

export interface ChatResponse extends Message {
  // Response is just a Message from the assistant
}
export interface Division {
  id: string;
  division_type: string;
}

export interface School {
  id: string;
  name: string;
  division: string;
}
