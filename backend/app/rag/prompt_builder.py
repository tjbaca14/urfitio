from typing import Optional


class PromptBuilder:
    """
    Pure prompt formatting service.

    Responsibilities:
    - Format prompt templates (context + query formatting)
    - Provide system prompts

    Does NOT:
    - Manipulate message lists
    - Handle conversation flow
    - Validate message structure

    Message flow is handled by RAGPipeline.
    """

    DEFAULT_SYSTEM_PROMPT = """Use the context in <data> xml tags to answer the user query.
If the user query cannot be determined from the context, do not answer. Inform the user as such and prompt a new question.
If a user asks a question pertaining to themselves, ask for more data to answer the question to the best of your ability."""

    def __init__(self, system_prompt: Optional[str] = None):
        """
        Initialize prompt builder.

        Args:
            system_prompt: Optional custom system prompt
        """
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT

    def format_user_message(self, user_query: str, context: Optional[str]) -> str:
        """
        Format user query with optional context.

        Pure formatting function - takes strings, returns formatted string.

        Args:
            user_query: User's query text
            context: Retrieved context to augment the query

        Returns:
            Formatted message content
        """
        if context:
            # Format with context in XML tags
            return f"""Context: <data>{context}</data>

User query: {user_query}"""
        else:
            # No context available, return plain query
            return f"User query: {user_query}"

    def get_system_prompt(self) -> str:
        """Get the configured system prompt."""
        return self.system_prompt

    def set_system_prompt(self, system_prompt: str) -> None:
        """
        Update the system prompt.

        Args:
            system_prompt: New system prompt
        """
        self.system_prompt = system_prompt
