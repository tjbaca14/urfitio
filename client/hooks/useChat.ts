import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { chatApi, schoolsApi } from '@/lib/api';

/**
 * Hook to send a chat message
 */
export function useSendMessage() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: chatApi.sendMessage,
    onSuccess: (response, variables) => {
      // Invalidate chat history queries to refetch
      queryClient.invalidateQueries({ queryKey: ['chat', variables.id] });
      queryClient.invalidateQueries({ queryKey: ['chats', variables.userId] });
    },
  });
}

/**
 * Hook to save a chat conversation
 */
export function useSaveChat() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: chatApi.saveChat,
    onSuccess: (data) => {
      // Update cache with saved chat
      queryClient.setQueryData(['chat', data.id], data);
      queryClient.invalidateQueries({ queryKey: ['chats', data.userId] });
    },
  });
}

/**
 * Hook to fetch chat history by ID
 */
export function useChatHistory(chatId: string | null) {
  return useQuery({
    queryKey: ['chat', chatId],
    queryFn: () => chatApi.getChatHistory(chatId!),
    enabled: !!chatId,
  });
}

/**
 * Hook to fetch all chat history for a user
 */
export function useUserChatHistory(userId: string, limit = 10) {
  return useQuery({
    queryKey: ['chats', userId, limit],
    queryFn: () => chatApi.getUserChatHistory(userId, limit),
    enabled: !!userId,
  });
}

/**
 * Hook to fetch all available divisions
 */
export function useDivisions() {
  return useQuery({
    queryKey: ['divisions'],
    queryFn: schoolsApi.getDivisions,
    // Divisions rarely change, cache for 24 hours
    staleTime: 24 * 60 * 60 * 1000,
  });
}

/**
 * Hook to fetch a single school within a division
 */
export function useSchool(divisionId: string | null, schoolId: string | null) {
  return useQuery({
    queryKey: ['school', divisionId, schoolId],
    queryFn: () => schoolsApi.getSchool(divisionId!, schoolId!),
    enabled: !!divisionId && !!schoolId,
    staleTime: 24 * 60 * 60 * 1000,
  });
}

/**
 * Hook to fetch schools for a specific division
 */
export function useSchools(division: string | null) {
  return useQuery({
    queryKey: ['schools', division],
    queryFn: () => schoolsApi.getSchoolsByDivision(division!),
    enabled: !!division,
    // Schools rarely change, cache for 24 hours
    staleTime: 24 * 60 * 60 * 1000,
  });
}

/**
 * Hook to list schools with filters within a division
 */
export function useListSchools(
  divisionId: string | null,
  params?: {
    name_contains?: string;
    limit?: number;
  }
) {
  return useQuery({
    queryKey: ['schools', 'list', divisionId, params],
    queryFn: () => schoolsApi.listSchools(divisionId!, params),
    enabled: !!divisionId,
    staleTime: 24 * 60 * 60 * 1000,
  });
}