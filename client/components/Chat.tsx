'use client';

import { useEffect, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { useChatStore } from '@/stores/useChatStore';
import { useSendMessage, useDivisions, useSchools, useSaveChat } from '@/hooks/useChat';
import type { Message } from '@/lib/api';

export function Chat() {
  const {
    messages,
    input,
    selectedDivision,
    selectedSchool,
    addMessage,
    setInput,
    setSelectedDivision,
    setSelectedSchool,
    currentChatId,
    setCurrentChatId,
  } = useChatStore();

  const { mutate: sendMessage, isPending: isSending } = useSendMessage();
  const { data: divisions, isLoading: loadingDivisions } = useDivisions();
  const { data: schools, isLoading: loadingSchools } = useSchools(selectedDivision);
  const { mutate: saveChat } = useSaveChat();

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isSending) return;

    // Create user message
    const userMessage: Message = {
      role: 'user',
      content: input.trim(),
    };

    // Add to local state immediately (optimistic update)
    addMessage(userMessage);

    // Generate or reuse chat ID
    const chatId = currentChatId || uuidv4();
    if (!currentChatId) {
      setCurrentChatId(chatId);
    }

    // Prepare chat request
    const chatRequest = {
      id: chatId,
      userId: 'user-123', // TODO: Replace with actual user ID from auth
      messages: [...messages, userMessage],
      contextQuery: selectedSchool || undefined,
    };

    // Clear input immediately
    setInput('');

    // Send message - mutation will handle success/error
    sendMessage(chatRequest, {
      onSuccess: (responseMessage) => {
        // Add assistant's response to local state
        addMessage(responseMessage);

        // Save the full conversation to backend
        saveChat({
          ...chatRequest,
          messages: [...chatRequest.messages, responseMessage],
        });
      },
      onError: (error) => {
        console.error('Error sending message:', error);
        // TODO: Show error toast/notification to user
        // Optionally: Remove the optimistic user message on error
      },
    });
  };

  return (
    <div className="flex flex-col h-screen max-w-6xl mx-auto bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header with Context Selection */}
      <div className="p-6 border-b border-slate-700 bg-slate-800/50 backdrop-blur-sm">
        <h1 className="text-3xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">
          UrFit.io Chat
        </h1>
        <div className="flex gap-4">
          <div className="flex-1">
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Division
            </label>
            <select
              value={selectedDivision || ''}
              onChange={(e) => setSelectedDivision(e.target.value || null)}
              disabled={loadingDivisions}
              className="w-full bg-slate-700 border border-slate-600 text-slate-100 rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50 transition-all"
            >
              <option value="">Select Division</option>
              {divisions?.map((div) => (
                <option key={div.id} value={div.id}>
                  {div.division_type}
                </option>
              ))}
            </select>
          </div>

          <div className="flex-1">
            <label className="block text-sm font-medium text-slate-300 mb-2">
              School
            </label>
            <select
              value={selectedSchool || ''}
              onChange={(e) => setSelectedSchool(e.target.value || null)}
              disabled={!selectedDivision || loadingSchools}
              className="w-full bg-slate-700 border border-slate-600 text-slate-100 rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50 transition-all"
            >
              <option value="">Select School</option>
              {schools?.map((school) => (
                <option key={school.id} value={school.name}>
                  {school.name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 bg-slate-900">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="mb-4 text-6xl">💬</div>
              <p className="text-2xl font-semibold mb-2 text-slate-200">Welcome to UrFit.io!</p>
              <p className="text-slate-400">
                Select a division and school to get started.
              </p>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[70%] rounded-2xl px-5 py-3 shadow-lg ${
                    msg.role === 'user'
                      ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white'
                      : 'bg-slate-800 border border-slate-700 text-slate-100'
                  }`}
                >
                  <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                </div>
              </div>
            ))}

            {/* Loading indicator while waiting for response */}
            {isSending && (
              <div className="flex justify-start">
                <div className="max-w-[70%] rounded-2xl px-5 py-3 bg-slate-800 border border-slate-700">
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce [animation-delay:150ms]"></div>
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce [animation-delay:300ms]"></div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Area */}
      <form onSubmit={handleSubmit} className="p-6 bg-slate-800/50 backdrop-blur-sm border-t border-slate-700">
        <div className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isSending}
            placeholder="Type your message..."
            className="flex-1 bg-slate-700 border border-slate-600 text-slate-100 placeholder-slate-400 rounded-xl px-5 py-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          />
          <button
            type="submit"
            disabled={isSending || !input.trim()}
            className="px-8 py-3 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-medium rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-slate-900 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-blue-500/50"
          >
            {isSending ? 'Sending...' : 'Send'}
          </button>
        </div>
      </form>
    </div>
  );
}