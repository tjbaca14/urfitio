import axios from 'axios';
import type { ChatRequest, ChatResponse, Division, School } from './types';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatApi = {
  /**
   * Send a chat message and get a response
   */
  sendMessage: async (chatRequest: ChatRequest): Promise<ChatResponse> => {
    const { data } = await api.post<ChatResponse>('/chats', chatRequest);
    return data;
  },

  /**
   * Save a chat conversation to the database
   */
  saveChat: async (chatRequest: ChatRequest): Promise<ChatRequest> => {
    const { data } = await api.put<ChatRequest>(`/chats/${chatRequest.id}`, chatRequest);
    return data;
  },

  /**
   * Get chat history by ID
   */
  getChatHistory: async (chatId: string): Promise<ChatRequest> => {
    const { data } = await api.get<ChatRequest>(`/chats/${chatId}`);
    return data;
  },

  /**
   * Get all chat history for a user
   */
  getUserChatHistory: async (userId: string, limit = 10): Promise<ChatRequest[]> => {
    const { data } = await api.get<ChatRequest[]>(`/chats/user/${userId}`, {
      params: { limit },
    });
    return data;
  },
};

export const schoolsApi = {
  /**
   * Get all available divisions
   */
  getDivisions: async (): Promise<Division[]> => {
    const { data } = await api.get<Division[]>('/schools/divisions');
    return data;
  },

  /**
   * Get a single school by ID or name
   */
  getSchool: async (schoolId: string): Promise<School> => {
    const { data } = await api.get<School>(`/schools/${schoolId}`);
    return data;
  },

  /**
   * List schools with optional filters
   */
  listSchools: async (params?: {
    division?: string;
    name_contains?: string;
    limit?: number;
  }): Promise<School[]> => {
    const { data } = await api.get<School[]>('/schools', { params });
    return data;
  },

  /**
   * Get schools in a specific division (convenience method)
   */
  getSchoolsByDivision: async (division: string): Promise<School[]> => {
    const { data } = await api.get<School[]>('/schools', {
      params: { division },
    });
    return data;
  },
};
