import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Message } from '@/lib/api';

interface ChatState {
  // Current conversation
  currentChatId: string | null;
  messages: Message[];

  // UI state
  input: string;

  // Context selection
  selectedDivision: string | null;
  selectedSchool: string | null;

  // Actions
  setCurrentChatId: (id: string | null) => void;
  addMessage: (message: Message) => void;
  setMessages: (messages: Message[]) => void;
  clearMessages: () => void;
  setInput: (input: string) => void;
  setSelectedDivision: (division: string | null) => void;
  setSelectedSchool: (school: string | null) => void;
  reset: () => void;
}

export const useChatStore = create<ChatState>()(
  persist(
    (set) => ({
      // Initial state
      currentChatId: null,
      messages: [],
      input: '',
      selectedDivision: null,
      selectedSchool: null,

      // Actions
      setCurrentChatId: (id) => set({ currentChatId: id }),

      addMessage: (message) =>
        set((state) => ({ messages: [...state.messages, message] })),

      setMessages: (messages) => set({ messages }),

      clearMessages: () => set({ messages: [] }),

      setInput: (input) => set({ input }),

      setSelectedDivision: (division) =>
        set({
          selectedDivision: division,
          // Reset school when division changes
          selectedSchool: null,
        }),

      setSelectedSchool: (school) => set({ selectedSchool: school }),

      reset: () =>
        set({
          messages: [],
          input: '',
          currentChatId: null,
        }),
    }),
    {
      name: 'chat-storage',
      // Only persist certain fields
      partialize: (state) => ({
        currentChatId: state.currentChatId,
        selectedDivision: state.selectedDivision,
        selectedSchool: state.selectedSchool,
      }),
    }
  )
);
