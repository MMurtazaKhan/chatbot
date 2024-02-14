from rest_framework.decorators import api_view
from rest_framework.response import Response
import openai
from app.models import *
import numpy as np
from sentence_transformers import SentenceTransformer
import os


openai.api_key = "api-key"

# Create your views here.
@api_view()
def hello_world(request):
    return Response({"Message": "Hello World"})


@api_view(['POST'])
def chat(request):
    data = request.data
    user_message = data["user_message"]
    
    user_id = data['user_id']

    user_memory = ChatBot(user_id=user_id, role="user", content=user_message)
    user_memory.save()

    max_history_length = 3

    user_memory_history = ChatBot.objects.filter(user_id=user_id).order_by('-id')[:max_history_length]

    print(user_memory_history)
    memory = [{"role": message.role, "content": message.content} for message in reversed(user_memory_history)]

    user_prompt = """You are an AI-powered sustainability assistant designed to guide users in making eco-friendly choices and reducing their carbon footprint. Your mission is to empower users by providing personalized recommendations and insights on various aspects of their daily lives, including commuting habits, home energy usage, and dietary choices.

    Please follow these guidelines:

    1. Give the appropriate suggestions to reduce their carbon footprint.
    2. Give concise suggestions in bullet points
    """

    chat_prompt = [
        {"role": "system", "content": user_prompt},
        {"role": f"assistant", "content": 'Use the chat memory to help the user with their carbon footprint queries. Prioritize accurate information and offer guidance on relevant sustainable choices.'}
    ] + memory
    print("Chat Prompt: ", chat_prompt)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=chat_prompt)
    bot_message = response["choices"][0]["message"]["content"]

    bot_memory = ChatBot(user_id=user_id, role="assistant", content=bot_message)
    bot_memory.save()

    return Response({'bot_message': bot_message})



@api_view(['DELETE'])
def delete_chat_records(request):
    try:
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'User ID is required'}, status=400)
        
        # Delete records based on user_id
        ChatBot.objects.filter(user_id=user_id).delete()
        
        return Response({'message': 'Chat records deleted successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)

# # Load precomputed embeddings and corresponding questions/answers
# current_directory = os.path.dirname(os.path.abspath(__file__))
# stored_embeddings = np.load(os.path.join(current_directory, "question_embeddings.npy"))
# with open("questions.txt", "r") as file:
#     questions = file.readlines()
# with open("answers.txt", "r") as file:
#     answers = file.readlines()

# # Function to encode user query into an embedding
# def encode_user_query(user_query):
#     model = SentenceTransformer('distilbert-base-nli-mean-tokens')
#     return model.encode([user_query])[0]

# # Function to find most similar question and return its answer
# def find_most_similar_question(query_embedding, stored_embeddings, questions, answers):
#     similarities = np.dot(stored_embeddings, query_embedding)
#     most_similar_idx = np.argmax(similarities)
#     return answers[most_similar_idx]

# @api_view(['POST'])
# def chat_embeddings(request):
#     if request.method == 'POST':
#         user_message = request.data.get("user_message")
#         user_id = request.data.get('user_id')

#         # Encode the user query into an embedding
#         user_query_embedding = encode_user_query(user_message)

#         # Find the most similar question and return its answer
#         bot_answer = find_most_similar_question(user_query_embedding, stored_embeddings, questions, answers)

#         return Response({'bot_message': bot_answer})
#     else:
#         return Response({'error': 'Only POST requests are allowed.'})