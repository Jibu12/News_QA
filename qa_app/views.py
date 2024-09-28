# views.py
from django.shortcuts import render
import google.generativeai as genai
from django.http import JsonResponse


API_KEY = "AIzaSyBpWuDUzAkG3PRMLYGHKx6hEmmKG1soguY"  # Replace with your actual API key
genai.configure(api_key=API_KEY)


def question_answer_view(request):
    response_text = None

    if request.method == 'POST':
        article_content = request.POST.get('article_content')
        question_input = request.POST.get('question_input')

        if article_content and question_input:
            combined_input = f"Content: {article_content}\n\nQuestion: {question_input}"
            
            # Initialize the Google AI model
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            chat_session = model.start_chat(history=[])
            
            # Send the user's input to the model
            response = chat_session.send_message(combined_input)
            response_text = response.text
        else:
            response_text = "Please provide both the content and a question."

    return render(request, 'question_answer.html', {'response_text': response_text})




