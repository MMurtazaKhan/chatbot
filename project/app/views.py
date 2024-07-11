from rest_framework.decorators import api_view
from rest_framework.response import Response
import openai
from app.models import *
from django.http import JsonResponse



openai.api_key = "openai-api-key"

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


@api_view(['POST'])
def carbon_reduction(request):
    data = request.data
    current_emission = data["current_emission"]
    category = data["category"]
    sub_category = data["sub_category"]
    target_emission = data["target_emission"]

    # Construct the prompt for OpenAI
    user_prompt = f"""You are an AI-powered sustainability assistant. Your mission is to help users reduce their carbon emissions in specific categories and subcategories.

    Please provide three personalized recommendations to reduce the user's carbon emissions from {current_emission} kg CO2e to {target_emission} kg CO2e in the {category} category, specifically in the {sub_category} subcategory. The recommendations should be actionable, specific, and concise.

    Give the suggestions in bullet points:
    """

    chat_prompt = [
        {"role": "system", "content": user_prompt}
    ]

    # Generate the response from OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_prompt
    )
    bot_message = response["choices"][0]["message"]["content"]

    # Convert bot message into a list of strings
    recommendations = bot_message.split("\n")

    # Remove empty strings from the list
    recommendations = [rec for rec in recommendations if rec]

    # Ensure we only return three recommendations
    recommendations = recommendations[:3]

    return Response({'recommendations': recommendations})

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


@api_view(['POST'])
def chat_history(request):
    # Get the user_id from the request data
    data = request.data
    user_id = data.get('user_id', None)

    if user_id is None:
        return JsonResponse({'error': 'user_id is required in the request body'}, status=400)

    # Retrieve all user chats ordered by id in ascending order
    user_memory_history = ChatBot.objects.filter(user_id=user_id).order_by('id')

    # Organize user chats and bot responses in the desired sequence
    chat_history = []
    user_message = None
    for message in user_memory_history:
        if message.role == 'user':
            user_message = message.content
        elif message.role == 'assistant':
            if user_message is not None:
                chat_history.append({"question": user_message, "answer": message.content})
                user_message = None

    # If the last message was a user message without a bot response, add it to the chat history
    if user_message is not None:
        chat_history.append({"question": user_message})

    # Return the chat history
    return JsonResponse({'chat_history': chat_history})