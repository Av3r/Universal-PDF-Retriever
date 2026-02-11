"""Chainlit user interface application."""
import chainlit as cl

from src.config import config, init_llm_settings
from src.services.rag_engine import RAGEngineService
from src.services.vector_store import VectorDBService


@cl.password_auth_callback
def auth(username, password):
    """Verifies user credentials against the .env configuration."""
    if username == config.app_username and password == config.app_password:
        # Return a User object, which means: Successfully logged in!
        return cl.User(identifier=username)

    # Returning None means: Invalid username or password (access denied)
    return None

@cl.on_chat_start
async def start() -> None:
    """Initializes the chat environment for a new user session."""
    init_llm_settings()

    # Dependency Injection setup
    db_service = VectorDBService()
    rag_service = RAGEngineService(db_service=db_service)

    # Retrieve the configured chat engine and store it in the user's session
    chat_engine = rag_service.get_chat_engine()
    cl.user_session.set("chat_engine", chat_engine)

    await cl.Message(
        content="Hello! I am ready to analyze your documents. What would you like to know?"
    ).send()

@cl.on_message
async def main(message: cl.Message) -> None:
    """Handles incoming user messages using the context-aware RAG engine."""
    chat_engine = cl.user_session.get("chat_engine")

    # We use the native .achat() instead of cl.make_async()!
    response = await chat_engine.achat(message.content)

    source_elements = []

    # Check what exactly the system retrieved from the database
    if response.source_nodes:
        print(f"DEBUG: Success! Found {len(response.source_nodes)} fragments in the database.")
        for node in response.source_nodes:
            page = node.node.metadata.get('page_label', 'Unknown')
            source_elements.append(
                cl.Text(
                    name=f"Strona {page}",
                    content=node.node.get_text(),
                    display="side"
                )
            )
    else:
        print("DEBUG: ERROR - The database did not return any nodes for this query!")

    # Safeguard against "Empty Response" error from the LlamaIndex framework
    answer = str(response.response)
    if not answer or answer.strip() == "Empty Response":
        answer = "Przepraszam, ale nie znalazłem odpowiednich informacji w załączonym raporcie."

    # Odesłanie odpowiedzi do UI
    await cl.Message(content=answer, elements=source_elements).send()
